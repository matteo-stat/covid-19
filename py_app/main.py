# namespaces
import pandas as pd
import geopandas as gpd
import sys

# change this directory for local work
dir_home = r'C:\Users\Matteo\Documents\GitHub\covid-19\py_app'

# user custom library
sys.path.append(dir_home + r'\py_def')
from data_download import get_config
from data_download import get_data
from data_load import load_data
from data_out import build_linecharts_naz
from data_out import write_charts_data


# project config
proj_config = get_config(dir_home = dir_home
                        ,sep = ';'
                        ,header = True)

# download data
#get_data(proj_config['geojson'])
#get_data(proj_config['shapefile'])
get_data(proj_config['dati_andamento_nazionale'])
get_data(proj_config['dati_regioni'])
get_data(proj_config['dati_province'])

# load data
df_naz = load_data(proj_config['dati_andamento_nazionale']['dati_andamento_nazionale']['file_disk'])
df_reg = load_data(proj_config['dati_regioni']['dati_regioni']['file_disk'])
df_pro = load_data(proj_config['dati_province']['dati_province']['file_disk'])

# build charts
charts_naz = build_linecharts_naz(df_naz)

# write charts data
write_charts_data(charts_naz, dir_home + r'\data_out\andamento_nazionale.json')