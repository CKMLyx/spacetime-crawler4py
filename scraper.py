import re
from urllib.parse import urlparse
from utils.response import Response
from bs4 import BeautifulSoup
import urllib.request
from urllib.parse import urlparse

dec_values = set()
dec_values.update(range(48,57+1))
dec_values.update(range(65,90+1))
dec_values.update(range(97,122+1))
#Pages found
unique_pages = set()

#Allowed domains
allowed_domains = ("ics.uci.edu","cs.uci.edu","informatics.uci.edu","stat.uci.edu","today.uci.edu/department/information_computer_sciences")

#Read stopwords from text 
def load_stopwords():
    stop_words = set()
    f = open("stopwords.txt","r")
    words = f.read().split("\n")
    for word in words:
        stop_words.add(word)
    return stop_words
stop_words = load_stopwords()

def tokenize(html):
    html = html.split("\n")
    tokens = []
    for line in html:
        line = str(line)
        for word in re.split("[\s;,\-\n.?']",line):
            if len(word) > 1:
                word = word.lower()
                val = checkalnum(word)
                if val and word not in stop_words:
                    tokens.append(word)
    return tokens

def is_valid(url):
    try:
        parsed = urlparse(url)
        if parsed.scheme not in set(["http", "https"]):
            return False
        if urlparse(url).netloc[4:] not in allowed_domains:
            return False
        return not re.match(
            r".*\.(css|js|bmp|gif|jpe?g|ico"
            + r"|png|tiff?|mid|mp2|mp3|mp4"
            + r"|wav|avi|mov|mpeg|ram|m4v|mkv|ogg|ogv|pdf"
            + r"|ps|eps|tex|ppt|pptx|doc|docx|xls|xlsx|names"
            + r"|data|dat|exe|bz2|tar|msi|bin|7z|psd|dmg|iso"
            + r"|epub|dll|cnf|tgz|sha1"
            + r"|thmx|mso|arff|rtf|jar|csv"
            + r"|rm|smil|wmv|swf|wma|zip|rar|gz)$", parsed.path.lower())

    except TypeError:
        print ("TypeError for ", parsed)
        raise

def checkalnum(word):
    for i in range(len(word)):
        if ord(word[i]) not in dec_values:
            return False
    return True

def scraper(url, resp):

    links = extract_next_links(url, resp)
    conn = urllib.request.urlopen(url)
    html = conn.read()

    soup = BeautifulSoup(html,'lxml')
    res = tokenize(soup.get_text())
    #print(res) Don't print. Write to file instead.
    return [link for link in links if is_valid(link)]

def extract_next_links(url, resp):
    if is_valid(url):
        conn = urllib.request.urlopen(url)
        html = conn.read()

        soup = BeautifulSoup(html,'lxml')
        links = soup.find_all('a')

        res = []
        for tag in links:
            link = tag.get('href',None)
            if link is not None:
                res.append(link)
        
        return res



