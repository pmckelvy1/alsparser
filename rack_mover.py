import re
import json

# * * * PROJECT STRUCTURE ASSUMPTIONS * * *
# 1. all tracks are in groups
# 2. all groups are named "*** <group name> ***"
# 3. xxx_GROUP_NAMES contains the ordered list of groups in the source project

SEED_GROUP_NAMES = [
    'BASS GROUP',
    'CHORDS GROUP'
]

TEMPLATE_GROUP_NAMES = [
    'BASS GROUP',
    'CHORDS GROUP',
    'DRUMS GROUP'
]

# TEMPLATE_GROUP_NAMES = [
#     'KICK GROUP',
#     'PERC GROUP',
#     'CLAP GROUP',
#     'SNARE GROUP',
#     'HAT GROUP',
#     'TAMB / SHAKER GROUP',
#     'CYMBAL GROUP',
#     'SUB GROUP',
#     'BASS GROUP',
#     'CHORDS GROUP',
#     'LEAD GROUP',
#     'FX GROUP',
#     'VOX GROUP'
# ]

# open and read file
proj_dir = './projects/rack_mover/'
seed_file_name = 'test_rack.xml'
template_file_name = 'simp_template.xml'

def get_group_datas(xmlstr, group_names):
    xml_start = 0
    group_datas = []
    for i in range(0, len(group_names)):
        group_name = group_names[i]
        found_group = re.search(r'(?P<groups>\t+<GroupTrack Id.*<UserName Value="[*][*][*] ' + group_name + ' [*][*][*]" />)', xmlstr[xml_start:], flags=re.DOTALL)
        group_id = get_group_id(found_group.group('groups'))
        group_datas.append({'name': group_name, 'id': group_id, 'start_idx': found_group.start() + xml_start})
        if i > 0:
            group_datas[i - 1]['end_idx'] = xml_start + found_group.start()
        # set new starting point for search
        xml_start += found_group.end()
    end_idx = get_first_return_idx(xmlstr)
    end_data = {'name': 'END', 'id': 0, 'start_idx': end_idx, 'end_idx': len(xmlstr)}
    group_datas[-1]['end_idx'] = end_idx
    group_datas.append(end_data)
    return group_datas

def get_group_id(group_xml):
    group_opening = re.search(r'(?P<group_opening><GroupTrack Id="\d+">)', group_xml, flags=re.DOTALL)
    group_id = re.search(r'\d+', group_opening.group('group_opening'))
    return group_id.group(0)

def get_first_return_idx(xmlstr):
    first_return = re.search(r'(?P<first_return>\t+<ReturnTrack Id)', xmlstr, flags=re.DOTALL)
    return first_return.start()

def get_group_xmls(xmlstr, group_datas):
    for i in range(0, len(group_datas)):
        if i == len(group_datas) - 1:
            group_datas[i]['xml'] = ''
            continue
        start_idx = group_datas[i]['start_idx']
        end_idx = group_datas[i+1]['start_idx']
        group_datas[i]['xml'] = xmlstr[start_idx:end_idx]
    return group_datas

def get_group_inner_tracks(group_xml):
    idx = get_group_track_end_idx(group_xml)
    return group_xml[idx:]

def get_group_track_end_idx(group_xml):
    group_track = re.search(r'(?P<group_track>\t+</GroupTrack>)', group_xml, flags=re.DOTALL)
    return group_track.end()

def get_seed_group_data(seed_xml):
    seed_group_datas = get_group_datas(seed_xml, SEED_GROUP_NAMES)
    seed_group_datas = get_group_xmls(seed_xml, seed_group_datas)
    for i in range(0, len(seed_group_datas)):
        if seed_group_datas[i]['name'] == 'END':
            group_inner_tracks = ''
        else:
            group_inner_tracks = get_group_inner_tracks(seed_group_datas[i]['xml'])
        seed_group_datas[i]['inner_tracks'] = group_inner_tracks
    return seed_group_datas

def get_template_group_data(template_xml):
    template_group_datas = get_group_datas(template_xml, TEMPLATE_GROUP_NAMES)
    template_group_datas = get_group_xmls(template_xml, template_group_datas)
    # print_data_2(template_group_datas, template_xml)
    return template_group_datas

def set_group_track_id(inner_track_xml, new_id):
    return re.sub('<TrackGroupId Value="\d+" />', '<TrackGroupId Value="' + str(new_id) + '" />', inner_track_xml)

