import requests
import lxml.html
import urllib.request ##get_page
from bs4 import BeautifulSoup
import re
from pymongo import MongoClient

client = MongoClient()
db = client['database']
collection = db['collection']


def url_conv_ord(url):
    list_Sord = []
    for i in url:
        str_con = str(ord(i))
        list_Sord.append(str_con)
    str_num = '/'.join(list_Sord)
    return str_num
    
def all_link_in_url(url):
    links = []
    try:
        req = requests.get(url)
        content = lxml.html.fromstring(req.text)
        pages = content.xpath('//a')
        for page in pages:
            try:
                page = page.attrib['href']
                if page[0:4] == 'http' and page not in links:
                    links.append(page)
                    
            except:
                continue
            
        db.collection.insert({'seed':url, 'all_link':links})
            
        return links
                
    except:
        return links




def word_sp(keysss, url):
    for keyss in keysss:
        keys = str(keyss.text).split()
        for key in keys:
            entry = collection.find_one({'keyword':key})
            if entry:
                if url not in entry['url']:
                    entry['url'].append(url)
                    db.collection.save(entry)

            else:
                db.collection.insert({'keyword':key, 'url':[url]})

def words_list(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.text, 'lxml')

        titlesss = soup.find_all("title")
        word_sp(titlesss, url)

        h1sss = soup.find_all("h1")
        word_sp(h1sss, url)

        h2sss = soup.find_all("h2")
        word_sp(h2sss, url)

        h3sss = soup.find_all("h3")
        word_sp(h3sss, url)

        lisss = soup.find_all('li')
        word_sp(lisss, url)

        psss = soup.find_all('p')
        word_sp(psss, url)
    except:
        return


if __name__ == "__main__":
    tocrawl = ['http://www']
    depth = 0
    while tocrawl and depth <= 3:
        url = tocrawl.pop()

        find = collection.find_one({'seed':url})
        if not find:
            words_list(url)                ######### making collection
            links = all_link_in_url(url)   ######### get all links in url
            for e in links:                ######### making tocrawl
                if e not in tocrawl:
                    tocrawl.append(e)

        depth += 1
