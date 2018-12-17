import json
import urllib.request
from tkinter import *
from bs4 import BeautifulSoup
import json
import MySQLdb
# ##########################################################################################
#Save class's base data to the database
# Open database connection
HOST = "localhost"
USERNAME = "root"
PASSWORD = ""
DATABASE = "testowa"
db = MySQLdb.connect(HOST, USERNAME, PASSWORD, DATABASE, use_unicode=True, charset="utf8")
url = ""
idOfProduct = ""
nameOfProduct = ""
listOfOpinions = []
extractedData = {}
extractedData['opinions'] = []
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'
numberOfPage = 1
data = 1
reviews = []
class Rewiew:
  def __init__(self, name, recomendOrNot, comment, score, nameOfProduct, idOfProduct ):
    self.name = name
    self.recomendOrNot = recomendOrNot
    self.comment = comment
    self.score = score
    self.nameOfProduct = nameOfProduct
    self.idOfProduct = idOfProduct

def clearDataBase():
    sql = "TRUNCATE TABLE rewiewers"
    cursor = db.cursor()
    cursor.execute(sql)
    # Commit your changes in the database
    db.commit()
    infoText.delete('1.0',END)
    infoText.insert(1.0, "Z bazy danych usunięto wszystkie rekordy")

def processETL():
    extractData()
    transform()
    saveDatatoDataBase()
    
    
def saveDatatoDataBase():
    global numberOfPage
    global idOfProduct 
    global nameOfProduct 
    sql = "DELETE FROM rewiewers WHERE id_of_product_on_website = %s"
    id = (idOfProduct, )
    cursor = db.cursor()
    cursor.execute(sql, id)
    db.commit()
    for opinion in listOfOpinions:
        cursor = db.cursor()
        sql = "INSERT INTO rewiewers(id_of_product_on_website, name_of_product, name_of_reviewer, recomended_or_not, comment, score) VALUES ('{}','{}','{}', '{}', '{}', '{}')".format(idOfProduct, nameOfProduct, opinion.name , opinion.recomendOrNot , opinion.comment, opinion.score)
            
        # Prepare SQL query to INSERT a record into the database.
        try:
            # Execute the SQL command
            cursor.execute(sql)
            # Commit your changes in the database
            db.commit()
        except:
            print("catch")
            # Rollback in case there is any error
            db.rollback()
            # #get the just inserted class id
    komunikat = 'Do bazy danych zapisano ' + str(len(listOfOpinions))  + ' rekordy/ów'
    infoText.delete('1.0',END)
    infoText.insert(1.0, komunikat)
    buttonETL['state'] = 'normal'
    buttonExtract['state'] = 'normal'
    buttonTransform['state'] = 'disable'
    buttonSave['state'] = 'disable'
    buttonExport['state'] = 'disable'
    reviews.clear()
    listOfOpinions.clear()
    numberOfPage = 1
    nameOfProduct = ""
    idOfProduct = ""
    
      
def extractData():
    global numberOfPage
    global idOfProduct 
    global nameOfProduct 
    text.delete('1.0',END)
    url = 'https://www.ceneo.pl/' + entry.get() + '/opinie-' + str(numberOfPage)
    idOfProduct = entry.get()
    numberOfPage += 1
    rewiewsForOneProduct = []
    request = urllib.request.Request(url, headers={'User-Agent': user_agent})

    html = urllib.request.urlopen(request).read()
    soup = BeautifulSoup(html,'html.parser')

    #First lets get the HTML of the table called site Table where all the links are displayed
    main_table = soup.find("div",attrs={'class':'screening-wrapper' })
    nameOfProduct = main_table.find("h2",attrs={'class': 'section-title with-context header-curl'}).text.replace('- Opinie', '')
    # all reviews on site
    reviews.extend(main_table.find_all("li",attrs={'class': 'review-box js_product-review'}))

    if checkIFMoreExist(main_table) == True :
        extractData()
    else:
        # reviews.extend(rewiewsForOneProduct)
        komunikat = 'Ze strony sciagnieto ' + str(len(reviews))  + ' opinii'
        infoText.delete('1.0',END)
        infoText.insert(1.0, komunikat)
        buttonTransform['state'] = 'normal'     
        buttonExtract['state'] = 'disable'
        buttonETL['state'] = 'disable'

    #    saveDatatoDataBase()
