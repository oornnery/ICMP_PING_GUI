from datetime import datetime



def time_now():
    return datetime.now().strftime('%H:%M')


input_time = int(input('Digite o tempo de execução: '))

start = time_now()

count = [start.split(':')[0], start.split(':')[1]]

if int(count[1]) + input_time > 59:
    count[0] = str(int(count[0]) + 1)
    count[1] = str(int(count[1]) + input_time - 60)
else:
    count[1] = str(int(count[1]) + input_time)

print(count)