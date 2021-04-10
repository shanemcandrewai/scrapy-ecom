import json
import pandas as pd

def one_hot():
    with open('mp.json') as f:
        dfd = json.load(f)
    csvl = []
    rec = {}
    for d in dfd:
        for l in d['listings']:
            rec = l.copy()
            rec.update(d)
            rec[rec['periodSinceRegistrationDate']] = True
            rec[rec['priceType']] = True
            if 'countryAbbreviation' in rec and 'cityName' in rec:
                rec[rec['countryAbbreviation'] + rec['cityName']] = True
            rec[rec['sellerId']] = True
            rec[rec['categoryId']] = True
            for v in rec['verticals']:
                rec[v] = True
            del rec['id']
            del rec['periodSinceRegistrationDate']
            del rec['title']
            del rec['priceType']
            if 'cityName' in rec:
                del rec['cityName']
            if 'countryAbbreviation' in rec:
                del rec['countryAbbreviation']
            del rec['date']
            del rec['sellerId']
            del rec['sellerName']
            del rec['categoryId']
            del rec['verticals']
            del rec['listings']
            csvl.append(rec)
    return pd.DataFrame(csvl)

def flatten():
    with open('mp.json') as f:
        mp = json.load(f)
    csvl = []
    rec = {}
    for d in mp:
        for l in d['listings']:
            rec = l            
            rec.update(d)                
            rec['verticals'] = '-'.join(rec['verticals'])
            del rec['itemId']
            del rec['id']                
            del rec['title']                
            del rec['listings']
            del rec['date']                
            del rec['sellerName']
            csvl.append(rec)
    return pd.DataFrame(csvl)
    
