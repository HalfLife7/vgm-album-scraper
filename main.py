# imports
import requests
import requests_cache
import json
from bs4 import BeautifulSoup

# main method
def main():
    # set headers for requests
    headers = requests.utils.default_headers()
    headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:52.0) Gecko/20100101 Firefox/52.0',
    })

    # set cache for requests
    requests_cache.install_cache('vgm_cache')

    # set pages for beautifulsoup
    base_page = 'https://vgmdb.net/search?do=results&id=477523&field=&&page='
    page_number = 1

    # set json data for output
    data = {}
    data['albums'] = []

    # 300 total pages to scrape
    while page_number <= 5:
        # cycle through pages from 1-300
        next_page = base_page + str(page_number)
        page = requests.get(next_page, headers=headers)

        # check if page being read is cached - 'True')
        print(page.from_cache)

        # read page
        soup = BeautifulSoup(page.text, 'html.parser')

        # find the html that contains the albums
        album_list = soup.find_all('a', {'class':'album-game'})

        # go through albums and get the album title and id
        for album in album_list:
            album_title = album.get('title', 'no title attribute')
            album_id = (album.get('href').split('/')[4])
            print('{} {}'.format(album_title, album_id))
            # append to json object
            data['albums'].append({
                'title': album_title,
                'id': album_id,
            })
        
        # increment counter
        page_number += 1

    # write json to file
    with open('data.json', 'w') as outfile:
        json.dump(data, outfile)

# run main
main()