import urllib.request
from bs4 import BeautifulSoup
import json

url = "https://old.reddit.com/top/"
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.3'}
request = urllib.request.Request(url,headers=headers)
html = urllib.request.urlopen(request).read()
soup = BeautifulSoup(html,'html.parser')
#First lets get the HTML of the table called site Table where all the links are displayed
main_table = soup.find("div",attrs={'id':'siteTable'})
#Now we go into main_table and get every a element in it which has a class "title" 
links = main_table.find_all("a",class_="title")
#List to store a dict of the data we extracted 
extracted_records = []
for link in links: 
    title = link.text
    url = link['href']
    #There are better ways to check if a URL is absolute in Python. For sake simplicity we'll just stick to .startwith method of a string 
    # https://stackoverflow.com/questions/8357098/how-can-i-check-if-a-url-is-absolute-using-python 
    if not url.startswith('http'):
        url = "https://reddit.com"+url 
    # You can join urls better using urlparse library of python. 
    # https://docs.python.org/3/library/urllib.parse.html#urllib.parse.urljoin 
    #Lets just print it 
    print("%s - %s"%(title,url))
    record = {
        'title':title,
        'url':url
        }
    extracted_records.append(record)
#Lets write these to a JSON file for now. 
with open('data.json', 'w') as outfile:
    json.dump(extracted_records, outfile, indent=4)