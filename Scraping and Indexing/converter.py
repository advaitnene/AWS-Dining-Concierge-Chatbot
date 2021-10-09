import csv
import json
import collections
from collections import OrderedDict
orderedDict = collections.OrderedDict()


def csv_to_json(csvFilePath, jsonFilePath):
    jsonArray = []
    # x = OrderedDict([('index', {})])
    # jsonString = json.dumps(x)
    jsonString  = ""
    with open(csvFilePath, encoding='utf-8') as csvf:
        with open(jsonFilePath, 'w', encoding='utf-8') as jsonf:
            csvReader = csv.DictReader(csvf)
            for row in csvReader:
                jsonf.write(jsonString)
                # jsonf.write("\n")
                y = json.dumps(row)
                jsonf.write(y)
                jsonf.write("\n")


csvFilePath = r'C:/Users/Sudhindra/Desktop/SOPs/NEW_2021/BOSE/Colleges/NYU\Assignments/Cloud/Dining CC/final_results.csv'
jsonFilePath = r'C:/Users/Sudhindra/Desktop/SOPs/NEW_2021/BOSE/Colleges/NYU\Assignments/Cloud/Dining CC/elastic.json'
csv_to_json(csvFilePath, jsonFilePath)
