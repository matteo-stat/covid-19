# dependecies
import sys

# change this directory for local work
#dir_home = r'C:\Users\Matteo\Documents\GitHub\covid-19\py_app'
dir_home = r'C:\Users\Matteo\Documents\GitHub\covid-19\py_app'
dir_output = r'C:\Users\Matteo\Documents\GitHub\covid-19\docs\json'

# download data
download_data = True

# user custom library
sys.path.append(dir_home + r'\py_def')
from data_download import get_config
from data_download import get_data
from data_load import load_data
from data_out import build_charts_index
from data_out import build_charts_reg
from data_out import build_geomap_reg
from data_out import build_geomap_prov
from data_out import write_charts_data
from data_out import write_geojson_data

# project config
proj_config = get_config(dir_home = dir_home
                        ,sep = ';'
                        ,header = True)

# download data
if(download_data):
    #get_data(proj_config['geojson'])
    #get_data(proj_config['shapefile'])
    get_data(proj_config['dati_andamento_nazionale'])
    get_data(proj_config['dati_regioni'])
    get_data(proj_config['dati_province'])

# load data
df_naz = load_data(proj_config['dati_andamento_nazionale']['dati_andamento_nazionale']['file_disk'])
df_reg = load_data(proj_config['dati_regioni']['dati_regioni']['file_disk'])
df_prov = load_data(proj_config['dati_province']['dati_province']['file_disk'])

# build charts
charts_index = build_charts_index(df_naz = df_naz
                                  ,df_reg = df_reg
                                  ,dir_home = dir_home)

charts_reg = build_charts_reg(df_reg = df_reg
                              ,df_prov = df_prov
                              ,dir_home = dir_home)

map_reg = build_geomap_reg(df = df_reg
                           ,dir_home = dir_home
                           ,col_value = 'totale_positivi')

map_prov = build_geomap_prov(df_prov = df_prov
                             ,df_reg = df_reg
                             ,dir_home = dir_home
                             ,col_value = 'totale_casi')


# write charts data
write_charts_data(charts_dict = charts_index
                  ,pathfilename = dir_output + r'\italia\charts_ita.json'
                  ,split_key = False)

write_charts_data(charts_dict = charts_reg
                  ,pathfilename = dir_output + r'\regioni'
                  ,split_key = True)

write_geojson_data(obj = map_reg
                   ,pathfilename = dir_output + r'\italia\map_ita.geojson'
                   ,split_key = False)

write_geojson_data(obj = map_prov
                   ,pathfilename = dir_output + r'\regioni'
                   ,split_key = True)
