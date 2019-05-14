import requests
import xlrd
from bs4 import BeautifulSoup
import datetime
group = {}
groups_list = {}

def get_week():
        page = requests.get("https://www.mirea.ru/")
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.find("div", {"class":"date_text uk-display-inline-block"})
        week = ""
        for el in result:
                if "идет" in el:
                        for char in el:
                                if str(char).isdigit():
                                        week += char
        return week

even = int(get_week()) % 2

with open("id.txt", "r") as file:
                for line in file:
                        arr = line.strip().split(" ")
                        group[int(arr[0])] = arr[1]

def rasp_download():
        page = requests.get("https://www.mirea.ru/education/schedule-main/schedule/")
        soup = BeautifulSoup(page.text, "html.parser")
        result = soup.find("div", {"id":"toggle-3"}).findAll("a", {"class":"xls"})

        for x in result:
                if "IIT" in str(x) and "1k" in str(x):
                        try:
                                f = open("1k.xlsx", 'r')
                        except Exception:
                                f = open("1k.xlsx", "wb")
                                u = requests.get(x["href"])
                                f.write(u.content)
                                f.close()
                elif "IIT" in str(x) and "2k" in str(x):
                        try:
                                f = open("2k.xlsx", 'r')
                        except Exception:                         
                                f = open("2k.xlsx", "wb")
                                u = requests.get(x["href"])
                                f.write(u.content)
                                f.close()
                elif "IIT" in str(x) and "3k" in str(x):
                        try:
                                f = open("3k.xlsx", 'r')
                        except Exception:
                                f = open("3k.xlsx", "wb")
                                u = requests.get(x["href"])
                                f.write(u.content)
                                f.close()
                elif "IIT" in str(x) and "4k" in str(x):
                        try:
                                f = open("4k.xlsx", 'r')
                        except Exception:
                                f = open("4k.xlsx", "wb")
                                u = requests.get(x["href"])
                                f.write(u.content)
                                f.close()

def get_rasp(file):
        book = xlrd.open_workbook(file)
        sheet = book.sheet_by_index(0)
        num_cols = sheet.ncols
        num_rows = sheet.nrows
        for col_index in range(num_cols):
                group_cell = str(sheet.cell(1, col_index).value)
                if "-1" in group_cell:
                        groups_list[group_cell] = {}
        for col_index in range(num_cols):
                for group in groups_list.keys():
                        if group == str(sheet.cell(1, col_index).value):
                                groups_list[group] = [
                                        {0: dict(), 1: dict(), 2: dict(), 3: dict(), 4: dict(), 5: dict()},
                                        {0: dict(), 1: dict(), 2: dict(), 3: dict(), 4: dict(), 5: dict()}
                                        ]
                                row_index1 = 3
                                row_index2 = 4
                                for day in groups_list[group][0].keys():
                                        groups_list[group][0][day] = {"1 пара": dict(), "2 пара": dict(), "3 пара": dict(), "4 пара": dict(), "5 пара": dict(), "6 пара": dict()}
                                        for couple in groups_list[group][0][day].keys():
                                                groups_list[group][0][day][couple] = {"Предмет": "-", "Вид занятия": "", "Преподаватель": "", "Аудитория": ""}
                                                groups_list[group][0][day][couple]['Предмет'] = str(sheet.cell(row_index2, col_index).value)
                                                groups_list[group][0][day][couple]['Вид занятия'] = str(sheet.cell(row_index2, col_index+1).value)
                                                groups_list[group][0][day][couple]['Преподаватель'] = str(sheet.cell(row_index2, col_index+2).value)
                                                groups_list[group][0][day][couple]['Аудитория'] = str(sheet.cell(row_index2, col_index+3).value)
                                                row_index2 += 2
                                for day in groups_list[group][1].keys():
                                        groups_list[group][1][day] = {"1 пара": dict(), "2 пара": dict(), "3 пара": dict(), "4 пара": dict(), "5 пара": dict(), "6 пара": dict()}
                                        for couple in groups_list[group][1][day].keys():
                                                groups_list[group][1][day][couple] = {"Предмет": "-", "Вид занятия": "", "Преподаватель": "", "Аудитория": ""}
                                                groups_list[group][1][day][couple]['Предмет'] = str(sheet.cell(row_index1, col_index).value)
                                                groups_list[group][1][day][couple]['Вид занятия'] = str(sheet.cell(row_index1, col_index+1).value)
                                                groups_list[group][1][day][couple]['Преподаватель'] = str(sheet.cell(row_index1, col_index+2).value)
                                                groups_list[group][1][day][couple]['Аудитория'] = str(sheet.cell(row_index1, col_index+3).value)
                                                row_index1 += 2
        return groups_list

