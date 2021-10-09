import pandas
import ipdb
import json

old = pandas.read_csv('final_results.csv')

new = []
for i in range(len(old)):
	r = {}
	r['Restaurant'] = {}
	r['Restaurant']['RestaurantID'] = old['RestaurantID'][i]                                                     
	r['Restaurant']['Cuisine'] = old['Cuisine'][i]  
	new.append(r)

with open('final_indices.json', 'w') as fout:
    json.dump(new, fout)