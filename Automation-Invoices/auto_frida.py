import csv
import sys
import tabula
import PyPDF2
import re
import pandas as pd
import json
from collections import namedtuple

Inv = namedtuple('Inv', 'vend_num vend_name inv_dt due_dt inv_amt net_amt description')



pdf_file = open('Invoice_template.pdf', 'rb')

read_pdf = PyPDF2.PdfFileReader(pdf_file)

#caputurar o numero de pgs
number_of_pages = read_pdf.getNumPages()

#lê a primeira pagina toda 
page = read_pdf.getPage(0)

#extrair o texto
page_content = page.extractText()

parsed = ''.join(page_content) #junção das linhasi
parsed = re.sub('/n', '',parsed) #quebra de linhas
#print(parsed)


## Convertento para Json ###########################
with open ('./frida_all.csv','w',newline='\n',encoding='utf-8') as csvfile:
    csv.writer(csvfile,delimiter=',').writerows(parsed)

with open("frida_json.json", "w") as arquivo:     
    json.dump(parsed,arquivo,indent=4)

csv_data = pd.read_csv("frida_all.csv")
csv_data.to_json("frida_json.json", orient = "records")

df = pd.read_json (r'frida_json.json')
df.to_csv (r'frida_dejson.csv', index = None)


##################################################

Name = re.compile(r'Name:\s[a-zA-Z]{2,}\s[a-zA-Z]{1,}[a-zA-Z]')
name = Name.findall(parsed)
for line in parsed.split('\n'):
    if Name.match(line):
        print(line)


#Invoice = parsed[203]
Invoice = re.compile(r'\s\s[0-9]\s')
voice = Invoice.findall(parsed)
for line in parsed.split('\n'):
    if Invoice.match(line):
        print(line)



Date = re.compile('\d{1,2}\D\d{1,2}\D\d{4}')
check = Date.findall(parsed)
#print(check)

Description = parsed[248:315]
#print(Description)

#Total_Amount
Total = re.compile('L\s\s.+')
total = Total.findall(parsed)


with open ('./frida.csv','w',newline='\n',encoding='utf-8') as csvfile:
    csv.writer(csvfile, delimiter=',').writerow(['Name','Invoice','Date','Description','Total Amount'])
    csv.writer(csvfile, delimiter=',').writerow([name,voice,check,Description,total])




