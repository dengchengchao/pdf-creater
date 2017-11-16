import xml.etree.ElementTree as ET
tag_forward='{http://www.abbyy.com/FineReader_xml/FineReader10-schema-v1.xml}'
root=ET.parse('result.xml').getroot()
line=root.iter(tag_forward+'line')
for node in line:
   print node.get('b')
    #node2=node.findall(tag_forward+'formatting')
    #for node3 in node2:
       # for node4 in node3:
           #node5=node3.findall(tag_forward+'charParams')
           #for node6 in node5:
               #for node7 in node6.find(tag_forward+'charRecVariants').findall(tag_forward+'charRecVariant'):
                   #print(node7.text)
