import sys
import json
import csv
import requests
import pandas as pd
import bar_chart_race as bcr

"""
mp4出力するためにはffmpegがダウンロード済みでパスも通っている必要がある

"""

users = ["kemuniku", "aplysia", "BinomialSheep"]

# json2dict
results = {}
for user in users:
    data = requests.get("https://atcoder.jp/users/" + user + "/history/json").json()
    for contest in data:
        date = contest["EndTime"][:10]
        if date in results:
            results[date][user] = contest["NewRating"]
        else:
            results[date] = {user: contest["NewRating"]}

# dict2list
lists = []
# 不参加回は直前のレートで埋める
lastRates = {user: 0 for user in users}
for date, result in sorted(results.items()):
    lists.append([date])
    for user in users:
        if not user in result:
            result[user] = lastRates[user]
        lastRates[user] = result[user]
        lists[-1].append(result[user])

# list2csv
with open("output.csv", "w", newline="") as file:
    writer = csv.writer(file)
    columns = ["date"] + users
    writer.writerow(columns)
    for list in lists:
        writer.writerow(list)

# csv2mp4
df = pd.read_csv("output.csv", encoding="shift-jis", header=0, index_col=0)
bcr.bar_chart_race(df=df, n_bars=10, filename="output.mp4")
