import os
from bs4 import BeautifulSoup as bs
import requests

playlist_url = 'https://www.youtube.com/watch?v=rjttzxG3hZw&list=PLPCWXaq8VyL2vi649E08OJAFzJtIA-Yaa'

data = []
r = requests.get(playlist_url)
page = r.text
soup = bs(page, 'html.parser')
b = open("a.html", "w", encoding="utf_8")
b.write(str(soup))
c = open("a.html", "r", encoding="utf_8")

d = c.readlines()
lin = 0
while True:
    try:
        a = d[lin]
    except:
        print("Finished")
        break
    if '"url":"/watch?v=' in a:
        a = a.split('"url":"')
        te = 0

        while True:
            try:
                if "/watch?v=" in a[te]:
                    aa = a[te].split('",')
                    e = 0
                    while True:
                        try:
                            if "/watch?v=" in aa[e]:
                                url = "https://www.youtube.com" + aa[e]
                                # url is added in data if you want to print all url uncomment this code
                                # print(url)
                                data.append(url)
                        except:

                            break
                        e += 1

            except:

                break
            te += 1

    lin += 1
c.close()
b.close()
os.remove("a.html")


with open('links.txt', 'a') as file:
    for link in data:
        file.write(f'{link}\n')
