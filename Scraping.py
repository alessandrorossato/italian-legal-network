import time
import pickle
from bs4 import BeautifulSoup
from urllib.request import urlopen

def brocardi_scraper(law_code, save_scraping=True, path = ''):
    print('Scraping started')
    url_root = "https://www.brocardi.it/"
    
    books = books_scraper(url_root, law_code)
        
    articles = articles_scraper(url_root, law_code, books)
    
    soups = soup_articles(url_root, articles)
    
    if save_scraping:
        store_soups(soups, articles, law_code, path)
        print("soup and articles are stored and ready to use")
    else:
        print("soups and articles not stored, but returned and ready to use")
    return soups, articles
    
    
def books_scraper(url_root, law_code):  
    page = urlopen(url_root + law_code + "/")
    html = page.read()
    soup = BeautifulSoup(html, "html.parser")
    links = [link.get("href") for link in soup.find_all("a") if link.get("href") is not None]
    books = [link for link in links if link.startswith(f"/{law_code}/l") or link.startswith(f"/{law_code}/p") and not link.endswith("o/")]
    
    print('Books links scraped')
    return books 
    
    
def articles_scraper(url_root, law_code, books):
    articles = []
    
    for book in books:
        time.sleep(0.5)
        html = urlopen(url_root + book).read()
        soup = BeautifulSoup(html, "html.parser")
        links = [link.get("href") for link in soup.find_all("a") if link.get("href") and link.get("href").endswith("html")]
        articles.append(links)

    articles = filter_articles(law_code, articles)
    
    print('Articles links scraped')
    return articles
     
        
def filter_articles(law_code, articles):
    filtered_articles = []
    dupes = set()
    
    for book in articles:
        for link in book:
            if link.startswith(f"/{law_code}") and link not in filtered_articles:
                filtered_articles.append(link)
            else:
                dupes.add(link)
                
    return filtered_articles


def soup_articles(url_root, articles):
    soups = []
    
    for article in articles:
        time.sleep(0.5)
        html = urlopen(url_root + article).read()
        soups.append(BeautifulSoup(html, "html.parser")) 
    
    print('Articles soups scraped')
    return soups


def store_soups(soups, articles, law_code, path = ''): 
    
    with open(f"{path}{law_code}.pkl", "wb") as f:
        pickle.dump(zip(soups, articles), f)
    print(f'{path}{law_code} stored')

# -------
# soups = brocardi_scraper("costituzione", False)  # codice-di-procedura-civile
