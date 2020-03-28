# return a scaled pandas series
def get_pds_scaled(pds, scale_logic):
    
    # dependecies
    import numpy as np
    
    if scale_logic == 'max perc':
        
        pds = (pds / np.nanmax(pds))
        
    elif scale_logic == 'log max perc':
        pds = np.log(1 + pds)
        pds = (pds / np.nanmax(pds))

    return pds

# return a pandas dataframe with palettes as original series
def get_colors(pds, palettable_pal, scale_logic = 'max perc', opacity = 1, opacity_border = 1):

    # dependecies
    import pandas as pd
    import numpy as np

    # initialize a blank dictionary that will be converted into a pandas dataframe
    df_colors = {
                 'series': pds
                ,'rgb': []
                ,'hex': []
                ,'rgba': []
                ,'rgba_border': []
                }    
   
    # scale pandas series
    pds_scaled = get_pds_scaled(pds = pds, scale_logic = scale_logic).tolist()
    
    # initialize rgba colors list
    rgba_colors = []
    rgba_colors_border = []

    # build up rgba colors
    for rgb_color in palettable_pal.colors:
        
        # rgba
        rgba_colors.append(
                'rgba('
                + str(rgb_color[0]) + ', '
                + str(rgb_color[1]) + ', '
                + str(rgb_color[2]) + ', '
                + str(opacity) + ')'
        )
                
        # rgba border
        rgba_colors_border.append(
                'rgba('
                + str(rgb_color[0]) + ', '
                + str(rgb_color[1]) + ', '
                + str(rgb_color[2]) + ', '
                + str(opacity_border) + ')'
        )
                
    # create a palette dataframe
    df_palette = pd.DataFrame(
                            {'index': np.arange(0, len(palettable_pal.colors), 1)
                            ,'value': np.linspace(0,1,len(palettable_pal.colors))
                            ,'rgb': palettable_pal.colors
                            ,'rgba': rgba_colors
                            ,'rgba_border': rgba_colors_border
                            ,'hex': palettable_pal.hex_colors                        
                            }
                        )
    
    # find an appropriate color for every value of pandas series
    for value in pds_scaled:
        
        i = df_palette['value'] < value
        
        if pd.isna(value) or i.sum() == 0:
            
            i = 0
            
        else:
                                    
            i = np.nanmax(df_palette.loc[i, 'index'])
            
        df_colors['rgb'].append(df_palette.loc[i, 'rgb'])
        df_colors['rgba'].append(df_palette.loc[i, 'rgba'])
        df_colors['rgba_border'].append(df_palette.loc[i, 'rgba_border'])
        df_colors['hex'].append(df_palette.loc[i, 'hex'])
    
    # create output dataframe
    df_colors = pd.DataFrame(df_colors)
    
    return(df_colors)

# return dictionary with chart data
def build_linechart_dates(x_pds_dt, x_freq, y_first_dict, y_sec_dict = {}):
    
    # dependecies
    import pandas as pd

    # create labels at specified frequency
    labels = (
            (100 + x_pds_dt.dt.day).astype(str).str[1:3]
            + ' '
            + x_pds_dt.dt.month_name(locale = 'it').str[:3].str.lower()
        )

    i = ((pd.Series(list(range(0, len(labels)))) + 1) % x_freq) != 0

    if i.sum() > 0:
        labels[i] = ''
    
    if 'bordercolor' not in y_first_dict:
        y_first_dict['bordercolor'] = y_first_dict['backgroundcolor']    

    # create dictionary with chart data
    if(len(y_sec_dict) > 0):
                
        if 'bordercolor' not in y_sec_dict:
            y_sec_dict['bordercolor'] = y_sec_dict['backgroundcolor']
        
        data_out = {
                'labels': labels.tolist()
                ,'data_first': y_first_dict['data']
                ,'backgroundcolor_first': y_first_dict['backgroundcolor']
                ,'bordercolor_first': y_first_dict['bordercolor']
                ,'label_first': y_first_dict['label']
                ,'data_sec': y_sec_dict['data']
                ,'label_sec': y_sec_dict['label']
                ,'backgroundcolor_sec': y_sec_dict['backgroundcolor']
                ,'bordercolor_sec': y_sec_dict['bordercolor']                
            }
    else :
        data_out = {
                'labels': labels.tolist()
                ,'data_first': y_first_dict['data']
                ,'backgroundcolor_first': y_first_dict['backgroundcolor']
                ,'bordercolor_first': y_first_dict['bordercolor']
                ,'label_first': y_first_dict['label']
            }
    
    return(data_out)
        
    
    