def route_inner_tracks(seed_group_datas, template_group_datas):
    for i in range(0, len(seed_group_datas)):
        sgd = seed_group_datas[i]
        group_name = sgd['name']
        template_group = [tgd for tgd in template_group_datas if tgd['name'] == group_name][0]
        seed_group_datas[i]['inner_tracks'] = set_group_track_id(sgd['inner_tracks'], template_group['id'])
    return seed_group_datas

def prune_inner_tracks(template_group_datas):
    for i in range(0, len(template_group_datas)):
        if template_group_datas[i]['name'] == 'END':
            continue
        tgd = template_group_datas[i]
        group_track_end_idx = get_group_track_end_idx(tgd['xml'])
        template_group_datas[i]['xml'] = tgd['xml'][:group_track_end_idx]
    return template_group_datas

def add_seed_tracks_to_template_groups(seed_group_datas, template_group_datas):
    for i in range(0, len(template_group_datas)):
        tgd = template_group_datas[i]
        group_name = tgd['name']
        seed_group = [sgd for sgd in seed_group_datas if sgd['name'] == group_name]
        if len(seed_group) == 0:
            continue
        template_group_datas[i]['xml'] = tgd['xml'] + seed_group[0]['inner_tracks']
    return template_group_datas

def add_final_groups_to_template(template_group_datas, template_xml):
    all_groups_xml = ''.join([xml['xml'] for xml in template_group_datas if xml['name'] != 'END'])
    final_xml = template_xml[:template_group_datas[0]['start_idx']] + all_groups_xml + '\n'
    final_xml = final_xml + template_xml[template_group_datas[len(template_group_datas) - 1]['start_idx']:]
    return final_xml

def run():
    # get xmls
    seed_xml = open(proj_dir + seed_file_name, 'r').read()
    template_xml = open(proj_dir + template_file_name, 'r').read()

    # gather data
    seed_group_datas = get_seed_group_data(seed_xml)
    template_group_datas = get_template_group_data(template_xml)

    # modify group ids for inner tracks
    route_inner_tracks(seed_group_datas, template_group_datas)
    # print_datas(seed_group_datas)

    # prune template inner tracks from template group xml
    template_group_datas = prune_inner_tracks(template_group_datas)
    # print_datas(template_group_datas)

    # add seed inner tracks to template groups
    template_group_datas = add_seed_tracks_to_template_groups(seed_group_datas, template_group_datas)
    print_datas(template_group_datas)

    # recombine final xml
    final_xml_str = add_final_groups_to_template(template_group_datas, template_xml)
    open('./final.xml', 'w').write(final_xml_str)


def print_datas(data):
    for d in data:
        print('\n * * * * * * \n')
        print_data(d)

def print_data(d):
    for k, v in d.items():
        print(k + ' : ' + json.dumps(str(v)))

def print_data_2(data, xml):
    for d in data:
        print('\n * * * * * * \n')
        print_data(d)
        print('\n * * * START * * * \n')
        print(xml[d['start_idx'] - 100:d['start_idx'] + 100])
        print('\n * * * END * * * \n')
        print(xml[d['end_idx'] - 100:d['end_idx'] + 100])
        print('\n * * * * * * \n')

# # add pitch control to all simplers
# group_string = re.search(r'(?P<pitcher><MidiPitcher.*</MidiPitcher>)', xmlstring, flags=re.DOTALL)
#
# copyable_device_name = "MidiPitcher"
#
# # find copyable text
# device_chain = "device_chain"
# copyable_device_search_stirng = "<" + copyable_device_name + ".*</" + copyable_device_name + ">\s+"
# copyable_device_xml = re.search(r'(?P<' + device_chain + '>' + copyable_device_search_stirng + ')', xmlstring, flags=re.DOTALL)
# copy_end = copyable_device_xml.end(device_chain)
# copyable_device_string = copyable_device_xml.group(device_chain)
#
# # find where to insert
# position_chain = "position_chain"
# insertable_position_name = "OriginalSimpler"
# insertable_position_search_string = "<" + insertable_position_name
# insertable_position_xml = re.finditer(r'(?P<' + position_chain + '>' + insertable_position_search_string + ')', xmlstring, flags=re.DOTALL)
#
# final_str = xmlstring
#
# i_pos_arr = [ipx for ipx in insertable_position_xml]
# i = len(i_pos_arr) - 1
# while i > 0:
#     insertable_pos = i_pos_arr[i]
#     insertable_position_start = insertable_pos.start(position_chain)
#     final_str = final_str[0:insertable_position_start] + copyable_device_string + final_str[insertable_position_start:]
#     i -= 1

# # write output
# open('./output.xml', 'w').write(final_str)


if __name__ == '__main__':
    run()
