import urllib.request
from tkinter import *
from bs4 import BeautifulSoup
import json
from time import sleep 

#Adding a User-Agent String in the request to prevent getting blocked while scraping 

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'


# function which is run by button and doind all process of data extraction
def go():
    text.delete(1.0, END)
    url = 'https://www.ceneo.pl/' + entry.get() + '#tab=reviews'
    request = urllib.request.Request(url, headers={'User-Agent': user_agent})

    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    #First lets get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("div",attrs={'class':'screening-wrapper' })

    offers = main_table.find_all("li",attrs={'class': 'review-box js_product-review'})
    extracted_data = []

    for a_tag in offers:
        # print(a_tag['data-shopurl'])
       extracted_data.append(a_tag.find("span",attrs={'class':'review-score-count'}).text)
    #    print(a_tag.find("span",attrs={'class':'review-score-count'}).text) 


    print(len(offers))
    text.insert(1.0, extracted_data)

# build gui window to let user put url to scrap
browser_window = Tk()
browser_window.title('cENEO SCRAPPER')
label = Label(browser_window, text ='Enter product Id: ')
entry = Entry(browser_window)
entry.insert(END, "35379099")
button = Button(browser_window, text='go', command= go)
text = Text(browser_window)

# insert parts of gui to in window
label.pack(side = TOP)
entry.pack(side = TOP)
button.pack(side = TOP)
text.pack(side = TOP)

# opens window
browser_window.mainloop()