def set_group(id, new_group):
        group[id] = new_group
        with open("id.txt", "w") as file:
                for id in group.keys():
                        file.write(str(id) + " " + group[id] + "\n")

def get_group(id):
        try:
                return group[id]
        except Exception:
                return "Вы не написали номер группы"
def today_rasp(id):
        try:
                arr = []
                for couple in groups_list[group[id]][even][int(datetime.date.today().weekday())].keys():
                                arr.append(str(
                                        couple + ": " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())][couple]["Предмет"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())][couple]["Вид занятия"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())][couple]["Аудитория"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())][couple]["Преподаватель"] + "\n"
                                ))
                return arr
        except Exception:
                return "Вы не написали номер группы"
def tomorrow_rasp(id):
        try:
                arr = []
                for couple in groups_list[group[id]][even][int(datetime.date.today().weekday())+1].keys():
                                arr.append(str(
                                        couple + ": " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())+1][couple]["Предмет"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())+1][couple]["Вид занятия"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())+1][couple]["Аудитория"] + " " +
                                        groups_list[group[id]][even][int(datetime.date.today().weekday())+1][couple]["Преподаватель"] + "\n"
                                ))
                return arr
        except Exception:
                return "Вы не написали номер группы"
def week_rasp(id):
        try:
                arr = ["ПОНЕДЕЛЬНИК\n", "ВТОРНИК\n", "СРЕДА\n", "ЧЕТВЕРГ\n", "ПЯТНИЦА\n", "СУББОТА\n"]
                i = 0
                for day in groups_list[group[id]][even].keys():
                        for couple in groups_list[group[id]][0][day].keys():
                                arr[i] += str(
                                        couple + ": " +
                                groups_list[group[id]][even][day][couple]["Предмет"] + " " +
                                groups_list[group[id]][even][day][couple]["Вид занятия"] + " " +
                                groups_list[group[id]][even][day][couple]["Аудитория"] + " " +
                                groups_list[group[id]][even][day][couple]["Преподаватель"] + "\n"
                                )
                        i += 1
                return arr
        except Exception:
                return "Вы не написали номер группы"
def nextweek_rasp(id):
        try:
                arr = ["ПОНЕДЕЛЬНИК\n", "ВТОРНИК\n", "СРЕДА\n", "ЧЕТВЕРГ\n", "ПЯТНИЦА\n", "СУББОТА\n"]
                i = 0
                for day in groups_list[group[id]][(even+1)%2].keys():
                        for couple in groups_list[group[id]][(even+1)%2][day].keys():
                                arr[i] += str(
                                        couple + ": " +
                                groups_list[group[id]][(even+1)%2][day][couple]["Предмет"] + " " +
                                groups_list[group[id]][(even+1)%2][day][couple]["Вид занятия"] + " " +
                                groups_list[group[id]][(even+1)%2][day][couple]["Аудитория"] + " " +
                                groups_list[group[id]][(even+1)%2][day][couple]["Преподаватель"] + "\n"
                                )
                        i += 1
                return arr
        except Exception:
                return "Вы не написали номер группы"
def daygroup_rasp(day, agroup):
        arr = ["ЧЕТНАЯ НЕДЕЛЯ\n", "НЕЧЕТНАЯ НЕДЕЛЯ\n"]
        for couple in groups_list[agroup][0][day].keys():
                        arr[0] += str(
                                couple + ": " +
                                groups_list[agroup][0][day][couple]["Предмет"] + " " +
                                groups_list[agroup][0][day][couple]["Вид занятия"] + " " +
                                groups_list[agroup][0][day][couple]["Аудитория"] + " " +
                                groups_list[agroup][0][day][couple]["Преподаватель"] + "\n"
                        )
        for couple in groups_list[agroup][1][day].keys():
                        arr[1] += str(
                                couple + ": " +
                                groups_list[agroup][1][day][couple]["Предмет"] + " " +
                                groups_list[agroup][1][day][couple]["Вид занятия"] + " " +
                                groups_list[agroup][1][day][couple]["Аудитория"] + " " +
                                groups_list[agroup][1][day][couple]["Преподаватель"] + "\n"
                        )
        return arr

