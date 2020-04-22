from urllib.request import urlopen as uReq # Import Module to get data contents from a specified URL
from bs4 import BeautifulSoup as soup # Webscraping library
from xml.dom import minidom # XML File Stuff
import xlsxwriter # Library to generate excel sheets
# import helper as func # Import library of custom webscraping functions
from datetime import date

def main():
    workbook = xlsxwriter.Workbook("resources/logs/" + str(getWorkbookName())) # Create New Workbook with Datestamped Name

    urlList = textToList('resources/urlList.txt') # Open urlList.txt file and create a list of the URLs
    nameList = textToList('resources/sheetNames.txt') # Open sheetNames.txt file and create a list of names
    counter = 0 # Counter for the URL Loop

    for url in urlList: # Loop through all the URL's
        soup = URLToSoup(url) # Convert to BeautifuLSoup
        name = str(nameList[counter])
        print("Starting " + name)
        worksheet = workbook.add_worksheet(name)
        scrapeToWorksheet(soup, worksheet) # Thornbury Village Routine
        print("Completed " + name)
        counter += 1
        print()
    workbook.close()
    print("Program finished succesfully!")

def scrapeToWorksheet(soup, worksheet):
    script = soup.find_all('script') # Find all the script tags
    inventoryScript = script[-1] # The info we want is the last element, access with -1
    saveTextToFile(inventoryScript) # Save it to a text file
    with open('test.html') as file: # Open the text file
        text = file.read()
    result = text.split('var') # Split the file by 'var', all of our contents will be in the first element
    
    listOfStores = result[1].split('{') # Now we split this var into the list of stores with "{"
    
    cleanListOfStores = cleanStores(listOfStores)
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
                cityCellContents = cityCellContents.strip('"')
                cityCellContents = cityCellContents.lower()
                cityCellContents = cityCellContents.capitalize()
                worksheet.write(cityCellName, cityCellContents)
                #print("City: " + test[string+1].strip())

            elif(test[string].strip() == 'inventory'):
                blah = test[string+1].split(" " )
                blah = blah[0].replace("Math.floor(" "", "")
                blah = blah.lstrip('\"')
                test = blah.split('"')
                #print("Inventory: " + test[0])
                inventoryCellContents = str(test[0])
                inventoryCellCounter += 1
                inventoryCellName = 'B' + str(inventoryCellCounter)
                worksheet.write(inventoryCellName, inventoryCellContents)
                # print("--------------")
                #print("inventory: " + test[string+1].strip().replace("inventoryMath.floor", ""))
            elif(test[string].strip() == 'uniqueId'):
                IDContents = test[string+1].strip()
                IDContent = IDContents.strip('"')
                IDContents = IDContent
                IDCounter += 1
                IDName = 'C' + str(IDCounter)
                worksheet.write(IDName, IDContents)
                #print("unique ID: " + test[string+1].strip())
 
def textToList(filename):
    with open(filename, 'r') as file:
        urlList = file.readlines()
    file.close()
    return urlList

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

def getWorkbookName():
    today = date.today()
    workbookName = str(today) + '.xlsx'
    return workbookName

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

def cleanStores(listOfStores):
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

