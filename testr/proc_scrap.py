import json
import pandas as pd
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
df = pd.DataFrame(csvl)
