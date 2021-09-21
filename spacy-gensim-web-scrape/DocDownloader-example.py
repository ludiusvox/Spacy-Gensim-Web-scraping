# DocDownloader-example.py
# Collin Lynch and Travis Martin
# 9/8/2021

# The DocDownloader package provides a simple iterative download
# of files via the requests package and storage of the files as
# processed docs via spacey.  It presumes that we are using a
# pretrained spacey package that will provide the basic loading
# and processing tasks.
#
# Expand this code for your own version of the assignment.


# Imports
# ---------------------------------------------

import spacy
import requests
from bs4 import BeautifulSoup



# Core Code.
# ---------------------------------------------
"""
input: spacy model, url, storage dirctory, n = iterator variable
1. grab the url and download the page
2. convert the webpage to being text readable
3. pass the text through the spacy model
4. create the name of the outfile using the n passed in
5. save the file to disk
output: none
"""
def download_and_save(Model, URL, StorageDir, n):    
    # First download the URL as a request.
    print("Downloading Doc: {}".format(URL))
    Req = requests.get(URL)
    
    # Now convert it to a doc.
    print("  converting...")
    SoupText = BeautifulSoup(Req.text, features="lxml")
    PageText = SoupText.get_text()
    FileDoc = Model(PageText)

    # Get a unique file/directory name.
    outfile = StorageDir + str(n)    
    
    # And finally save it.
    print("  saving...")
        
    #save_file(FileDoc, FileDir)
    FileDoc.to_disk(outfile)            
                
    print("  done.")
    return
    


"""
input: spacy model, urlfile, starage directory
1. open the url file containing the url's to be processes
2. pass each url to the download and save function
3. read the next url
4. close the file and exit
output: none
"""
def process_url_file(SpacyModel, UrlFile, StorageDir):
    
    n = 0
    with open(UrlFile, 'r') as InFile:
        website = InFile.readline()[:-1]
        while website:
            download_and_save(SpacyModel, website, StorageDir, n)
            
            website = InFile.readline()[:-1]
            n+=1
            
        InFile.close()
    return




if __name__ == "__main__":

    #initial declarations
    URL_File = 'infile.txt'
    Directory = '/home/aaronl/PycharmProjects/pythonProject/start/save'
    
    #load the spacy model
    Model = spacy.load("en_core_web_sm")
    
    #process the urls
    process_url_file(Model, URL_File, Directory)
    
    