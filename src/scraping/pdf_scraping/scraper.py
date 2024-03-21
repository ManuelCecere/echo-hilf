import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
from tqdm import tqdm

pdf_scraper_folder = os.path.dirname(os.path.abspath(__file__))
pdfLists_folder = pdf_scraper_folder + '/PDFS_LISTS/'
file_path = 'biodegradable polymers list 29 nov.csv' 
path = pdfLists_folder + file_path 

### read in csv (adjust if you hav a txt file) ###
df = pd.read_csv(path)
links = df['PaperLink'].to_list()

### setting up selenium ###
options = webdriver.ChromeOptions()
service = Service()
chrome_prefs = {
    "download.default_directory": pdf_scraper_folder + "/" + "DOWNLOADED_PDFS", # Add children folders if needed
    "download.prompt_for_download": False, #To auto download the file - ON FALSE IT WORKS
    "download.directory_upgrade": True, # ON TRUE WORKS
    "plugins.always_open_pdf_externally": True, #It will not show PDF directly in chrome - ON TRUE WORKS
}
options.add_experimental_option('prefs', chrome_prefs)
options.add_argument('--disable-extensions')
options.add_argument('--disable-pdf-extensions')

driver = webdriver.Chrome(
    service=service,
    options=options
)


if __name__ == '__main__':
    for i in tqdm(range(len(links))):
        try:
            driver.get(links[i])
        except Exception as e:
            print("Error on link:", links[i])
        time.sleep(5)
