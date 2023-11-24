from bs4 import BeautifulSoup
import pandas
import requests
import pandas as pd
import threading
from queue import Queue

cookies = {
    'sid': 'ed0c137d35d22235eb869ddb283f2d07',
    'language2': 'ru',
    'lngtd-session': '98752a11-7719-4cdf-87b8-6f3bc1fd8e03',
    '_sharedID': 'ea83c3fe-7aa3-4092-830c-003c2fc17917',
    '_sharedID_cst': 'zix7LPQsHA%3D%3D',
    'pbjs-unifiedid': '%7B%22TDID%22%3A%22b77c7ff3-9012-4feb-8f46-859f546be6bd%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-19T20%3A41%3A13%22%7D',
    'pbjs-unifiedid_cst': 'zix7LPQsHA%3D%3D',
    'panoramaId_expiry': '1700512873165',
    '_cc_id': 'c0963e152d8b101fc2c08c8a2541b7bf',
    'panoramaId': '985bee11a78c3c1d9088e359cba3a9fb927a29bd94ab99d2158189aab1cd6e16',
    '__qca': 'P0-1378401203-1700426473019',
    '_pbjs_userid_consent_data': '3524755945110770',
    '_sharedid': '7cf3bab3-44c2-4499-8024-e5a5ca31baf5',
    'OptanonAlertBoxClosed': '2023-11-19T20:41:25.892Z',
    '_gcl_au': '1.1.1415494099.1700426487',
    '_tt_enable_cookie': '1',
    '_ttp': 'gv1EW-tAD20EGuB4aNtZsF8D9vy',
    '_gid': 'GA1.2.91205893.1700426488',
    '_hjFirstSeen': '1',
    '_hjIncludedInSessionSample_1817499': '0',
    '_hjSession_1817499': 'eyJpZCI6ImZkZjc0YmQzLTQyYWUtNGZmNy04MjBkLWVlOGY5Mzc3MGJlNSIsImNyZWF0ZWQiOjE3MDA0MjY0ODc1ODEsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=',
    '_hjAbsoluteSessionInProgress': '0',
    '_hjHasCachedUserAttributes': 'true',
    '__hstc': '182323384.7b937f77a236c8702845623bf28c36e7.1700426508915.1700426508915.1700426508915.1',
    'hubspotutk': '7b937f77a236c8702845623bf28c36e7',
    '__hssrc': '1',
    'cto_bundle': '3P2Ppl9HTXdzSEFRNDM2N04yY0FUMk1QbUdkNG5zOE9wVHNJaEtGNkIzOHpjandSZGFkTjlwaFBpTng5MnlUSGI0VElNZmxReEhRMFowOGV5VkdzWUJlMTlZU3YyU2tNTkFlMjclMkZDQmdPWHRQWmEwMUJZc3V2NDd5bGlMdEFOczd5SGlhYmVZajZWcDY5RmtFZXBZSzdMd2RxdyUzRCUzRA',
    '__cf_bm': 'kA.uZrNPkm8Ilno6b9OpNoinMODbwdglhXZwvL7.3nw-1700426896-0-ASmSxvnKwVhwFcqXrx7oYlM2EJ2q3lWMQdeWgGN/rhuBO53/Ek7VvR0zchT/0QsaCnfeCJ6sJ6rprhmpXYvjG8k=',
    '_ga_XPPVCBYHPD': 'GS1.1.1700426487.1.1.1700426906.0.0.0',
    '_ga': 'GA1.1.1862921769.1700426487',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Sun+Nov+19+2023+23%3A48%3A27+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=e3be2c41-ac39-47cd-bc0f-efefcd4cb9e5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=FR%3B',
    '_hjSessionUser_1817499': 'eyJpZCI6ImE4MzY2NjYzLWJmZmQtNWU3Yy1iMTg2LTZiZmViODBhZDYxYiIsImNyZWF0ZWQiOjE3MDA0MjY0ODc1ODAsImV4aXN0aW5nIjp0cnVlfQ==',
    'lngtd-sdp': '3',
    '__hssc': '182323384.2.1700426508917',
}

