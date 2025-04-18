import csv
import os


def open_csv(filename):
    file_path = os.path.abspath(f'csv_files/{filename}')
    with open(file_path, newline='', encoding='cp1251') as File:
        reader = csv.reader(File)
        pars = False
        pars_data = []
        for line in reader:
            if line:
                if "РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ВРЕМЕНИ" in line[0]:
                    pars = True
                if "РАСПРЕДЕЛЕНИЕ ВХОДОВ ПО БИЛЕТАМ ПО ТОЧКАМ ДОСТУПА" in line[0]:
                    pars = False
                if pars:
                    pars_data.append(line[0])
    return pars_data


def parser_data_of_time(data):
    total_data = " ".join(data[:1])
    total_data_finish = total_data[:-1].split()
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
    return time_pars, count_pars, percent_pars, total_data_finish, df

#Ввод имя файла CSV
#filename = input("Введите файл ")
# data_for_parser = open_csv("Статистика 12.03 Акрон - Спартак.csv")
# diagram = parser_data_of_time(data_for_parser[3:])
# print(len(diagram[2]), diagram[2])
# print(len(diagram[0]), diagram[0])
# print(len(diagram[1]), diagram[1])
# print(diagram[3])

# df = {'Время проходов':'', 'Количество проходов': ''}
# df['Время проходов'] = diagram[0]
# df['Количество проходов'] = diagram[1]
# print(df)