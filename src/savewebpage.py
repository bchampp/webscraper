from urllib.request import urlopen as uReq
from bs4 import BeautifulSoup as soup 

# Use this file to convert your webpage into .html so that you can read it and plan your webscraping -- Easier to use than the inspect tool!
def main():
    # Helper file to save nice html code to file 

    url = input("Enter url: ")
    soup = urlToSoup(url)

    filename = input("Filename: ")
    filename += ".html"
    file = open(filename, "w+")
    file.write(soup.prettify())
    file.close()

    # This function takes in the URL as input and converts it to a "Beautiful Soup" data-type
def urlToSoup(url):
    page = uReq(url) # Open a 'page' with the URL 
    html = page.read() # Read everything (Raw HTML Code) into variable 'html'
    page.close() # Close the webpage
    return soup(html, 'html.parser') # Parse the raw HTML code with the soup() function and return

main()