import requests
import json
import csv
import os
import time


#print(d['date_added'],d['date'],d['price'],d['title_1'],d['line_2'],d['line_1'],d['line_3'])
os.remove('yad2.csv')
def output_csv(date_added,date_update,address,size,floor,roms,price,neighborhood):
    if os.path.exists('yad2.csv'):
        header_exists = True
    else:
        header_exists = False
    with open('yad2.csv', mode='a', newline='',encoding='utf-8') as csv_file:
        fieldnames = ['date_added','date_update','address','neighborhood','size','floor','roms','price']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        if not header_exists:
            writer.writeheader()
        writer.writerow({'date_added':date_added,'date_update': date_update,'neighborhood':neighborhood,'address':address,'size':size,'floor':floor,'roms':roms,'price':price})

def is_float(number):
    return isinstance(number, float)

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Accept-Language': 'en-US,en;q=0.9',
    'Cache-Control': 'no-cache',
    'Connection': 'keep-alive',
    'Cookie': '__ssds=3; __ssuzjsr3=a9be0cd8e; __uzmaj3=2482bab2-e643-4981-b19f-ca5d3afc7132; __uzmbj3=1687852959; __uzmlj3=PyqZE7dcY4wB1d0cwdis7E=; y2018-2-cohort=87; leadSaleRentFree=82; __uzmb=1687852961; __uzma=1489c434-41b7-4cb2-ba68-54014c40ede2; __uzme=7900; guest_token=eyJhbGciOiJIUz3ZS04ZWQ0LTQ4NDItOTE3YS0zjoxNjg3ODUyOTYxLCJleHAiOjE3MjEwNzY4MTQ4MDN9.15-hRYa5G_B7ASy6lrVllacDfAG8zz08c_riM57i1vs; abTestKey=79; use_elastic_search=1; canary=never; __uzmcj3=105419468535; __uzmdj3=1690528114; __uzmfj3=7; server_env=production; y2_cohort_2020=8; favorites_userid=edd1063272547; __uzmd=; __uzmc=763',
    'Origin': 'https://www.yad2.co.il',
    'Pragma': 'no-cache',
    'Referer': 'https://www.yad2.co.il/',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-site',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36',
    'mainsite_version_commit': '7c9a9c5c1fe45ec28c16bc473d25aad7141f53bd',
    'mobile-app': 'false',
    'sec-ch-ua': 'Not/A)Brand";v="99", "Google Chrome";v="115", "Chromium";v="115"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': 'Windows',
}
for i in range(1,20):
    url = f'https://gw.yad2.co.il/feed-search-legacy/realestate/rent?topArea=25&area=5&city=4000&propertyGroup=apartments&price=0-4500&page={i}&forceLdLoad=true'
    time.sleep(1)
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        data = response.json()
        # Process the JSON data as needed
        for d in data['data']['feed']['feed_items']:
            try:
                neighborhood =d['neighborhood']
            except KeyError:
                neighborhood = None
            try:

                rooms = float(str(d['line_1']).split()[0])
                size = int(str(d['line_3']).split()[0])
                if size >= 80 and rooms > 3:
                    print(d['date_added'], d['date'], d['price'], d['title_1'], d['line_2'], d['line_1'], d['line_3'],
                          neighborhood)
                    output_csv(date_added=d['date_added'], date_update=d['date'], floor=d['line_2'], price=d['price'],
                               address=d['title_1'], size=size, roms=str(d['line_1']).split()[0],
                               neighborhood=neighborhood)

            except (KeyError,ValueError):
                pass
    else:
        print(f"Request failed with status code: {response.status_code}")


# ['line_1'] חדרים
#['line_2'] קומה
#['line_3'] גודל
#['title_1'] רחוב
#['search_text'] -תיאור
#['price'] מחיר
#['date_added'] -נוצר
#['date'] עדכון
