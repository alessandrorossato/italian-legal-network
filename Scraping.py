import time
import pickle
from bs4 import BeautifulSoup
from urllib.request import urlopen

def brocardi_scraper(law_source, save_scraping=True, path = 'data/soups/'):
    print(f'Scraping {law_source} started')
    url_root = "https://www.brocardi.it/"
    
    books = books_scraper(url_root, law_source)
        
    articles = articles_scraper(url_root, law_source, books)
    
    soups, missing = soup_articles(url_root, articles)
        
    if save_scraping:
        store_soups(soups, missing, articles, law_source, path)
        # print("soup and articles are stored and ready to use")
    else:
        pass
        # print("soups and articles not stored, but returned and ready to use")
    return soups, articles
    
    
def books_scraper(url_root, law_source):  
    html = urlopen(url_root + law_source + "/").read()
    soup = BeautifulSoup(html, "html.parser")
    filt_soup = soup.find("div", {"class": "section_content content-box content-ext-guide"})
    books = [link.get("href") for link in filt_soup.find_all("a") if link.get("href") is not None]
    
    print('Books links scraped')
    return books 
    
    
def articles_scraper(url_root, law_source, books):
    articles = []
    
    for book in books:
        time.sleep(0.5)
        html = urlopen(url_root + book).read()
        soup = BeautifulSoup(html, "html.parser")
        # filt_soup = soup.find("div", {"class": "section_content content-box content-ext-guide"})
        links = [link.get("href") for link in soup.find_all("a") if link.get("href") and link.get("href").endswith("html")]
        articles.append(links)

    articles = filter_articles(law_source, articles)
    
    print('Articles links scraped')
    return articles
     
        
def filter_articles(law_source, articles):
    filtered_articles = []
    dupes = set()
    
    for book in articles:
        for link in book:
            if link.startswith(f"/{law_source}") and link not in filtered_articles:
                filtered_articles.append(link)
            else:
                dupes.add(link)
                
    return filtered_articles


def soup_articles(url_root, articles): # da migliorare
    soups = []
    missing = []
    
    for article in articles:
        try:
            html = urlopen(url_root + article).read()
        except:
            print(f'Article {article} not found')
            missing.append(article)
            
        time.sleep(0.5)
        soups.append(BeautifulSoup(html, "html.parser")) 
    
    print('Articles soups scraped')
    return soups, missing


def store_soups(soups, missing, articles, law_source, path = ''): 
    
    with open(f"{path}{law_source}.pkl", "wb") as f:
        pickle.dump(zip(soups, articles), f)
    print(f'{law_source} stored')
    
    if len(missing) > 0:
        with open(f"{path}{law_source}_missing.txt", "w") as m:
            m.write(str(missing))
    

def source_scraper(url = 'https://www.brocardi.it/fonti.html', save = True, path = 'data/'):
    html = urlopen(url).read()
    soup = BeautifulSoup(html, "html.parser")
    filt_soup = soup.find("div", {"class": "content-box content-ext-guide"})
    sources = [link.get("href") for link in filt_soup.find_all("a") if link.get("href") is not None]
    sources = [source[1:-1] for source in sources if source.startswith("/")]
    
    if save:
        with open(f"{path}sources.txt", "w") as f:
            f.write(str(sources))
        print('sources stored')
        
    return sources
