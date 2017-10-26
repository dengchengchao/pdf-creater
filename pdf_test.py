import pdf_parser
import pdf_xmler
test=pdf_parser.pdf_parser('result.xml')
for node in test.block_list:
    print(node.line_point.left)
#for node in test.xml_list:
#    list1=[]
#    test2=pdf_xmler.block(node)
#    print(len(test2.block_list))
#    for node2 in test2.block_list:
#        char1=""
#        for node3 in node2:
#            char1+=node3.char
#        print (char1)
#        char1=""

