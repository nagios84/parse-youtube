#!/home/plombir/test/trydjango/bootit/parser/bin/python
import requests
from bs4 import BeautifulSoup as bs
import csv
from time import sleep


def write_csv(data):
    with open('yt_data1.csv', 'a') as f:
        order = ['name', 'url']
        writer = csv.DictWriter(f, fieldnames=order)
        writer.writerow(data)


def get_html(url):
    return requests.get(url)


def get_page_data(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['content_html']

    soup = bs(html, 'lxml')

    items = soup.find_all('h3', attrs={'class': 'yt-lockup-title'})
    for item in items:
        name = item.find('a').get('title')
        url = item.find('a').get('href')

        data = {'name': name, 'url': url}
        write_csv(data)
    print('Writted some data!')


def get_next(response):
    if 'html' in response.headers['Content-Type']:
        html = response.text
    else:
        html = response.json()['load_more_widget_html']

    soup = bs(html, 'lxml')

    try:
        url = 'https://youtube.com' + soup.find('button', class_='load-more-button').get('data-uix-load-more-href')
    except:
        url = ''

    return url


def main():
    url = 'https://www.youtube.com/user/DotaCinema/videos'
    # url = 'https://www.youtube.com/browse_ajax?action_continuation=1&amp;continuation=4qmFsgJAEhhVQ05SUS1EV1VYZjRVVk45TDMxWTlmM1EaJEVnWjJhV1JsYjNNZ0FEZ0JZQUZxQUhvQk1yZ0JBQSUzRCUzRA%253D%253D&amp;direct_render=1'
    # response = get_html(url)
    # get_page_data(response)

    while True:
        response = get_html(url)
        print('Getting response from YouTube')
        sleep(1)
        get_page_data(response)
        print('Got page data..')
        sleep(1)
        url = get_next(response)
        print('Got new URL')

        if url:
            continue
        break


if __name__ == '__main__':
    main()
