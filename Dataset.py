import pickle
import pandas as pd
import re
import numpy as np
import json
import time
import Scraping as sc

def dataset_loop(loop = True, sources_load = True, df_load = True, save = True, path = "data/", scraping = False, save_scraping = True, save_dataset = True, ref_all = True):
    if loop:
        if sources_load:
            with open(f'{path}sources.txt', 'r') as f:
                law_sources = f.read().replace("'", "\"")
            law_sources = json.loads(law_sources)
        else:
            law_sources = sc.source_scraper()

        df = pd.DataFrame()

        for source in law_sources:
            try:
                if df_load: # da migliorare
                    df_json = pd.read_json(f'{path}dataset/{source}.json')
                    print(f'{source} loaded: length {len(df_json)}')
                    df = pd.concat([df, df_json], ignore_index=True)
                else:
                    df_json = dataset_creation(source, scraping, save_scraping, save_dataset, ref_all)
                    print(f'{source} stored: length {len(df_json)}')
                    df = df.append(df_json, ignore_index=True)
            except:
                print(f'Error with {source}')
                with open('data/errors.txt', 'a') as f:
                    f.write(source + '\n')
                continue
        
        if save:
            df.to_json(f'{path}all.json', orient='records')
    else:
        df = pd.read_json(f'{path}all.json')

    return df


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


def dataset_elaboration(law_source, soups, links, save_dataset, ref_all = True, path='data/'):
    data = []

    for soup, link in zip(soups, links):
        name_article = soup.find('h1', class_='hbox-header').text.strip()
        hierarchy = link.split('/')[2:-1]

        body_text = soup.find('div', class_='corpoDelTesto')
        article_text = ""

        if body_text:
            article_text, references = extract_ref(law_source, body_text, ref_all)

        data.append({"name": name_article, "gerarchy": hierarchy, "text": article_text, "references": references, "link": link})

    df = pd.DataFrame(data)
    print('Dataset created correctly')

    if save_dataset:
        df.to_json(f'{path}{law_source}.json', orient='records')

    return df    

    
def extract_ref(law_source, body_text, ref_all = True):
    paragraph_text = body_text.text.strip()

    # Remove [word, etc], (numbers, word, etc), \n and double space from text
    paragraph_text = re.sub(r' \[[^\]]+\]|\([^\)]+\]|\([^\)]+\)', '', paragraph_text)
    paragraph_text = re.sub(r'\[[^\)]+\]|\([^\)]+\)', '', paragraph_text)
    paragraph_text = re.sub(r'\n|  ', ' ', paragraph_text)
    
    if ref_all:
        # If you want to add all references
        references = [ref['href'] for ref in body_text.find_all('a', href=True)
                        if not ref['href'].startswith('/dizionario') 
                            and not ref['href'].startswith('#nota_')]
    else:
        # If you want to add only references to the law_code
        references = [ref['href'] for ref in body_text.find_all('a', href=True) if ref['href'].startswith(f'/{law_source}/')]

    return paragraph_text, references
