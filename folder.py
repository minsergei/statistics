import os

def input_match():
    matchs_load = []
    dir_path = os.path.abspath('csv_files/')
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith('.csv'):
                matchs_load.append(file)
    return matchs_load

if __name__ == '__main__':
    print(input_match())
    print(os.path.abspath('csv_files/'))