import requests
import csv
import time
import json
import math
import pandas as pd
from urllib import request
from bs4 import BeautifulSoup
import re
import Scraping as Sc

def coloring(N):
    color = ["Gray", "Brown", "Green", "Cyan", "Blue", "Yellow", "Orange", "Red"]
    return color[N // 400] if N < 3200 else color[7]

#SはUser_id
def First_Rating_Count(S):


    #ユーザーページでスクレイピングを実行
    url = "https://atcoder.jp/users/{}?graph=rating".format(S)
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    script = soup.find_all("script")

    print(S)

    for i in script:
        if "rating_history" in str(i):
            i = str(i)
            word = re.search("\"NewRating\":[0-9]*,\"OldRating\":0",i).group()

    #初回変動レートを計算する
    st,en = 0,0
    for i in range(len(word)):
        if word[i] == ":":
            st = i + 1
        elif word[i] == ",":
            en = i - 1
            break

    Rating_diff = int(word[st:en+1])
    #変動レート147(Perf = 1200程度)以下を0, それより上を1として分類

    return 1 if Rating_diff >= 147 else 0
    
            
def main():
    st = time.time()
    #csvを生成
    #Sc.Username_Scraping()
    main_csv = open("Scraping.csv","r",encoding = "ms932", errors = "", newline="")
    main_csv_dic = csv.DictReader(main_csv, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)

    problem_models = open("problem-models.json", "r")
    problem_models = json.load(problem_models)


    #2020-4-29
    N = 1588158028

    #["user_id", "Rating", "色" "diffの平均値", "RPS", "合計AC数", "Ave_points", "type"]の形式のデータを作成する
    data = [["a",0,"a",0,"b",0,0,0] for _ in range(1500)]
    User_cnt = 0

    for i in main_csv_dic:
        total, cnt = 0, 0
        S = i["User_id"]

        url1 = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/submissions?user={}&from_second={}".format(S, N)
        res1 = requests.get(url1)

        url2 = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/rated_point_sum_rank?user={}".format(S)
        res2 = requests.get(url2)

        url3 = "https://kenkoooo.com/atcoder/atcoder-api/v3/user/ac_rank?user={}".format(S)
        res3 = requests.get(url3)

        #print(res1,res2)

        #if res2 == "<Response [404]>":
        #    continue

        for problem_data in res1.json():
          
            if problem_data["problem_id"] not in problem_models or "difficulty" not in problem_models[problem_data["problem_id"]]:
                continue
            tmp = problem_models[problem_data["problem_id"]]["difficulty"]

            if problem_data["result"] == "AC":
                if tmp < 0:
                    tmp = int(400 / math.exp(1 - (tmp/400)))
                total += tmp
                cnt += 1

        data[User_cnt][0] = S
        data[User_cnt][1] = i["Rating"]
        data[User_cnt][2] = coloring(int(i["Rating"]))
        data[User_cnt][4] = res2.json()["count"]
        data[User_cnt][5] = res3.json()["count"]
        data[User_cnt][6] = data[User_cnt][4] / data[User_cnt][5]
        if cnt == 0:
            data[User_cnt][3] = 0
        else:
            data[User_cnt][3] = int(total/cnt)
        data[User_cnt][7] = First_Rating_Count(S)

        print(data[User_cnt])
        User_cnt += 1



    #CSVファイルを生成する
    #filename
    S = "Dataset_world_Perf1200.csv"


    with open("C:/Users/mcah8/OneDrive/デスクトップ/大学/授業/B3 後期/デザプロ/ソフトウェアリポジトリマイニング/{}".format(S),"w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User_id", "Rating", "Color", "Ave_diff", "RPS", "Total_AC_count", "Ave_points", "type"])
        for i in range(len(data)):
            writer.writerow(data[i])

    #CSVファイル内の余分なデータを削除する
    df = pd.read_csv(S)
    df = df[df["User_id"] != "a"]
    df.to_csv(S)



    #秒数をh,m,s形式に変換
    total_time = time.time() - st
    hh = total_time // 3600
    mm = (total_time - 3600 * hh) // 60
    ss = total_time - 60 * mm - 3600 * hh

    print("{}h{}m{}s".format(int(hh),int(mm),int(ss)))




if __name__ == "__main__":
    main()
