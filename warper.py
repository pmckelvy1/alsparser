import re
import xml.etree.ElementTree as et
from als_modder import ALSModder

# open and read file
filename = '../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/scale_chord_a.xml'
# filename = '../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/scale_chord_b.xml'
# filename = './projects/drumrack_mod/TESTER.xml'
xmlstring = open(filename, 'r').read()

# unwarp all simplers
xmlstring = re.sub('<IsWarped Value="true" />', '<IsWarped Value="false" />' , xmlstring)

# add pitch control to all simplers
pitcher_string = re.search(r'(?P<pitcher><MidiPitcher.*</MidiPitcher>)', xmlstring, flags=re.DOTALL)

copyable_device_name = "MidiPitcher"

# find copyable text
device_chain = "device_chain"
copyable_device_search_stirng = "<" + copyable_device_name + ".*</" + copyable_device_name + ">\s+"
copyable_device_xml = re.search(r'(?P<' + device_chain + '>' + copyable_device_search_stirng + ')', xmlstring, flags=re.DOTALL)
copy_end = copyable_device_xml.end(device_chain)
copyable_device_string = copyable_device_xml.group(device_chain)

# find where to insert
position_chain = "position_chain"
insertable_position_name = "OriginalSimpler"
insertable_position_search_string = "<" + insertable_position_name
insertable_position_xml = re.finditer(r'(?P<' + position_chain + '>' + insertable_position_search_string + ')', xmlstring, flags=re.DOTALL)

final_str = xmlstring

i_pos_arr = [ipx for ipx in insertable_position_xml]
i = len(i_pos_arr) - 1
while i > 0:
    insertable_pos = i_pos_arr[i]
    insertable_position_start = insertable_pos.start(position_chain)
    final_str = final_str[0:insertable_position_start] + copyable_device_string + final_str[insertable_position_start:]
    i -= 1

als_modder = ALSModder('../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/scale_chord_a_output.xml', '../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/scale_chord_a_output.xml')
als_modder.load_source_string(final_str)
als_modder.mod_ids()
to_add = '<?xml version="1.0" encoding="UTF-8"?>\n'
final_str = to_add + et.tostring(als_modder.source_tree).decode('utf-8')

# write output
open('../../PS 2018 Followthru/AUDIO ONLY CHORD TEMPLATE Project/scale_chord_a_output.xml', 'w').write(final_str)
# open('./projects/drumrack_mod/output2.xml', 'w').write(final_str)
