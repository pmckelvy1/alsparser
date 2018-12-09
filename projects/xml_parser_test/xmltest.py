import xml.etree.ElementTree as et

filename = './test.xml'
tree = et.parse(filename)
tree.write('test.xml')
# xmlstring = open(filename, 'r').read()