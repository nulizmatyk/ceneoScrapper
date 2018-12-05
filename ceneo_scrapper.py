import urllib.request
from bs4 import BeautifulSoup
import json
from time import sleep 


def extract_opinions

url = "https://www.ceneo.pl/35379099"

#Adding a User-Agent String in the request to prevent getting blocked while scraping 
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
request = urllib.request.Request(url,headers={'User-Agent': user_agent})

html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html,'html.parser')

#First lets get the HTML of the table called site Table where all the links are displayed
main_table = soup.find("div",attrs={'class':'page-tab-content click no-padding wrapper', })

offers = main_table.find_all("tr",attrs={'class': ['product-offer js_product-offer', 'promoted']})
extracted_data = []

for a_tag in offers:
    print(a_tag['data-shopurl'])
    


print(len(offers))
# print(offers)