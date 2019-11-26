import urllib
from bs4 import BeautifulSoup


class Paper:
    def __init__(self, field, title, authors, pdf, abstract):
        self.field = field
        self.title = title
        self.authors = authors
        self.pdf = pdf
        self.abstract = abstract
        
    def __repr__(self):
        s = 'Paper {\n'
        s += ''.join([f'{k:>10}: {v}\n' for k, v in self.__dict__.items()])
        s += '}'
        return s
    
    
def get_fields(domain='cs'):
    fields = {}

    uh = urllib.request.urlopen(f'https://arxiv.org/archive/{domain}')
    soup = BeautifulSoup(str(uh.read()))

    for x in soup.findAll('ul')[2].findAll('li'):
        k = x.findAll('b')[0].text
        field, desc = k[3:5], k[8:]
        fields[field] = desc

    return fields


def get_abstract(url):
    uh = urllib.request.urlopen(url)
    soup = BeautifulSoup(str(uh.read()))
    a = soup.findAll('blockquote', {'class': 'abstract mathjax'})[0].text
    a = a.replace('\\n', ' ')
    a = a.replace('Abstract:  ', '')
    return a