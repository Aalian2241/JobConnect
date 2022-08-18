
def open_pdf_file(file_name):
    from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
    from pdfminer.converter import TextConverter
    from pdfminer.layout import LAParams
    from pdfminer.pdfpage import PDFPage
    from io import StringIO
    output = StringIO()
    manager = PDFResourceManager()
    converter = TextConverter(manager, output, laparams=LAParams())
    interpreter = PDFPageInterpreter(manager, converter)

    pagenums = set()
    try:
        infile = open(file_name, 'rb')
    except:
        pass
    for page in PDFPage.get_pages(infile, pagenums):
        interpreter.process_page(page)
    infile.close()
    converter.close()
    text = output.getvalue()
    output.close()

    result = []

    for line in text.split('\n'):
        line2 = line.strip()
        if line2 != '':
            result.append(line2)
    return result, text

 # Load your PDF
a = open_pdf_file("Tahir's Resume (1).pdf")
print(a[1])