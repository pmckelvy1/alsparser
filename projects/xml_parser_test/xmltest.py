import xml.etree.ElementTree as et

filename = './test.xml'
tree = et.parse(filename)
tree.write('test.xml')
add_to_top = '<?xml version="1.0" encoding="UTF-8"?>\n'
xmlstring = open(filename, 'r').read()
res = add_to_top + xmlstring
open(filename, 'w').write(res)