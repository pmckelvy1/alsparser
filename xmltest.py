import xml.etree.ElementTree as et

filename = './projects/drumrack_mod/TESTER.xml'
tree = et.parse(filename)
tree.write('output.xml')
# xmlstring = open(filename, 'r').read()