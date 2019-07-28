# File with all of the helper functions for the program

from urllib.request import urlopen as uReq # Import Module to get data contents from a specified URL
from bs4 import BeautifulSoup as soup # Webscraping library
from xml.dom import minidom # XML File Stuff
import xlsxwriter # Library to generate excel sheets
import helper # Import library of custom webscraping functions


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