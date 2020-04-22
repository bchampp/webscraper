import requests
from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 
import time

def main():
    # url = input("Enter a full URL: ")
    print("Please enter a choice of programs: ") # List the programs available to use in main()
    print("1. Normal Catalogue")
    print("2. Test Inventory stuff")

    userChoice = int(input())
    if(userChoice == 1): # If user inputs a "1" then you can do this
        catalogueProgram()
    elif (userChoice == 2): # if user inputs a "2" then do this
        inventoryStuff()
    else: # Otherwise try again
        print("Please enter a valid choice!")
        time.sleep(.5)
        print("--------------------------------")
        main()

def catalogueProgram():
    # This is the sample function for doing what you want within the catalogue!
    # You can keep developing this if you want or use it as reference
    url = 'https://www.lcbo.com/webapp/wcs/stores/servlet/en/lcbo/beer-cider-16/lager-16023/light-lager-16023300-1/light-lager-16023300135-1'
    print("Your URL is: " + url)

    # Now we have the 'beautiful soup' version of the webpage -- Look into making this a try-catch-throw block for safety
    soup = urlToSoup(url)
    
    print("Successfully opened the webpage")
    counter = 1
    for item in soup.select("ul.list_mode li"):
        print(str(counter) + ".")
        counter += 1
        # Now we further dissect the <li> blocks that BS has found.
        #
        # there should only be one here but ".select" returns a list:
        for li in item.select("div.productChart div a"): # Prints the Name
            print(li.get_text())
        for link in item.select("div.productChart div a[href]"):
            # print(link)
            print
        for price in item.select("div.product_price"): # Prints the Price
            print(price.get_text().strip())
        for identification in item.select("div.other_details span span"): # Prints the ID
            # Two things come with this, we only want the ID so 
            temp = identification.get_text().strip()
            ID = temp.strip('\n')
            # print(identification.get_text().strip())
            if(ID != "can" and ID != "bottle"):
                print("ID: " + ID)
        print("--------------------")
    main()  

def inventoryStuff():
    url = 'https://www.lcbo.com/webapp/wcs/stores/servlet/PhysicalStoreInventoryView?langId=-1&storeId=10203&catalogId=10051&productId=59667'
    soup = urlToSoup(url)
    
    print("Successfully opened the webpage")

    # Implement your webscraper for this specific webpage!



    main() # Return to main program after! 


# This function takes in the URL as input and converts it to a "Beautiful Soup" data-type
def urlToSoup(url):
    page = uReq(url) # Open a 'page' with the URL 
    html = page.read() # Read everything (Raw HTML Code) into variable 'html'
    page.close() # Close the webpage
    return soup(html, 'html.parser') # Parse the raw HTML code with the soup() function and return


print("Welcome to a webscraping program")
main()