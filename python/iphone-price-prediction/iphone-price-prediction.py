# pip install pandas matplotlib scikit-learn

import pandas
# import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

data=pandas.read_csv("iphone-data.csv")

# plt.bar(data['version'],data['price'])
# plt.barh(data['version'],data['price'])
# plt.scatter(data['version'],data['price'])
# plt.show()

# print(data.head())

model=LinearRegression()

model.fit(data[['version']],data[['price']])

print(model.predict([[20]]))

