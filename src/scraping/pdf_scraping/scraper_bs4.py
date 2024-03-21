import requests
from bs4 import BeautifulSoup
import os
import pandas as pd
from tqdm import tqdm
import pickle


def download_pdf(url, directory="pdf_new"):
    """ Downloads a PDF file from a given URL """
    try:
        response = requests.get(url)
        filename = os.path.join(directory, url.split('/')[-1])
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f'Downloaded {filename}')
        return True, filename
    except Exception as e:
        print(f"Error downloading {url}: {e}")
        return False, None


class Scraper:
    """ The scraper for the PDFs using Beautiful Soup """

    def __init__(self):
        self.links = []
        self.df = pd.DataFrame()

    def list_creator(self, name):
        ''' Generates a list of links given a pickle file '''
        with open(name, 'rb') as file:
            self.links = pickle.load(file)

    def create_log_df(self):
        """ Creates a DataFrame to log download status """
        self.df = pd.DataFrame(self.links, columns=['link'])
        self.df['downloaded'] = False
        self.df['file_name'] = ''

    def scrape(self, file_name):
        """ Main function to scrape PDFs """
        self.list_creator(file_name)
        self.create_log_df()

        if not os.path.exists('pdf_new'):
            os.makedirs('pdf_new')

        for i, row in tqdm(self.df.iterrows(), total=self.df.shape[0]):
            try:
                # Assume each link directly points to a PDF file
                success, filename = download_pdf(row['link'])
                if success:
                    self.df.loc[i, 'downloaded'] = True
                    self.df.loc[i, 'file_name'] = filename
                if i % 50 == 0:
                    self.export_df(file_name='down_log_additional.csv')
            except Exception as e:
                print(f"Error: {e} on ", row['link'])

    def export_df(self, file_name):
        """ Exports the DataFrame to a CSV file """
        self.df.to_csv(file_name, index=False)


if __name__ == '__main__':
    scraper = Scraper()
    scraper.scrape(file_name='allPDF.pkl')
    scraper.export_df(file_name='down_log_additional.csv')
