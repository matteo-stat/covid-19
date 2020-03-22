# namespaces
import pandas as pd
import geopandas as gpd
import sys

# change this directory for local work
dir_home = r'C:\Users\Matteo\Documents\GitHub\covid-19'

# user custom library
sys.path.append(dir_home + r'\py_def')
from data_download import get_config
from data_download import get_data

# project config
proj_config = get_config(dir_home = dir_home
                        ,sep = ';'
                        ,header = True)

# download data
get_data(proj_config['geojson'])
get_data(proj_config['shapefile'])
get_data(proj_config['dati_andamento_nazionale'])
get_data(proj_config['dati_regioni'])
get_data(proj_config['dati_province'])

# read downloaded data
df_naz = pd.read_csv(filepath_or_buffer = proj_config['dati_andamento_nazionale']['dati_andamento_nazionale']['file_disk']
                    ,sep = ','
                    ,header = 0)

df_reg = pd.read_csv(filepath_or_buffer = proj_config['dati_regioni']['dati_regioni']['file_disk']
                    ,sep = ','
                    ,header = 0)

df_prov = pd.read_csv(filepath_or_buffer = proj_config['dati_province']['dati_province']['file_disk']
                    ,sep = ','
                    ,header = 0)

gdf_shape = gpd.read_file(proj_config['shapefile']['aree_shp']['file_disk'])

gdf_geojson = gpd.read_file(proj_config['geojson']['aree_geojson']['file_disk'])

# geojson plot?
gdf_geojson.plot(figsize=(10,10), color='none', edgecolor='gainsboro', zorder=3)
