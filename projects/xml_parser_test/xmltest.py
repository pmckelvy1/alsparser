import xml.etree.ElementTree as et

filename = './test_rack.xml'
tree = et.parse(filename)
tree.write('test_rack.xml')
# xmlstring = open(filename, 'r').read()