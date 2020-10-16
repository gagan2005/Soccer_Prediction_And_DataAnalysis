import sys 
import csv
import re

def makecsv(file,season):
    try:
        with open(file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=season[0].keys())
            writer.writeheader()
            for data in season:
                writer.writerow(data)
    except IOError:
        print("I/O error")




filename =  'playerdata.csv'
season1 = []
season2 = []
season3 = []
with open(filename, mode='r') as csv_file:
    reader = csv.DictReader(csv_file)
    #print(reader.fieldnames)
    for row in reader:
        row1={}
        row2={}
        row3={}
        for feature in reader.fieldnames:
            if feature=='name':
                row1['name'] = row[feature]
                row2['name'] = row[feature]
                row3['name'] = row[feature]
            else:
                s = row[feature]
                seasons = re.findall(r"[-+]?\d*\.\d+|\d+", s)
                while len(seasons)<3:
                    seasons.append(None)

                row1[feature] = (seasons[0])
                row2[feature] = (seasons[1])
                row3[feature] = (seasons[2])

        season1.append(row1)
        season2.append(row2)
        season3.append(row3)

print(season1[0].keys())
makecsv('season1.csv',season1)
makecsv('season2.csv',season2)
makecsv('season3.csv',season3)