def professor_rasp(professor, date):
        string = ""
        arr = ["ПОНЕДЕЛЬНИК\n", "ВТОРНИК\n", "СРЕДА\n", "ЧЕТВЕРГ\n", "ПЯТНИЦА\n", "СУББОТА\n"]
        if date.lower() == "сегодня":
                rasp = {"1 пара": "", "2 пара": "", "3 пара": "", "4 пара": "", "5 пара": "", "6 пара": ""}
                for group in groups_list.keys():
                        for couple in groups_list[group][even][int(datetime.date.today().weekday())].keys():
                                if professor == groups_list[group][even][int(datetime.date.today().weekday())][couple]["Преподаватель"]:
                                        if (rasp[couple] == ""):
                                                rasp[couple] = (
                                                        groups_list[group][even][int(datetime.date.today().weekday())][couple]["Предмет"] + ", " +
                                                        groups_list[group][even][int(datetime.date.today().weekday())][couple]["Вид занятия"] + ", " +
                                                        groups_list[group][even][int(datetime.date.today().weekday())][couple]["Аудитория"] + ", " +
                                                        group
                                                )
                                        else:
                                                rasp[couple] += group + ", "
                for key, value in rasp.items():
                        string += key + ") " + value + "\n"
        elif date.lower() == "завтра":
                rasp = {"1 пара": "", "2 пара": "", "3 пара": "", "4 пара": "", "5 пара": "", "6 пара": ""}
                for group in groups_list.keys():
                        for couple in groups_list[group][even][int(datetime.date.today().weekday())+1].keys():
                                if professor == groups_list[group][even][int(datetime.date.today().weekday())+1][couple]["Преподаватель"]: 
                                        if (rasp[couple] == ""):
                                                rasp[couple] = (
                                                        groups_list[group][even][int(datetime.date.today().weekday())+1][couple]["Предмет"] + ", " +
                                                        groups_list[group][even][int(datetime.date.today().weekday())+1][couple]["Вид занятия"] + ", " +
                                                        groups_list[group][even][int(datetime.date.today().weekday())+1][couple]["Аудитория"] + ", " +
                                                        group
                                                )
                                        else:
                                                rasp[couple] += group + ", "
                for key, value in rasp.items():
                        string += key + ") " + value + "\n"
        elif date.lower() == "эта неделя":
                rasp = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
                for day in rasp.keys():
                        rasp[day] = {"1 пара": "", "2 пара": "", "3 пара": "", "4 пара": "", "5 пара": "", "6 пара": ""}
                for group in groups_list.keys():
                        for day in groups_list[group][even].keys():
                                for couple in groups_list[group][even][day].keys():
                                        if professor == groups_list[group][even][day][couple]["Преподаватель"]:
                                                if (rasp[day][couple] == ""):
                                                        rasp[day][couple] = (
                                                                groups_list[group][even][day][couple]["Предмет"] + ", " +
                                                                groups_list[group][even][day][couple]["Вид занятия"] + ", " +
                                                                groups_list[group][even][day][couple]["Аудитория"] + ", " +
                                                                group
                                                        )
                                                else:
                                                        rasp[day][couple] += group + ", "
                for day in rasp.keys():
                        for couple in rasp[day].keys():
                                arr[day] += couple + ") " + rasp[day][couple] + "\n"
                string = "".join(arr)
        elif date.lower() == "следующая неделя":
                rasp = {0:{}, 1:{}, 2:{}, 3:{}, 4:{}, 5:{}}
                for day in rasp.keys():
                        rasp[day] = {"1 пара": "", "2 пара": "", "3 пара": "", "4 пара": "", "5 пара": "", "6 пара": ""}
                for group in groups_list.keys():
                        for day in groups_list[group][(even+1)%2].keys():
                                for couple in groups_list[group][(even+1)%2][day].keys():
                                        if professor == groups_list[group][(even+1)%2][day][couple]["Преподаватель"]:
                                                if (rasp[day][couple] == ""):
                                                        rasp[day][couple] = (
                                                                groups_list[group][(even+1)%2][day][couple]["Предмет"] + ", " +
                                                                groups_list[group][(even+1)%2][day][couple]["Вид занятия"] + ", " +
                                                                groups_list[group][(even+1)%2][day][couple]["Аудитория"] + ", " +
                                                                group
                                                        )
                                                else:
                                                        rasp[day][couple] += group + ", "
                for day in rasp.keys():
                        for couple in rasp[day].keys():
                                arr[day] += couple + ") " + rasp[day][couple] + "\n"
                string = "".join(arr)
        return "Расписание " + professor + " " + date + ":\n" + string

def professors(professor):
        arr = []
        for group in groups_list.keys():
                for week in groups_list[group]:
                        for day in week.keys():
                                for couple in week[day].keys():
                                        if (
                                                professor in week[day][couple]["Преподаватель"].lower() and 
                                                week[day][couple]["Преподаватель"] not in arr and 
                                                "\n" not in week[day][couple]["Преподаватель"]
                                        ):
                                                arr.append(week[day][couple]["Преподаватель"])
        return arr
get_rasp("1k.xlsx")
get_rasp("2k.xlsx")
get_rasp("3k.xlsx")
get_rasp("4k.xlsx")


