import csv

file = open("cameralist.csv")
csvreader = csv.reader(file)
addresses = []
for row in csvreader:
    addresses.extend(row)
print(addresses)