#Adding a User-Agent String in the request to prevent getting blocked while scraping 
# user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 Safari/537.36'

# function to check if there is more opinions
def checkIFMoreExist(page):
    more = []
    more = page.find_all("li",attrs={'class': 'page-arrow arrow-next'})
    if len(more) != 0 :
        return True
    else :
        return False

# function which transform data
def transform():
    for a_tag in reviews:
        score = a_tag.find("span",attrs={'class':'review-score-count'}).text.replace("'","`") 
        nameOfReviewer = a_tag.find("div",attrs={'class':'reviewer-name-line'}).text.replace("'","`") 
        recomendOrNot = a_tag.find("em",attrs={'class': ['product-recommended', 'product-not-recommended']})

        # check if field with recomendation isn't empty beacuse it can be left blank and then, there is no em with this class
        if recomendOrNot != None and recomendOrNot != 'null':
            recomendOrNot = recomendOrNot.text.replace("'","`") 
        else:
            recomendOrNot = ''
        # there is a need to replace character ' with blank space because of sql
        comment = a_tag.find("p",attrs={'class':'product-review-body'}).text.replace("'","`") 
        text.insert(1.0,nameOfProduct + ' - ' + nameOfReviewer + ' - ' + recomendOrNot + ' - ' + comment + ' - ' + score )
        text.insert(1.0, '')
        rewiew = Rewiew(nameOfReviewer, recomendOrNot, comment, score, nameOfProduct, idOfProduct)
        listOfOpinions.append(rewiew)
        extractedData['opinions'].append({  
        'nameOfProduct': nameOfProduct,
        'idOfProduct': idOfProduct,
        'nameOfReviewer': nameOfReviewer,
        'recomendOrNot': recomendOrNot,
        'comment': comment,
        'score': score
        })
    komunikat = 'Przetransformowano ' + str(len(listOfOpinions)) + ' opinii'
    infoText.delete('1.0',END)
    infoText.insert(1.0, komunikat)    
    buttonSave['state'] = 'normal'
    buttonExport['state'] = 'normal'
    buttonTransform['state'] = 'disable'

   

    # jest test
    # saveDatatoDataBase()

def exportDatatoJson():
    with open('ceneo.json', 'w') as outfile:
        json.dump(extractedData, outfile, indent=4)
    infoText.delete('1.0',END)
    infoText.insert(1.0, "dane zostały pomyślnie wyeksportowane")    
    



# build gui window to let user put url to scrap
browser_window = Tk()
# szerokosc na wysokosc ale okna nie pola tesktowego
browser_window.geometry("1000x1000")
browser_window.title('CENEO SCRAPPER')
label = Label(browser_window, text ='Enter product Id: ')
entry = Entry(browser_window)
entry.insert(END, "")
buttonExtract = Button(browser_window, text='Extract Data', command= extractData)
buttonTransform = Button(browser_window, text='Transform Data', command= transform, state=DISABLED)
buttonSave = Button(browser_window, text='Save Data', command= saveDatatoDataBase, state=DISABLED)
buttonETL = Button(browser_window, text='ETL Process', command= processETL)
buttonClear = Button(browser_window, text='Clear DataBase', command= clearDataBase)
buttonExport = Button(browser_window, text='ExportData', command= exportDatatoJson, state=DISABLED)
text = Text(browser_window, height= 100, width = 500)
infoText =  Text(browser_window, height= 2, width = 30)

# insert parts of gui to in window
label.pack(side = TOP)
entry.pack(side = TOP)
buttonExtract.pack(side = TOP, fill=BOTH, expand=1)
buttonTransform.pack(side = TOP, fill=BOTH, expand=1)
buttonSave.pack(side = TOP, fill=BOTH, expand=1)
buttonETL.pack(side = TOP, fill=BOTH, expand=1)
buttonClear.pack(side = TOP, fill=BOTH, expand=1)
buttonExport.pack(side = TOP, fill=BOTH, expand=1)
infoText.pack(side = TOP)
text.pack(side = TOP)


# opens window
browser_window.mainloop()


