from datetime import datetime
import json

results_run = open('results_RUN.txt')
def open_json_file():
    with open('competitors2.json', encoding='utf-8') as name_dict:
        name_dict = json.load(name_dict)
    return name_dict
def preparing_data(results_run):
    results_run_data = results_run.readlines()
    results_run_data = [line.replace('\n', '') for line in results_run_data]
    results_run_data[0] = results_run_data[0].replace("ï»¿", "")
    return results_run_data
def get_result(results_run_data):
    for i in range(0, len(results_run_data), 2):
        runner = results_run_data[i].split()[0]
        start_time = datetime.strptime(results_run_data[i].split()[2], '%H:%M:%S,%f')
        finish_time = datetime.strptime(results_run_data[i + 1].split()[2], '%H:%M:%S,%f')
        result = finish_time - start_time
        times[runner] = result
    times_sorted = dict(sorted(times.items(), key=lambda item: item[1]))
    return times_sorted
def fill_finally_dictionary():
    counter = 1
    finally_dictionary = {}
    for number in times_sorted:
        if number in name_dict:
            name_info = name_dict[number]
            finally_dictionary[counter] = {
                'Нагрудный номер': str(number),
                'Имя': name_info['Surname'],
                'Фамилия': name_info['Name'],
                'Результат': str(times_sorted[number]),
            }
        counter += 1
    return finally_dictionary
def print_table(finally_dictionary):
    headers = ['Занятое место','Нагрудный номер', 'Имя', 'Фамилия', 'Результат']
    print('{:<15} {:<15} {:<15} {:<15} {:<15}'.format(*headers))
    for key, value in finally_dictionary.items():
        row = [key] + [value.get(header, '') for header in headers[1:]]
        print('{:<15} {:<15} {:<15} {:<15} {:<15}'.format(*row))

times = {}
name_dict = open_json_file()
results_run_data = preparing_data(results_run)
times_sorted = get_result(results_run_data)
finally_dictionary = fill_finally_dictionary()

#output to final_results.json file
with open('final_results.json', 'w', encoding='utf-8') as file:
    json.dump(finally_dictionary, file, ensure_ascii=False, indent='')

print_table(finally_dictionary)