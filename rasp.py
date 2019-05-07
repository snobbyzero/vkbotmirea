import requests
import xlrd
from bs4 import BeautifulSoup

page = requests.get("https://www.mirea.ru/education/schedule-main/schedule/")
soup = BeautifulSoup(page.text, "html.parser")

result = soup.find("div", {"id":"toggle-3"}).findAll("a", {"class":"xls"})

for x in result:
    if "IIT" in str(x) and "1k" in str(x):
        f = open("1k.xlsx", "wb")
        u = requests.get(x["href"])
        f.write(u.content)

book = xlrd.open_workbook("1k.xlsx")
sheet = book.sheet_by_index(0)

num_cols = sheet.ncols
num_rows = sheet.nrows

groups_list = []

for col_index in range(num_cols):
    group_cell = str(sheet.cell(1, col_index).value)
    if "-18" in group_cell:
        groups_list.append(group_cell)
        #{group: [{"Mon":[пары]}]}
for el in groups_list:
    print(el)