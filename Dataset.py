import pickle
import pandas as pd
import re
import numpy as np
import json
import Scraping as sc

def dataset_creation(law_code, scraping = False, save_scraping = False, save_dataset = False, path = ""):
    soups, links = load_data(law_code, scraping, save_scraping, path)
    
    df = dataset_elaboration(soups, links, save_dataset)
    
    return df


def load_data(law_code, scraping, save_scraping = False, path = ""):
    if scraping:
        soups, links = sc.brocardi_scraper(law_code, save_scraping, path)
    else:
        with open(f"{path}{law_code}.pkl", "rb") as f:
            soups, links = zip(*pickle.load(f))
    
    print('Data loaded correctly')
    return soups, links 


def dataset_elaboration(soups, links, save_dataset):
    # create a dataframe with all articles
    df = pd.DataFrame(columns=["name", "gerarchy", "text", "references", "link"])

    for i in range(0, len(soups)):
        soup = soups[i]
        link = links[i]
        
        # Estrai il nome dell'articolo corrente
        nome_articolo = soup.find('h1', class_='hbox-header').text.strip()

        # Estrai la gerarchia di appartenenza dal corrispettivo link
        gerarchia = link.split('/')[2:-1]    

        # Estrai il testo dell'articolo
        testo_articolo = ""
        riferimenti = []  # Lista per i riferimenti trovati nel corpo del testo
        corpo_testo = soup.find('div', class_='corpoDelTesto')

        if corpo_testo:
            paragrafo_testo = corpo_testo.text.strip()
            
            # remove [word, etc], (numbers, word, etc), \n and double space from text
            paragrafo_testo = re.sub(r' \[[^\]]+\]', '', paragrafo_testo)
            paragrafo_testo = re.sub(r' \([^\)]+\)', '', paragrafo_testo)
            
            paragrafo_testo = re.sub(r'\[[^\)]+\] ', '', paragrafo_testo)
            paragrafo_testo = re.sub(r'\([^\)]+\) ', '', paragrafo_testo)
            
            paragrafo_testo = re.sub(r'\[[^\)]+\]', '', paragrafo_testo)
            paragrafo_testo = re.sub(r'\([^\)]+\)', '', paragrafo_testo)
            
            paragrafo_testo = re.sub(r'\n', ' ', paragrafo_testo)
            paragrafo_testo = re.sub(r'  ', ' ', paragrafo_testo)
            
            # If you want to add only references to the constitution
            # for ref in corpo_testo.find_all('a', href=True):
            #     if ref['href'].startswith('/costituzione'): 
            #         riferimenti.append(ref['href'])
            
            # If you want to add all references
            for ref in corpo_testo.find_all('a', href=True):
                if ref['href'].startswith('/dizionario') or ref['href'].startswith('#nota_'):
                    continue
                else:    
                    riferimenti.append(ref['href'])

            # Aggiungi il testo del paragrafo al testo dell'articolo
            testo_articolo += paragrafo_testo

        df = pd.concat([df, pd.DataFrame([{"name": nome_articolo, "gerarchy": gerarchia, "text": testo_articolo, "references": riferimenti, "link":link}])], ignore_index=True)
    
    print('Dataset created correctly')
    if save_dataset: 
        df.to_json('costituzione.json', orient='records')
        return df
    else:
        return df

law_code = "costituzione"
df = dataset_creation(law_code, scraping = True, save_scraping = True, save_dataset = True, path = "")

print(df)
