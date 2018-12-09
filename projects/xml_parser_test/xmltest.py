import xml.etree.ElementTree as et

filename = './test.xml'
tree = et.parse(filename)
tree.write('output.xml')
# xmlstring = open(filename, 'r').read()