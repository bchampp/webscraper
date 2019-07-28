from urllib.request import urlopen as uReq # Import Module to get data contents from a specified URL
from bs4 import BeautifulSoup as soup # Webscraping library
from xml.dom import minidom # XML File Stuff
import xlsxwriter # Library to generate excel sheets
import helper as func # Import library of custom webscraping functions
from datetime import date

# TODO
# Move functions to various helper files with good structure 
# Add doxy commenting for functions
# Build routines for the rest of the beers
# Fill in req'd file paths for functions
# 
def main():
    url = openURLs()
    soup = func.URLToSoup(url) # Convert to BeautifuLSoup
    thornBuryVillage(soup) # Thornbury Village Routine

def thornBuryVillage(soup):
    script = soup.find_all('script') # Find all the script tags
    inventoryScript = script[-1] # The info we want is the last element, access with -1
    func.saveTextToFile(inventoryScript) # Save it to a text file
    with open('test.html') as file: # Open the text file
        text = file.read()
    result = text.split('var') # Split the file by 'var', all of our contents will be in the first element
    
    listOfStores = result[1].split('{') # Now we split this var into the list of stores with "{"
    #print(listOfStores)

    cleanListOfStores = func.cleanStores(listOfStores)
    # print(cleanListOfStores)
    today = date.today()
    workbookName = str(today) + '.xlsx'

    workbook = xlsxwriter.Workbook(workbookName)
    worksheet = workbook.add_worksheet('Thornbury Village No.26 Pilsner')
    worksheet.write('A1', 'City')
    worksheet.write('B1', 'Inventory')
    worksheet.write('C1', 'Store ID')
    storeEntries = getStoreEntries(cleanListOfStores)
    cityCellName = ''
    cityCellContents = ''
    cityCellCounter = 1
    inventoryCellName = ''
    inventoryCellContents = ''
    inventoryCellCounter = 1
    IDCounter = 1
    IDName = ''
    IDContents = ''

    for store in storeEntries:
        test = store.split(": ") 
        #print(test)
        for string in range(0, len(test) -1):
            #print(test[string].strip() + ": " + test[string+1].strip())
            if(test[string].strip() == 'city'):
                cityCellCounter += 1
                cityCellName = 'A' + str(cityCellCounter)
                cityCellContents = test[string+1].strip()
                worksheet.write(cityCellName, cityCellContents)
                print("City: " + test[string+1].strip())

            elif(test[string].strip() == 'inventory'):
                blah = test[string+1].split(" " )
                blah = blah[0].replace("Math.floor(" "", "")
                blah = blah.lstrip('\"')
                test = blah.split('"')
                print("Inventory: " + test[0])
                inventoryCellContents = str(test[0])
                inventoryCellCounter += 1
                inventoryCellName = 'B' + str(inventoryCellCounter)
                worksheet.write(inventoryCellName, inventoryCellContents)
                print("--------------")
                #print("inventory: " + test[string+1].strip().replace("inventoryMath.floor", ""))
            elif(test[string].strip() == 'uniqueId'):
                IDContents = test[string+1].strip()
                IDContent = IDContents.strip('"')
                IDContents = IDContent
                IDCounter += 1
                IDName = 'C' + str(IDCounter)
                worksheet.write(IDName, IDContents)
                print("unique ID: " + test[string+1].strip())
    workbook.close()
    
def openURLs():
    f = open("resources/urlList.txt", "r")
    url = f.read()
    f.close()
    return url


def getStoreEntries(storeList):
    entries = []
    for store in storeList:
        #print(store)
        for a in store:
            new = a.split(",")
            #print(new)
            entries.append(new)
    # print(entries)
    cleanEntries = []
    for store in entries:
        #print(store)
        for entry in store:
            #print(entry)
            cleanEntries.append(entry)

    return cleanEntries

def URLToSoup(url):
    page = uReq(url) # Open a 'page' with the URL 
    html = page.read() # Read everything (Raw HTML Code) into variable 'html'
    page.close() # Close the webpage
    return soup(html, 'html.parser') # Parse the raw HTML code with the soup() function and return

def saveTextToFile(text):
    filename = "test"
    # filename = input("Filename: ")
    filename += ".html"
    file = open(filename, "w+")
    file.write(str(text))
    file.close()

def saveHTMLToFile(url):
    soup = URLToSoup(url)
    filename = input("Filename: ")
    filename += ".html"
    file = open(filename, "w+")
    file.write(soup.prettify())
    file.close()


def read_URL_list():
    list = {}
    return list

def cleanStores(listOfStores):
#print(listOfStores)
    cleanedList = []
    for entry in listOfStores:
        newItem = entry.replace("\n", "")
        newItem = newItem.replace("\t", "")
        cleanedList.append(newItem)

    cleanedList = cleanedList[1:]
    # print(cleanedList)

    storeList = []
    for store in cleanedList:
        newItem = store.split('}')
        storeList.append(newItem)
    
    return storeList


main()

