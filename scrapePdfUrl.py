# -*- coding: utf-8 -*-
# importing modules
import requests
import BeautifulSoup
import os
import datetime
import csv

# variables
today       = datetime.datetime.now().strftime("%Y%m%d")
searchParam = 'pablo de camargo cerdeira'
urlParam    = 'http://doweb.rio.rj.gov.br/buscaweb/' \
              'search?q={0}&f=100&px=10&t=1&p={1}'
htmParam    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
              'load_tree.php?edi_id={0}'


def scrapeSearchResults(searchArg):
    '''
    returns the URLs containing the search parameter
    '''
    allResults  = []
    searchPage  = 1

    while True:
        response    = requests.get(urlParam.format(searchArg, searchPage))
        soup        = BeautifulSoup.BeautifulSoup(response.content)
        pageResults = [i.get('href') for i in soup.findAll('a') \
                       if i.get('href').find('search=' + searchArg) > 0]
        if len(pageResults) > 0:
            allResults  += pageResults
            searchPage  += 1
        else:
            break

    # cria lista com dicionários com URLs da busca e respectivos parametros
    resultDicts = []
    urlId       = 0
    for url in allResults:
        urlId       += 1
        resultDict  = {}

        resultDict['id']            = urlId
#        resultDict['search_url']    = url
        resultDict['do_edicao']     = url[url.find('edi_id=') + \
                                      len('edi_id='):url.find('&page=')]
        resultDict['do_pagina']     = url[url.find('&page=') + \
                                      len('&page='):url.find('&search=')]
        resultDict['pdf_url']       = 'http://doweb.rio.rj.gov.br/' \
                                      'ler_pdf.php?edi_id={0}&page={1}'.format(\
                                      resultDict['do_edicao'],
                                      resultDict['do_pagina'])
        resultDicts.append(resultDict)

    with open(searchParam + '.csv', 'w') as csvfile:
        fieldnames = ['id', 'do_edicao', 'do_pagina', 'pdf_url']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for result in resultDicts:
            writer.writerow(result)

    #
    ediParam    = resultDicts[0]['do_edicao']
    response    = requests.get(htmParam.format(ediParam))
    soup        = BeautifulSoup.BeautifulSoup(response.content)


    pageResults = [i.get('href') for i in soup.findAll('a') \
                   if i.get('href').find('search=' + searchArg) > 0]


    return True


scrapeSearchResults(searchParam)
