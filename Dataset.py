import pickle
import pandas as pd
import re
import numpy as np
import json
import time
import Scraping as sc

def dataset_creation(law_source, scraping = False, save_scraping = True, save_dataset = True, ref_all = True, path = "data/dataset/", data = "data/soups/"):
    soups, links = load_data(law_source, scraping, save_scraping, path=data)
    
    df = dataset_elaboration(law_source, soups, links, save_dataset, ref_all, path)
    
    return df


def load_data(law_source, scraping, save_scraping, path = "data/soups/"):
    if scraping:
        soups, links = sc.brocardi_scraper(law_source, save_scraping, path)
    else:
        with open(f"{path}{law_source}.pkl", "rb") as f:
            soups, links = zip(*pickle.load(f))
    
    print('Data loaded correctly')
    return soups, links 

    
def extract_text(body_text):
    paragraph_text = body_text.text.strip()

    # Remove [word, etc], (numbers, word, etc), \n and double space from text
    paragraph_text = re.sub(r' \[[^\]]+\]|\([^\)]+\]|\([^\)]+\)', '', paragraph_text)
    paragraph_text = re.sub(r'\[[^\)]+\]|\([^\)]+\)', '', paragraph_text)
    paragraph_text = re.sub(r'\n|  ', ' ', paragraph_text)

    return paragraph_text

def dataset_elaboration(law_source, soups, links, save_dataset, ref_all = True, path='data/'):
    data = []

    for soup, link in zip(soups, links):
        name_article = soup.find('h1', class_='hbox-header').text.strip()
        hierarchy = link.split('/')[2:-1]

        body_text = soup.find('div', class_='corpoDelTesto')
        article_text = ""

        if body_text:
            article_text = extract_text(body_text)

            if ref_all:
                # If you want to add all references
                references = [ref['href'] for ref in body_text.find_all('a', href=True)
                                if not ref['href'].startswith('/dizionario') 
                                    and not ref['href'].startswith('#nota_')
                                    ]
            else:
                # If you want to add only references to the constitution
                references = [ref['href'] for ref in body_text.find_all('a', href=True) if ref['href'].startswith('/costituzione')]

        data.append({"name": name_article, "gerarchy": hierarchy, "text": article_text, "references": references, "link": link})

    df = pd.DataFrame(data)
    print('Dataset created correctly')

    if save_dataset:
        df.to_json(f'{path}{law_source}.json', orient='records')

    return df

#-------------------------
# sources = sc.source_scraper()

with open('data/sources.txt', 'r') as f:
    law_sources = f.read().replace("'", "\"")
    
law_sources = json.loads(law_sources)

for source in law_sources:
    try:
        print(source)
        df = dataset_creation(source, scraping = False)
        print(f'{source} stored: length {len(df)}')
    except:
        print(f'Error with {source}')
        
        with open('data/errors.txt', 'a') as f:
            f.write(source + '\n')
        continue
    
