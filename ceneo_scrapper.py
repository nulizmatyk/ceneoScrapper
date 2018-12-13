import urllib.request
from tkinter import *
from bs4 import BeautifulSoup
import json
from time import sleep 

#Adding a User-Agent String in the request to prevent getting blocked while scraping 

user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
numberOfPage = 1
extracted_data = []
# function to check if there is more opinions
def checkIFMoreExist(page):
    more = []
    more = page.find_all("li",attrs={'class': 'page-arrow arrow-next'})
    if len(more) != 0 :
        return True
    else :
        return False

# function which is run by button and doing all process of data extraction
def go():
    global numberOfPage
    
    # do loop with every page with reviews
    url = 'https://www.ceneo.pl/' + entry.get() + '/opinie-' + str(numberOfPage)
    numberOfPage += 1

    request = urllib.request.Request(url, headers={'User-Agent': user_agent})

    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    #First lets get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("div",attrs={'class':'screening-wrapper' })
        
    # all reviews on site
    reviews = main_table.find_all("li",attrs={'class': 'review-box js_product-review'})
        
    # loop which takes every review from pool
    for a_tag in reviews:
            
        # score 
        # extracted_data.append(a_tag.find("span",attrs={'class':'review-score-count'}).text)
        score = a_tag.find("span",attrs={'class':'review-score-count'}).text
        nameOfReviewer = a_tag.find("div",attrs={'class':'reviewer-name-line'}).text
        recomendOrNot = a_tag.find("em",attrs={'class': ['product-recommended', 'product-not-recommended']})

        # check if field with recomendation isn't empty beacuse it can be left blank and then, there is no em with this class
        if recomendOrNot != None and recomendOrNot != 'null':
            recomendOrNot = recomendOrNot.text
        else:
            recomendOrNot = ''
        comment = a_tag.find("p",attrs={'class':'product-review-body'}).text
        text.insert(1.0, nameOfReviewer + ' - ' + recomendOrNot + ' - ' + comment + ' - ' + score )
        extracted_data.append(nameOfReviewer)
        text.insert(1.0, '')

    # jest tests
    print(len(extracted_data))
    print(url)
    print(checkIFMoreExist(main_table))
    # text.insert(1.0, extracted_data)
    if checkIFMoreExist(main_table) == True :
        go()



# build gui window to let user put url to scrap
browser_window = Tk()
# szerokosc na wysokosc ale okna nie pola tesktowego
browser_window.geometry("1000x1000")
browser_window.title('CENEO SCRAPPER')
label = Label(browser_window, text ='Enter product Id: ')
entry = Entry(browser_window)
entry.insert(END, "35379099")
button = Button(browser_window, text='go', command= go)
text = Text(browser_window, height= 100, width = 500)

# insert parts of gui to in window
label.pack(side = TOP)
entry.pack(side = TOP)
button.pack(side = TOP)
text.pack(side = TOP)

# opens window
browser_window.mainloop()


