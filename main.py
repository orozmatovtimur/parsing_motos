from os import write
import requests
from bs4 import BeautifulSoup as bs
import csv 

def get_html(url):
    response = requests.get(url)
    return response.text


def get_data(html):

    soup = bs(html, 'lxml')
    # catalog = soup.find('div', class_ = "table-view-list image-view clr label-view")
    catalog = soup.find('div', class_ = "search-results-table")

    motorcycles =catalog.find_all('div', class_ = "list-item list-label")

    for moto in motorcycles:

        try:
            title = moto.find('h2', class_ = "name").text.strip().replace('\n', '').replace(' ', '')
        except:
            title = ''
            
        try:
            price = moto.find('p', class_= "price").text.strip().replace('\n', '').replace(' ','')

        except:
            price = 'Договорная'
        try:
            year = moto.find('p', class_ = "year-miles").text.strip().replace('\n', '')

        except:
            year = ''
        try:
            type = moto.find('p', class_ = "body-type").text.strip().replace('\n', '')

        except:
            type = ''
        try:
            volume = moto.find('p', class_ = "volume").text.strip().replace('\n', '')

        except:
            volume = ''
        try:
            city = moto.find('p', class_ = "city").text.strip().replace('\n', '').replace('                          ', ' ')

        except:
            city = ''

        try:
            image = moto.find('img', class_ = "lazy-image").get("data-src") + '' + '\n'
            
        except:
            image = 'https://teja9.kuikr.com/images/bikeNoImage.jpg'


        data = { "title" : title,
                 "price" : price,
                 "year" : year, 
                 "type" : type,
                 "volume" : volume,
                 "city" : city,
                 "image" : image }

        write_to_csv(data)
        


def write_to_csv(data):
    with open('motorcycles.csv', 'a') as file:
        writer = csv.writer(file, delimiter = "\n" )

        writer.writerow([ data["title"],
                          data["price"],
                          data["year"],
                          data["type"],
                          data["volume"],
                          data["city"],
                          data["image"] ])

def main():
    with open('motorcycles.csv', 'w') as file:
        pass

    i = 1
    while True:
        url = f"https://www.mashina.kg/motosearch/all/?page={i}"
        html = get_html(url)
        if bs(get_html(url), "lxml").find('div', class_ = "search-results-table"):
            get_data(html)
            i+= 1
        else:
            break

main()

