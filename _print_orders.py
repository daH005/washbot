from tabulate import tabulate

from db import TimeWindow

if __name__ == '__main__':
    headers = ['Окно', 'Кто записался', 'ID в Телеграме', 'Комната']
    table = []
    for time_window in TimeWindow.all():
        if not time_window.user_id:
            continue
        table.append([time_window.text, time_window.user.name, time_window.user.id, time_window.user.room])

    print(tabulate(table, headers, tablefmt='simple'))

    while True:
        pass
