#!/usr/bin/env python

import yaml
import argparse
import time

parser = argparse.ArgumentParser(description='Create DeTT&CK data files')
parser.add_argument('-s', '--source', nargs='+', dest="source")
parser.add_argument('-c', '--category', dest="category")
parser.add_argument('-o', '--output', dest="output_file")
parser.add_argument('-p', '--products', dest="products_file")

args = parser.parse_args()

if args.output_file:
    out_file = args.output_file
else:
    out_file = "output.yaml"
if args.products_file:
    products_file = args.products_file
else:
    products_file = 'product-sources.yaml'

ds_template = 'data-sources-template.yaml'

products = yaml.load(open(products_file), Loader=yaml.FullLoader)
ds_file = yaml.load(open(ds_template), Loader=yaml.FullLoader)

date = time.strftime('%Y-%m-%d')

for product in products:
    if (args.source) and (product['name'] not in args.source):
        pass
    elif (args.category) and (product['category'] != args.category):
        pass
    else:
        for ds in product['data_sources']:
            for i, raw_ds in enumerate(ds_file['data_sources']):
                if raw_ds['data_source_name'] == ds:
                    if args.category:
                        category = args.category
                        raw_ds['products'] = [category]
                    else:
                        if raw_ds['products'][0] == "None":
                            raw_ds['products'] = [product['name']]
                        else:
                            raw_ds['products'].append(product['name'])
                    raw_ds['available_for_data_analytics'] = True
                    raw_ds['data_quality']['device_completeness'] = 5
                    raw_ds['data_quality']['timeliness'] = 5
                    raw_ds['data_quality']['data_field_completeness'] = 5
                    raw_ds['data_quality']['consistency'] = 5
                    raw_ds['data_quality']['retention'] = 5
                    raw_ds['date_connected'] = date
                    raw_ds['date_registered'] = date
                ds_file['data_sources'][i] = raw_ds 
        ds_file['name'] = "generated-" + date

with open(out_file, 'w') as f:
    yaml.dump(ds_file, f, default_flow_style=False)