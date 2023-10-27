import time
import requests
import threading
from collections import deque
import os

MAX_THREADS = 10
TIMEOUT = 10

links = deque()
valid = []

with open('./links.txt', 'r') as file:
    for line in file:
        links.append(line.strip())


def check_number(
        link: str,
):
    try:
        os.system(f'yt-dlp -x --audio-format mp3 --audio-quality 0 {link}')

    except requests.Timeout:
        links.append(link)
        print("Read timeout")
    except requests.exceptions.ConnectionError:
        links.append(link)
        print("Read timeout")
        time.sleep(TIMEOUT)


def main():

    threads = []
    threads_counter = 0

    while len(links) != 0:

        print(f'{len(links)} left')

        thread = threading.Thread(target=check_number, args=(links.pop(),))
        thread.start()
        threads.append(thread)

        threads_counter += 1

        if threads_counter == MAX_THREADS:

            for thread in threads:
                thread.join()

            threads = []
            threads_counter = 0
            print('\n')

    while len(links) != 0 or len(threads) != 0:

        for thread in threads:
            thread.join()
        threads = []

        if len(links) != 0:
            thread = threading.Thread(target=check_number, args=(links.pop(),))
            thread.start()
            threads.append(thread)


if __name__ == "__main__":
    MAX_THREADS = int(input('Enter number of threads: '))
    main()