headers = {
    'authority': 'www.discogs.com',
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7',
    # 'cookie': 'sid=ed0c137d35d22235eb869ddb283f2d07; language2=ru; lngtd-session=98752a11-7719-4cdf-87b8-6f3bc1fd8e03; _sharedID=ea83c3fe-7aa3-4092-830c-003c2fc17917; _sharedID_cst=zix7LPQsHA%3D%3D; pbjs-unifiedid=%7B%22TDID%22%3A%22b77c7ff3-9012-4feb-8f46-859f546be6bd%22%2C%22TDID_LOOKUP%22%3A%22TRUE%22%2C%22TDID_CREATED_AT%22%3A%222023-10-19T20%3A41%3A13%22%7D; pbjs-unifiedid_cst=zix7LPQsHA%3D%3D; panoramaId_expiry=1700512873165; _cc_id=c0963e152d8b101fc2c08c8a2541b7bf; panoramaId=985bee11a78c3c1d9088e359cba3a9fb927a29bd94ab99d2158189aab1cd6e16; __qca=P0-1378401203-1700426473019; _pbjs_userid_consent_data=3524755945110770; _sharedid=7cf3bab3-44c2-4499-8024-e5a5ca31baf5; OptanonAlertBoxClosed=2023-11-19T20:41:25.892Z; _gcl_au=1.1.1415494099.1700426487; _tt_enable_cookie=1; _ttp=gv1EW-tAD20EGuB4aNtZsF8D9vy; _gid=GA1.2.91205893.1700426488; _hjFirstSeen=1; _hjIncludedInSessionSample_1817499=0; _hjSession_1817499=eyJpZCI6ImZkZjc0YmQzLTQyYWUtNGZmNy04MjBkLWVlOGY5Mzc3MGJlNSIsImNyZWF0ZWQiOjE3MDA0MjY0ODc1ODEsImluU2FtcGxlIjpmYWxzZSwic2Vzc2lvbml6ZXJCZXRhRW5hYmxlZCI6dHJ1ZX0=; _hjAbsoluteSessionInProgress=0; _hjHasCachedUserAttributes=true; __hstc=182323384.7b937f77a236c8702845623bf28c36e7.1700426508915.1700426508915.1700426508915.1; hubspotutk=7b937f77a236c8702845623bf28c36e7; __hssrc=1; cto_bundle=3P2Ppl9HTXdzSEFRNDM2N04yY0FUMk1QbUdkNG5zOE9wVHNJaEtGNkIzOHpjandSZGFkTjlwaFBpTng5MnlUSGI0VElNZmxReEhRMFowOGV5VkdzWUJlMTlZU3YyU2tNTkFlMjclMkZDQmdPWHRQWmEwMUJZc3V2NDd5bGlMdEFOczd5SGlhYmVZajZWcDY5RmtFZXBZSzdMd2RxdyUzRCUzRA; __cf_bm=kA.uZrNPkm8Ilno6b9OpNoinMODbwdglhXZwvL7.3nw-1700426896-0-ASmSxvnKwVhwFcqXrx7oYlM2EJ2q3lWMQdeWgGN/rhuBO53/Ek7VvR0zchT/0QsaCnfeCJ6sJ6rprhmpXYvjG8k=; _ga_XPPVCBYHPD=GS1.1.1700426487.1.1.1700426906.0.0.0; _ga=GA1.1.1862921769.1700426487; OptanonConsent=isGpcEnabled=0&datestamp=Sun+Nov+19+2023+23%3A48%3A27+GMT%2B0300+(%D0%9C%D0%BE%D1%81%D0%BA%D0%B2%D0%B0%2C+%D1%81%D1%82%D0%B0%D0%BD%D0%B4%D0%B0%D1%80%D1%82%D0%BD%D0%BE%D0%B5+%D0%B2%D1%80%D0%B5%D0%BC%D1%8F)&version=202211.1.0&isIABGlobal=false&hosts=&consentId=e3be2c41-ac39-47cd-bc0f-efefcd4cb9e5&interactionCount=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0005%3A1&geolocation=FR%3B; _hjSessionUser_1817499=eyJpZCI6ImE4MzY2NjYzLWJmZmQtNWU3Yy1iMTg2LTZiZmViODBhZDYxYiIsImNyZWF0ZWQiOjE3MDA0MjY0ODc1ODAsImV4aXN0aW5nIjp0cnVlfQ==; lngtd-sdp=3; __hssc=182323384.2.1700426508917',
    'referer': 'https://www.discogs.com/ru/',
    'sec-ch-ua': '"Google Chrome";v="119", "Chromium";v="119", "Not?A_Brand";v="24"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
}

def get_data(id, name, result_queue):

    params = {
        'q': name,
        'type': 'all',
    }

    search_result_response = requests.get('https://www.discogs.com/ru/search', params=params, cookies=cookies, headers=headers)


    soup = BeautifulSoup(search_result_response.text, 'html.parser')

    try:
        output = soup.find('ul', {'id': 'search_results'})
        discs = output.find_all('li', {'role': 'listitem'})
        link = discs[0].find('a', {'class': 'search_result_title'})['href']
    except AttributeError:
        print("attribute error")
        return

    release_response = requests.get(
        url=f'https://www.discogs.com{link}', params=params, cookies=cookies, headers=headers,
    )


    release_soup = BeautifulSoup(release_response.text, 'html.parser')
    data = release_soup.find('table', {'class': 'table_1fWaB'})

    info_about_release = {
        'id': id,
        'genre': [],
        'style': [],
        'decade': None,
        'year': None,
    }

    try:
        for dataframe in data.find_all('a', {'class': 'link_1ctor'}):
            info = str(dataframe['href'])

            if info.find('style') != -1:
                info_about_release['style'].append(info.split('/')[-1].replace('%20', ' '))

            if info.find('genre') != -1:
                info_about_release['genre'].append(info.split('/')[-1].replace('%20', ' '))

            if info.find('decade') != -1:
                info_about_release['decade'] = info.split('decade=')[1][:4]

            if info.find('year') != -1:
                info_about_release['year'] = info.split('year=')[1][:4]
        print(info_about_release)
    except:
        print("couldnt process", name)
    
    result_queue.put(info_about_release) 


id_artist_title_path = "../data/intermediate-data/id-artist-title.csv"

MAX_THREADS = 32


def main():
    data = pd.read_csv(id_artist_title_path)
    
    info_list = []
    result_queue = Queue()
    threads = []    
    threads_counter = 0


    for index, row in data.iterrows():
        name = f"{row['artist']}, {row['title']}"
        
        thread = threading.Thread(target=get_data, args=(row['id'], name, result_queue))
        thread.start()
        threads.append(thread)

        threads_counter += 1

        if threads_counter == MAX_THREADS:

            for thread in threads:
                thread.join()

            threads = []
            threads_counter = 0
            print('\n')

    with open("dataset.tsv", "w") as file:
        file.write("id\tgenre\tstyle\tdecade\tyear\n")
        while not result_queue.empty():            
            info = result_queue.get()
            # list of genre to comma separated string
            genre = ','.join(info['genre'])
            # list of style to comma separated string
            style = ','.join(info['style'])
            file.write(f"{info['id']}\t{genre}\t{style}\t{info['decade']}\t{info['year']}\n")


if __name__ == '__main__':
    main()