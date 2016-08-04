# -*- coding: utf-8 -*-

# importing modules
import requests
import csv
from bs4 import BeautifulSoup
import unicodedata

# variables
lnkParam    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
              'mostrar.htm?id={0}&edi_id={1}'
ediParam    = 1772
matParam    = 335

# http response
response    = requests.get(lnkParam.format(matParam, ediParam))
soup        = BeautifulSoup(response.content, 'html.parser', from_encoding="iso-8859-1")

topoMateria = soup.find_all(class_='topo_materia')[0]

topoMatList = []
n = 0
for string in topoMateria.stripped_strings:
    n += 1
    if n % 2 == 0:
        topoMatList.append(unicodedata.normalize("NFKD", string).encode('utf-8'))

print topoMatList
