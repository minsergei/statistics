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

def parser_data_of_sectors(data):
    all_list_only_sum = []
    all_list_without_summ = []
    kpp_dict = {}
    for i in data[1][4:]:
        str = re.split(r"\s\s+", i)
        if "ВСЕГО" in str[1]:
            all_list_only_sum.append(str)
        else:
            all_list_without_summ.append(str)
    for name, group in itertools.groupby(all_list_without_summ, lambda x: x[0]):
        kpp_group = []
        # print(name)
        for i in group:
            kpp_group.append(*i[1:2])
            # print(i[1:2])
        kpp_dict[name] = kpp_group
    return all_list_only_sum

# Ввод имя файла CSV, для теста
#filename = input("Введите файл ")
# test = parser_data_of_sectors(open_csv("spartak.csv"))
# print(test)

# print(kpp_dict)
# [print(i[2]) for i in all_list_only_sum]



# print(data_for_parser)
# diagram = parser_data_of_time(data_for_parser[0][3:])
# print(diagram[0])
# print(diagram[1])
