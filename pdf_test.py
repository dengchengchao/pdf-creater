import pdf_parser
import pdf_xmler
test=pdf_parser.pdf_parser('result.xml')
print(len(test.xml_list))
for node in test.xml_list:
    list1=[]
    test2=pdf_xmler.block(node)
    for node2 in test2:
        print(node2.point.left)
