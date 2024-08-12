import PyPDF2
import pandas as pd 
import pdfplumber
import re


with open("/home/hope/work4/work/0.pdf/2024 신입생 정시 모집요강_20240102.pdf", 'rb') as file:
    docs = PyPDF2.PdfReader(file)
    page = docs.pages
    pdf = pdfplumber.open("/home/hope/work4/work/0.pdf/2024 신입생 정시 모집요강_20240102.pdf")

    with open("Handong4.txt", "a") as txt:
        txt.write("======================================================================")
        txt.write("여기서부터는 경상국립대학교 정시모집 요강입니다.")
        for i in range(len(page)):
            page = docs.pages[i]
            text = page.extract_text()
            txt.write(text)
            table_page = pdf.pages[i]
            table = table_page.extract_tables()
            
            if table:
                for num in range(len(table_page.extract_tables())):
                    table = table_page.extract_tables()[num]
                    for items in table:
                        text = ""
                        for item in items:
                            if item != None:
                                if not re.findall("\n",item):
                                    text += " "
                                    text += item
                                else:
                                    item = item.replace('\n', '')
                            else:
                                text += ""
                        txt.write(text)

           
            if text:
                rows = text.split("\n")
                for row in rows:
                    if row == None:
                        pass
                    else:
                        txt.write(row)
                        txt.write("\n")
            txt.write("\n")
