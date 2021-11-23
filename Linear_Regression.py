import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

df = pd.read_csv("Dataset_JP_Perf1200.csv")

df0 = df[df["type"] == 0]

#パラメータはRating, Ave_diff, Attending, RPS,  Total_AC_count, Ave_points
X = "Total_AC_count"
Y = "RPS"

x = df0[["{}".format(X)]]
y = df0[["{}".format(Y)]]
print(df0.head())

model = LinearRegression()
model.fit(x, y)

plt.plot(x,y,"o")
plt.xlabel("{}".format(X))
plt.ylabel("{}".format(Y))
plt.plot(x, model.predict(x), linestyle="solid")
plt.show()

print('モデル関数の回帰変数 w1: %.3f' %model.coef_)
print('モデル関数の切片 w2: %.3f' %model.intercept_)
print('y= %.3fx + %.3f' % (model.coef_ , model.intercept_))
print('相関係数 r： ', model.score(x, y)**.5)
print()
