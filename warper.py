import re

# open and read file
filename = './TESTER.xml'
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

# write output
open('./output.xml', 'w').write(final_str)
