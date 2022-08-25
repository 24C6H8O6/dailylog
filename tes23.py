import pandas as pd

data = pd.read_csv("gardenAll.csv", encoding='euc-kr')
plant = "청옥"
data2 = data[data['name'] == plant]
data3 = data2['temp(°C)']
print(float(data3))