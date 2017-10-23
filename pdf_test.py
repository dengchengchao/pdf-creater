import pdf_parser
test=pdf_parser.pdf_parser('result.xml')
print(len(test.xml_list))
for node in test.xml_list:
    print(node.line_point)
