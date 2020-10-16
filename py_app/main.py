# dependecies
import sys

# change this directory for local work
dir_home = r'C:\Users\Matteo\Documents\GitHub\covid-19\py_app'
dir_output = r'C:\Users\Matteo\Documents\GitHub\covid-19\docs\json'

# download data
download_data = True

# user custom library
sys.path.append(dir_home + r'\py_def')
import data_download
import data_load
import data_out

# project config
proj_config = data_download.get_config(dir_home = dir_home, sep = ';', header = True)

# download data
if(download_data):
    data_download.get_data(proj_config['dati_andamento_nazionale'])
    data_download.get_data(proj_config['dati_regioni'])
    data_download.get_data(proj_config['dati_province'])

# load data
df_naz = data_load.load_data(proj_config['dati_andamento_nazionale']['dati_andamento_nazionale']['file_disk'])
df_reg = data_load.load_data(proj_config['dati_regioni']['dati_regioni']['file_disk'], fix_reg = True)
df_prov = data_load.load_data(proj_config['dati_province']['dati_province']['file_disk'], fix_reg = True)

# build charts
charts_index = data_out.build_charts_index(df_naz = df_naz
                                           ,df_reg = df_reg
                                           ,dir_home = dir_home)

charts_reg = data_out.build_charts_reg(df_reg = df_reg
                                       ,df_prov = df_prov
                                       ,dir_home = dir_home)

map_reg = data_out.build_geomap_reg(df = df_reg
                                    ,dir_home = dir_home
                                    ,col_value = 'totale_positivi')

map_prov = data_out.build_geomap_prov(df_prov = df_prov
                                      ,df_reg = df_reg
                                      ,dir_home = dir_home
                                      ,col_value = 'totale_casi')

# write charts data
data_out.write_charts_data(charts_dict = charts_index
                           ,pathfilename = dir_output + r'\italia\charts_ita.json'
                           ,split_key = False)

data_out.write_charts_data(charts_dict = charts_reg
                           ,pathfilename = dir_output + r'\regioni'
                           ,split_key = True)

data_out.write_geojson_data(obj = map_reg
                            ,pathfilename = dir_output + r'\italia\map_ita.geojson'
                            ,split_key = False)

data_out.write_geojson_data(obj = map_prov
                            ,pathfilename = dir_output + r'\regioni'
                            ,split_key = True)