import re
filename = './TESTER.xml'
xmlstring = open(filename, 'r').read()
xmlstring = re.sub('<IsWarped Value="true" />', '<IsWarped Value="false" />' , xmlstring)
open('./output.xml', 'w').write(xmlstring)
