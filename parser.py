import csv
import os
import re
import itertools


def open_csv(filename):
    file_path = os.path.abspath(f'csv_files/{filename}')
    with open(file_path, newline='', encoding='cp1251') as File:
        reader = csv.reader(File)
        pars = 0
        pars_data = []
        pars_data_2 = []
        for line in reader:
            if line:
                if "РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ" in line[0]:
                    pars = 1
                if pars == 1:
                    pars_data.append(line[0])
                if "РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ТОЧКАМ ДОСТУПА" in line[0]:
                    pars = 2
                if pars == 2:
                    pars_data_2.append(line[0])
                if "РАСПРЕДЕЛЕНИЕ СОБЫТИЙ ВХОДОВ ПО БИЛЕТАМ" in line[0]:
                    pars = 3
                # if "РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ТОЧКАМ ДОСТУПА" in line[0]:
                #     pars = 0
                # if pars == 1:
                #     pars_data.append(line[0])
    return pars_data[:-1], pars_data_2[:-1]

# Парсим данные для РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ
def parser_data_of_time(data):
    total_data = " ".join(data[:1])
    total_data_finish = total_data[:-1].split() #Общие данные
    time_pars = []
    count_pars = []
    percent_pars = []
    for str in data[1:]:
        data = "".join(str[:-1]).split()
        time = "".join(data[:1])
        time_pars.append(time[:-3])
        count_pars.append(int("".join(data[3:4])))
        percent_pars.append(float("".join(data[4:])))
    df = {'Время проходов': '', 'Количество проходов': ''}
    df['Время проходов'] = time_pars
    df['Количество проходов'] = count_pars
    df['В %'] = percent_pars
    return total_data_finish, df

"""-----------------------------------------------------------------"""
# Ввод имя файла CSV, для теста
#filename = input("Введите файл ")

data_for_parser = open_csv("spartak.csv")

total_data = " ".join(data_for_parser[1][3:4])
# print(total_data.split())
all_list_only_sum = []
all_list_without_summ = []
kpp_dict = {}
for i in data_for_parser[1][4:]:
    str = re.split(r"\s\s+", i)
    if "ВСЕГО" in str[1]:
        all_list_only_sum.append(str)
    else:
        all_list_without_summ.append(str)
for name, group in itertools.groupby(all_list_without_summ, lambda x: x[0]):
    kpp_group = []
    for i in group:
        kpp_group.append(i[1:])
    kpp_dict[name] = kpp_group
# dictionary = {
#     'G1': {
#         'G1_1': 15, 'G1_2': 44, 'G1_3': 145}}
print(kpp_dict.keys())
# print(all_dict)
# for i in all_dict.values():
#     # print(i)
#     for i in i:
#         print(i)


# print(data_for_parser)
# diagram = parser_data_of_time(data_for_parser[0][3:])
# print(diagram[0])
# print(diagram[1])