# build a dictionary with charts data    
def build_charts_naz(df):
    
    # dependecies
    from palettable.colorbrewer.sequential import YlOrRd_9 as palettable_pal_red
    from palettable.colorbrewer.sequential import YlGn_9 as palettable_pal_green
    
    # add new columns
    df = df.sort_values(by = ['data', 'stato'])
    df['nuovi_deceduti'] = df['deceduti'] - df['deceduti'].shift(+1)
    df['nuovi_dimessi_guariti'] = df['dimessi_guariti'] - df['dimessi_guariti'].shift(+1)
    df['nuovi_tamponi'] = df['tamponi'] - df['tamponi'].shift(+1)
    
    # build charts
    
    # nuovi positivi
    pds = df['nuovi_attualmente_positivi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = palettable_pal_red
                    ,scale_logic = 'max perc'
                    ,opacity = 0.7
                    ,opacity_border = 1
                    )
    
    chart_nuovi_positivi = build_linechart_dates(
                                         x_pds_dt = df['data']
                                        ,x_freq = 1
                                        ,y_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Nuovi Positivi'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border'].tolist()
                                                        }
                                    
                                    )

    # nuovi positivi
    pds = df['totale_attualmente_positivi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = palettable_pal_red
                    ,scale_logic = 'max perc'
                    ,opacity = 0.7
                    ,opacity_border = 1
                    )
    
    chart_tot_positivi = build_linechart_dates(
                                         x_pds_dt = df['data']
                                        ,x_freq = 1
                                        ,y_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Attualmente Positivi'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border'].tolist()
                                                        }
                                    
                                    )
    
    # deceduti
    pds = df['nuovi_deceduti']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = palettable_pal_red
                    ,scale_logic = 'max perc'
                    ,opacity = 0.7
                    ,opacity_border = 1
                    )
    
    chart_deceduti = build_linechart_dates(
                                         x_pds_dt = df['data']
                                        ,x_freq = 1
                                        ,y_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Deceduti'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border'].tolist()
                                                        }
                                    
                                    )

    # decessi
    pds = df['nuovi_dimessi_guariti']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = palettable_pal_green
                    ,scale_logic = 'max perc'
                    ,opacity = 0.7
                    ,opacity_border = 1
                    )
    
    chart_guariti = build_linechart_dates(
                                         x_pds_dt = df['data']
                                        ,x_freq = 1
                                        ,y_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Dimessi Guariti'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border'].tolist()
                                                        }
                                    
                                    )

    # dictionary with all charts
    charts_dict = {
                 'chart_nuovi_positivi': chart_nuovi_positivi
                ,'chart_tot_positivi': chart_tot_positivi
                ,'chart_deceduti': chart_deceduti
                ,'chart_guariti': chart_guariti
                }

    return(charts_dict)
    
                
# write dictionary to json file
def write_charts_data(charts_dict, pathfilename):

    # dependecies
    import json
    
    list_json_null = ['nan', 'NaN']
    
    # write json
    with open(file = pathfilename, mode = 'w') as file_towrite:    
        
        json.dump(obj = charts_dict, fp = file_towrite)    
        
    # fix nan or NaN
    with open(file = pathfilename, mode = 'r') as file_toread:
        file_json = file_toread.read()        
         
    # replace with null
    for list_item in list_json_null:
        file_json = file_json.replace('NaN', 'null')
        
    # fix nan or NaN
    with open(file = pathfilename, mode = 'w') as file_towrite:
        file_towrite.write(file_json)
        

# return geo dataframe
def build_geomap_reg(df, dir_home, col_value, col_value_newlabel = ''):

    # dependecies
    import geopandas as gpd
    from palettable.colorbrewer.sequential import YlOrRd_9 as palettable_pal
    
    # check newlabel
    if col_value_newlabel == '':
        col_value_newlabel = col_value
        
    # value to represent with clorophlet
    col_value_scaled = col_value + '_scaled'    
    
    # retrieve last available data from regions
    i = df['data'] == df['data'].max()
    df = df.loc[i, ].groupby(['codice_regione']).sum()
    df['COD_REG'] = df.index
    
    # read geojson
    gdf = gpd.read_file(dir_home + r'\data_geo\geojson_leaflet\ita_regions.geojson')
    
    # merge geojson and regions data
    gdf = gdf.merge(right = df
                    ,how = 'left'
                    ,on = 'COD_REG'
                    )
    
    # scale values
    gdf[col_value_scaled] = get_pds_scaled(pds = gdf.loc[:, col_value], scale_logic = 'max perc')
    
    # get color palette
    df_col = get_colors(pds = gdf[col_value_scaled]
                        ,palettable_pal = palettable_pal
                        ,scale_logic = 'log max perc'                                     
                        )    
    
    # add hex colors
    gdf['hex_color'] = df_col['hex']
       
    # reorder and rename geo dataframe columns
    col_names = [
             'NOME_REG'
            ,col_value
            ,'hex_color'
            ,'terapia_intensiva'
            ,'deceduti'
            ,'dimessi_guariti'
            ,'geometry'
        ]
    
    col_names_sort = [
            'NOME_REG'
            ,col_value
            ,'hex_color'
            ,'terapia_intensiva'
            ,'deceduti'
            ,'dimessi_guariti'
            ,'geometry'
        ]
    
    col_names_new = [
             'Regione'
            ,col_value_newlabel
            ,'hex_color'
            ,'Terapia_Intensiva'
            ,'Deceduti'
            ,'Guariti'
            ,'geometry'
        ]
    
    gdf = gdf[gdf.columns.intersection(col_names)]
    gdf = gdf.loc[:, col_names_sort]
    gdf.columns = col_names_new
    
    # return geo dataframe
    return(gdf)
    
    
# write geo dataframe    
def write_geojson_data(gdf, pathfilename):
    
    # write geojson
    gdf.to_file(pathfilename, driver="GeoJSON")
    
        
           
        



    