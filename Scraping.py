from urllib import request
from bs4 import BeautifulSoup
import csv
import re
import pandas as pd

def Rating_Scraping(n,url):
    html = request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")

    tbody = soup.find_all("tbody")
    tbody = soup.find_all("td")
    tbody = soup.find_all("b")

    Rating = []

    for i,word in enumerate(tbody, 0):
        if i % 2 != 0:
            continue
        Rate = int(str(word)[3:7])
        if Rate >= 2000:
            Rating.append(Rate)
        else:
            break

    return Rating

def Username_Scraping():
    User_list = [["username", 0] for i in range(1500)]
    User_cnt = 0
    
    for n in range(1,16):
        url = "https://atcoder.jp/ranking?f.Affiliation=&f.BirthYearLowerBound=0&f.BirthYearUpperBound=9999&f.CompetitionsLowerBound=0&f.CompetitionsUpperBound=9999&f.Country=&f.HighestRatingLowerBound=0&f.HighestRatingUpperBound=9999&f.RatingLowerBound=0&f.RatingUpperBound=9999&f.UserScreenName=&f.WinsLowerBound=0&f.WinsUpperBound=9999&page={}".format(n)
        html = request.urlopen(url)
        #print(url)
        soup = BeautifulSoup(html, "html.parser")

        cnt = 0
        Rating = Rating_Scraping(n,url)

        a = soup.find_all("a")
        for i in a:
            S = str(i)
            if "class=\"username\"" in S:
                word = re.search("href=\"/users/[a-z,0-9,!,A-Z,_]*",S).group()
            else:
                continue
            
            if cnt > len(Rating):
                break

            User_list[User_cnt][0] = word[13:len(word)]
            if cnt == len(Rating):
                User_list[User_cnt][1] = Rating[cnt-1]
            else:
                User_list[User_cnt][1] = Rating[cnt]
            User_cnt += 1
            cnt += 1

    #filename
    S = "Scraping.csv"
    with open("C:/Users/mcah8/OneDrive/デスクトップ/大学/授業/B3 後期/デザプロ/ソフトウェアリポジトリマイニング/{}".format(S),"w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["User_id", "Rating"])
        for i in range(len(User_list)):
            writer.writerow(User_list[i])

    #CSVファイル内の余分なデータを削除する
    df = pd.read_csv(S)
    df = df[df["User_id"] != "username"]
    print(df)
    df.to_csv(S)

