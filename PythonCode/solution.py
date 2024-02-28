from openpyxl import load_workbook
from openpyxl import Workbook
import math

workbook = load_workbook(filename="Coordinates.xlsx")
sheet = workbook.active

# функция расстояния между двумя точками на плоскости
def dist(x1, y1, x2, y2):
    return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)


deliver = []
cost = []
cour = []
n = 0
m = 0
r = 0
minimal = [100000.0, -1, -1]
test = 0

#чтение из таблицы, сгенерированной ранее рандомно

for row in sheet.iter_rows(values_only=True):
    m += 1
    deliver.append([row[0], row[1], row[2], row[3]])
    cost.append(row[4])
    if row[5]:
        cour.append([row[5], row[6], 16000.0])
        n += 1
count = m
ans = [[] for i in range(n)]

# основной цикл
# находит минимальную сумму (расстояние от курьера до старта + длина доставки)
# так как неоходимо за минимальное время отвезти все посылки
# у меня нет доказательства, что такая логика верна, но при взятом примере с маленькими переменными она сработала
# в отличие от других способов

while True:
    if minimal[0] < 100000.0:
        mindel = deliver[minimal[2]]
        cour[minimal[1]] = [mindel[2], mindel[3], minimal[0]]
        deliver[minimal[2]] = [-12000, -12000, -12000, -12000]
        ans[minimal[1]].append(minimal[2] + 1)
        if test < minimal[0]:
            test = minimal[0]
        minimal = [100000.0, -1, -1]
        count -= 1
    for i in range(n):
        for j in range(m):
            if any(k > 0 for k in deliver[j]):
                r = dist(deliver[j][0], deliver[j][1], cour[i][0], cour[i][1])
                r += dist(deliver[j][0], deliver[j][1], deliver[j][2], deliver[j][3]) + cour[i][2]
            if minimal[0] > r:
                minimal = [r, i, j]
    if count <= 0:
        break

# сохранение ответов (с суммой заказов каждого курьера) в новой таблице

workbook = Workbook()
sheet = workbook.active
k = 0
for i in ans:
    summ = 0
    k += 1
    for j in i:
        summ += cost[j-1]
    sheet.append(i)
    sheet["G"+str(k)] = str(summ)
workbook.save('Answer.xlsx')

