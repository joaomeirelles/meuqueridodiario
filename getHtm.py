# -*- coding: utf-8 -*-

# importing modules
import requests
import csv

# variables
htmParam    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
              'load_tree.php?edi_id={0}'
lnkParam    = 'http://doweb.rio.rj.gov.br/do/navegadorhtml/' \
              'mostrar.htm?id={0}&edi_id={1}'

for edi in range(1974,1770,-1):
#for edi in [3173]:

    ediParam    = edi
    folders     = []
    materias    = []

    # http response
    response    = requests.get(htmParam.format(ediParam))
    respList    = response.content.split('\n')
    #respList    = open('3168_response.txt')

    for row in respList:
        if 'gFld(' in row:
            fldKey      = row[0:row.find(' = ')]
            fldVal      = row[row.find('gFld(')+5:row.find(');')] \
                          .split(', ')[0][1:-1].decode('iso-8859-1').encode('utf8')
            folders.append(dict(fldKey=fldKey, fldVal=fldVal))
        elif 'addChild(' in row:
            materia     = row[row.find('([')+2:row.find('])')].split('", "')
            matId       = materia[1][materia[1].find('?id=')+4: \
                          materia[1].find('&edi')]
            matTitulo   = materia[0][1:].decode('iso-8859-1').encode('utf8')
            matPaiKey   = row[0:row.find('.addChild')]
            materias.append(dict(matPathKey=[matPaiKey],
                                 matPathVal='',
                                 matTitulo=matTitulo,
                                 matId=matId,
                                 matEdi=ediParam,
                                 matLink=lnkParam.format(matId,ediParam)))
        elif 'addChildren(' in row:
            paiKey      = row[0:row.find('.addChildren')]
            childVals   = row[row.find('([')+2:row.find('])')].split(',')
            for val in childVals:
                for materia in materias:
                    if materia['matPathKey'][0] == val:
                        materia['matPathKey'].insert(0, paiKey)

    for materia in materias:
        for n,i in enumerate(materia['matPathKey']):
            for keyVal in folders:
                if keyVal['fldKey'] == i:
                    materia['matPathVal'] += keyVal['fldVal']
                    if n < len(materia['matPathKey']) - 1:
                        materia['matPathVal'] += ' | '

    matsOutput = materias


    with open('htmLinks/' + str(ediParam) + '.csv', 'w') as csvfile:
        fieldnames = ['matEdi','matId','matPathVal','matTitulo','matLink']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for matOut in matsOutput:
            del matOut['matPathKey']
            writer.writerow(matOut)

    print ediParam
