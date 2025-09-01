# Задание «Бравый сисадмин»
# # # Решение №1
def filterdata (x:int):
    if x > 0:
        return True

def solve(models: list, available: list, manufacturers: list):
   repair_count = 0  # количество дисков, которые купит сисадмин
   ssds = []  # модели дисков из списка models, которые купит сисадмин
   list_1 = zip(models, available)
   list_2 = []
   for j in list_1:
       if j[1]==1:
           list_2.append(j[0])
   for i in list_2:
       if manufacturers[0] in i or manufacturers[1] in i or manufacturers[2] in i:
           ssds.append(i)
           repair_count += 1
           print(ssds)
   return ssds, repair_count  # Этот код менять не нужно


if __name__ == '__main__':
   # Этот код менять не нужно
   models = ['480 ГБ 2.5" SATA накопитель Kingston A400', '500 ГБ 2.5" SATA накопитель Samsung 870 EVO',
             '480 ГБ 2.5" SATA накопитель ADATA SU650', '240 ГБ 2.5" SATA накопитель ADATA SU650',
             '250 ГБ 2.5" SATA накопитель Samsung 870 EVO', '256 ГБ 2.5" SATA накопитель Apacer AS350 PANTHER',
             '480 ГБ 2.5" SATA накопитель WD Green', '500 ГБ 2.5" SATA накопитель WD Red SA500']
   available = [1, 1, 1, 1, 0, 1, 1, 0]
   manufacturers = ['Intel', 'Samsung', 'WD']

   result = solve(models, available, manufacturers)
   assert result == (['500 ГБ 2.5" SATA накопитель Samsung 870 EVO', '480 ГБ 2.5" SATA накопитель WD Green'], 2), \
       f"Неверный результат: {result}"
   print(f"Сисадмин Василий сможет купить диски: {result[0]} и починить {result[1]} компьютера")