import csv

input_file = csv.DictReader(open("data.csv"))

states = {row['Abbreviation']:row for row in input_file}