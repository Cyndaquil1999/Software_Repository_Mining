import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Dataset_JP_Perf1200.csv")
#df = pd.read_csv("test2(Perf_border = 1600).csv")


print("-------df-------")
#統計情報あれこれ
print(df.describe())
print()
print("Rating_corration")
print(df.corr()["Rating"])

S = "Rating"

#グラフ
#ax1 = df.plot.scatter(x="Ave_diff", y=S)
#ax2 = df.plot.scatter(x="RPS", y=S)
#ax3 = df.plot.scatter(x="Ave_points", y=S)




print()
#初回perf < 1200を0、 perf >= 1200を1と分類した
print("-------df0(Only type0)-------")
df0 = df[df["type"] == 0]

#統計情報あれこれ
print(df0.describe())
print()
print("Rating_corration")
print(df0.corr()["Rating"])


#グラフ
#S = "Rating"
#df0["{}".format(S)].hist(bins = 30)
#plt.title("Distribution of {} df0".format(S))
#plt.xlabel("{}".format(S))
#plt.ylabel("Number of people")
pg = sns.pairplot(df0, kind="reg")
pg.savefig("df0_JP.png")
df0.plot.scatter(x="Ave_diff", y=S)
df0.plot.scatter(x="RPS", y=S)
df0.plot.scatter(x="Ave_points", y=S)
df0.plot.scatter(x="Total_AC_count", y=S)
plt.show()


print()


print("-------df1(Only type1)-------")
df1 = df[df["type"] == 1]

#統計情報あれこれ
print(df1.describe())
print()
print("Rating_corration")
print(df1.corr()["Rating"])


#グラフ
#df0.plot.scatter(x="Rating", y="Now_Color - start(day)")
#df1["{}".format(S)].hist(bins = 30)
#plt.title("Distribution of {} df1".format(S))
#plt.xlabel("{}".format(S))
#plt.ylabel("Number of people")
#plt.show()
