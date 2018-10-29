from xml.etree import ElementTree as et

filename = './TESTER.xml'
tree = et.parse(filename)
# tree.find('.//IsWarped').Value = 'false'
warped = tree.findall('.//IsWarped')
for w in warped:
    w.attrib["Value"] = "false"
# print(repr(warped))
tree.write(filename)
