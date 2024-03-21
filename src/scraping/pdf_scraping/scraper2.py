from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time
import os
import pandas as pd
from tqdm import tqdm
import pickle


class Scraper:
    ''' The scraper for the 5000 pdfs '''

    def __init__(self):
        pass

    def list_creator(self, name):
        'generates a list of links given a txt file'
        # Open the pickle file in binary read mode
        with open(name, 'rb') as file:
            # Load the pickle
            self.links = pickle.load(file)

    def removin_line_terminator(self):
        self.links = [link[:-1] for link in self.links if link.endswith('\n')]

    def create_log_df(self):
        self.df = pd.DataFrame(self.links, columns=['link'])
        self.df['downloaded'] = False
        self.df['file_name'] = ''

    def update_directory_stats(self):
        self.original_listdir = os.listdir('pdf_new')
        self.len_orginal_listdir = len(os.listdir('pdf_new'))

        return self.original_listdir, self.len_orginal_listdir

    def instantiate_driver(self):
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')  # Run Chrome in headless mode.
        options.add_argument('--no-sandbox')  # Bypass OS security model.
        options.add_argument('--disable-dev-shm-usage')  # Overcome limited resource problems.
        # options.add_argument('start-maximized')  # Open Browser in maximized mode.
        # options.add_argument('disable-infobars')  # Disabling infobars.
        options.add_argument('--disable-extensions')  # Disabling extensions.
        options.add_argument('--remote-debugging-port=9222')  # Specify a debugging port.

        # options = webdriver.ChromeOptions()
        options.add_experimental_option('prefs', {
            "download.default_directory": "pdf_new",
            # change default directory for downloads
            "download.prompt_for_download": False,  # to auto download the file
            "download.directory_upgrade": True,
            "plugins.always_open_pdf_externally": True})  # it will not show pdf directly in chrome})

        self.driver = webdriver.Chrome(
            service=Service(ChromeDriverManager().install()),
            options=options)

    def change_in_dir(self):
        return len(os.listdir('pdf_new')) != self.len_orginal_listdir

    def check_file_downloaded(self, i):
        if self.change_in_dir():
            print('ók')
            self.df.loc[i, 'downloaded'] = True
            news = [item for item in os.listdir('pdf_new') if item not in self.original_listdir]
            self.df.loc[i, 'file_name'] = news[0]
            self.update_directory_stats()
            return True
        else:
            print('no change')
            return False

    def scrape(self, file_name):
        """main function"""
        self.list_creator(name=file_name)
        # self.removin_line_terminator()
        self.create_log_df()
        self.update_directory_stats()
        self.instantiate_driver()
        for i, row in tqdm(self.df.iterrows()):
            try:

                t0 = time.time()
                self.driver.get(row.link)
                time.sleep(2)
                while not self.check_file_downloaded(i) and time.time() - t0 < 60:
                    time.sleep(2)

            except Exception as e:
                print(f"Error: {e} on ", row.link)

        self.export_df(file_name)

    def export_df(self, file_name):
        self.df.to_csv(file_name)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape(file_name='allPDF.pkl')
    scraper.export_df(file_name='down_log_additional.csv')
