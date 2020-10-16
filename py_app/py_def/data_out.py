# return a scaled pandas series
def get_pds_scaled(pds, scale_logic):
    
    # dependecies
    import numpy as np
    
    if np.nanmin(pds) < 0:
        
        pds = pds + abs(np.nanmin(pds))
    
    if scale_logic == 'max perc':
        
        pds = (pds / np.nanmax(pds))
        
    elif scale_logic == 'log max perc':
        
        pds = np.log(1 + pds)
        pds = (pds / np.nanmax(pds))

    return pds

# return a scaled pandas series but scale logic reset at zero
def get_pds_scaled_zero(pds, scale_logic):
    
    # dependecies
    import pandas as pd
    import numpy as np
        
    df = pd.DataFrame({'pds': pds})
    
    i = df['pds'] < 0
    j = df['pds'] >= 0
    
    if scale_logic == 'max perc':
        
        if i.sum() > 0:
            df.loc[i, 'pds'] = -(abs(df.loc[i, 'pds']) / abs(np.nanmin(df.loc[i, 'pds'])))
            
        if j.sum() > 0:
            
            df.loc[j, 'pds'] = (df.loc[j, 'pds'] / np.nanmax(df.loc[j, 'pds']))
        
    elif scale_logic == 'log max perc':
        
        if i.sum() > 0:
            df.loc[i, 'pds'] = np.log(1 + abs(df.loc[i, 'pds']))
            df.loc[i, 'pds'] = -(df.loc[i, 'pds'] / np.nanmax(df.loc[i, 'pds']))
        
        if j.sum() > 0:
            df.loc[j, 'pds'] = np.log(1 + df.loc[j, 'pds'])
            df.loc[j, 'pds'] = (df.loc[j, 'pds'] / np.nanmax(df.loc[j, 'pds']))

    return df['pds']

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
                ,'rgba_border_fixed': []
                }    
   
    # scale pandas series
    if len(palettable_pal)>1:
        
        pds_scaled = get_pds_scaled_zero(pds = pds, scale_logic = scale_logic).tolist()
        
    else:
    
        pds_scaled = get_pds_scaled(pds = pds, scale_logic = scale_logic).tolist()
    
    # initialize rgba colors dict
    rgba_colors = {}
    rgba_colors_border = {}

    for pal_key in palettable_pal:
        
        # initialize rgba colors list
        if pal_key not in rgba_colors:
            
            rgba_colors[pal_key] = []
            
        if pal_key not in rgba_colors_border:
            
            rgba_colors_border[pal_key] = []        
            
        # build up rgba colors
        for rgb_color in palettable_pal[pal_key].colors:
            
            # rgba
            rgba_colors[pal_key].append(
                    'rgba('
                    + str(rgb_color[0]) + ', '
                    + str(rgb_color[1]) + ', '
                    + str(rgb_color[2]) + ', '
                    + str(opacity) + ')'
            )
                    
            # rgba border
            rgba_colors_border[pal_key].append(
                    'rgba('
                    + str(rgb_color[0]) + ', '
                    + str(rgb_color[1]) + ', '
                    + str(rgb_color[2]) + ', '
                    + str(opacity_border) + ')'
            )

    # create a palette dataframe
    df_palette = pd.DataFrame(
                            {'index': np.arange(0, len(palettable_pal['main'].colors), 1)
                            ,'value': np.linspace(0,1,len(palettable_pal['main'].colors))
                            ,'rgb_main': palettable_pal['main'].colors
                            ,'rgba_main': rgba_colors['main']
                            ,'rgba_border_main': rgba_colors_border['main']
                            ,'hex_main': palettable_pal['main'].hex_colors                                
                            }
                        )
                
    if len(palettable_pal)>1:
        df_palette['rgb_opt'] = palettable_pal['opt'].colors
        df_palette['rgba_opt'] = rgba_colors['opt']
        df_palette['rgba_border_opt'] = rgba_colors_border['opt']
        df_palette['hex_opt'] = palettable_pal['opt'].hex_colors
    
    # find an appropriate color for every value of pandas series
    for value in pds_scaled:
        
        if value < 0:
            
            value_key = 'opt'
            
        else:
            
            value_key = 'main'
        
        i = df_palette['value'] < abs(value)
        
        if pd.isna(value) or i.sum() == 0:
            
            i = 0
            
        else:
                                    
            i = np.nanmax(df_palette.loc[i, 'index'])
            
        df_colors['rgb'].append(df_palette.loc[i, 'rgb_' + value_key])
        df_colors['hex'].append(df_palette.loc[i, 'hex_' + value_key])
        df_colors['rgba'].append(df_palette.loc[i, 'rgba_' + value_key])
        df_colors['rgba_border'].append(df_palette.loc[i, 'rgba_border_' + value_key])
        df_colors['rgba_border_fixed'].append(df_palette.loc[len(palettable_pal[value_key].colors)-1, 'rgba_border_' + value_key])
    
    # create output dataframe
    df_colors = pd.DataFrame(df_colors)
    
    return(df_colors)

# return dictionary with chart data
def build_chart(labels_pds, labels_freq, data_first_dict, data_sec_dict = {}):
    
    # dependecies
    import pandas as pd
    import numpy as np
    
    if len(pd.DataFrame(labels_pds).select_dtypes(include=[np.datetime64]).columns) > 0:
    
        # create labels at specified frequency
        labels = (
                (100 + labels_pds.dt.day).astype(str).str[1:3]
                + ' '
                + labels_pds.dt.month_name(locale = 'it').str[:3].str.lower()
            )
        
    else:
        
        labels = labels_pds.str.title()

    i = ((pd.Series(list(range(0, len(labels)))) + 1) % labels_freq) != 0

    if i.sum() > 0:
        labels[i] = ''
    
    if 'bordercolor' not in data_first_dict:
        
        data_first_dict['bordercolor'] = data_first_dict['backgroundcolor']            
    
    # create dictionary with chart data
    if (len(data_sec_dict) > 0):
                
        if 'bordercolor' not in data_sec_dict:
            
            data_sec_dict['bordercolor'] = data_sec_dict['backgroundcolor']        
        
        data_out = {
                    'labels': labels.tolist()
                    ,'data_first': data_first_dict['data']
                    ,'backgroundcolor_first': data_first_dict['backgroundcolor']
                    ,'bordercolor_first': data_first_dict['bordercolor']
                    ,'label_first': data_first_dict['label']
                    ,'data_sec': data_sec_dict['data']
                    ,'label_sec': data_sec_dict['label']
                    ,'backgroundcolor_sec': data_sec_dict['backgroundcolor']
                    ,'bordercolor_sec': data_sec_dict['bordercolor']                
                }
    else :
        
        data_out = {
                    'labels': labels.tolist()
                    ,'data_first': data_first_dict['data']
                    ,'backgroundcolor_first': data_first_dict['backgroundcolor']
                    ,'bordercolor_first': data_first_dict['bordercolor']
                    ,'label_first': data_first_dict['label']              
                }
    
    return(data_out)       
    

def build_charts_shared(df):
    
    # dependecies
    import numpy as np
    from palettable.colorbrewer.sequential import Reds_9 as palettable_pal_red
    from palettable.colorbrewer.sequential import Greens_9 as palettable_pal_green
    from palettable.colorbrewer.sequential import Blues_9 as palettable_pal_blue
    from palettable.colorbrewer.sequential import RdPu_9 as palettable_pal_redpurple
    from palettable.colorbrewer.sequential import Purples_9 as palettable_pal_purple     
    
    # perc tamponi positivi
    pds = df['nuovi_positivi'].divide(df['nuovi_tamponi']).replace(np.inf, 0) * 100.0
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_perc_tamponi_positivi = build_chart(
                                        labels_pds = df['data']
                                        ,labels_freq = 1
                                        ,data_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Percentuale Tamponi Positivi'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                        }
                                    
                                    )    
    
    # nuovi positivi
    pds = df['nuovi_positivi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_nuovi_positivi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Nuovi Positivi'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )

    # nuovi tamponi
    pds = df['nuovi_tamponi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_blue}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_nuovi_tamponi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Nuovi Tamponi'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # attualmente positivi
    pds = df['totale_positivi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_att_positivi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Attualmente Positivi'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # variazione attualmente positivi
    pds = df['variazione_totale_positivi']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red, 'opt': palettable_pal_green}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_var_att_positivi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Variazione Att. Positivi'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # nuovi deceduti
    pds = df['nuovi_deceduti']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_decessi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Decessi'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # nuovi guariti
    pds = df['nuovi_dimessi_guariti']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_green}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_dimessi = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Dimessi Guariti'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # terapia intensiva
    pds = df['terapia_intensiva']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_redpurple}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_ter_intensiva = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Terapia Intensiva'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )
    
    # totale ospedalizzati
    pds = df['totale_ospedalizzati']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_purple}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    chart_ospedalizzati = build_chart(
                                    labels_pds = df['data']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Ospedalizzati'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    
                                )     

    # dictionary with all shared charts
    charts_dict = {
                 'chart_perc_tamponi_positivi': chart_perc_tamponi_positivi
                ,'chart_nuovi_positivi': chart_nuovi_positivi
                ,'chart_nuovi_tamponi': chart_nuovi_tamponi
                ,'chart_att_positivi': chart_att_positivi
                ,'chart_var_att_positivi': chart_var_att_positivi
                ,'chart_decessi': chart_decessi
                ,'chart_dimessi': chart_dimessi
                ,'chart_ter_intensiva': chart_ter_intensiva
                ,'chart_ospedalizzati': chart_ospedalizzati
                }

    return(charts_dict)    


# build a dictionary with charts data    
def build_charts_index(df_naz, df_reg, dir_home):
       
    # dependecies
    import pandas as pd
    from palettable.colorbrewer.sequential import Reds_9 as palettable_pal_red
    
    # add new columns
    df_naz = df_naz.sort_values(by = ['data', 'stato'])
    df_naz['nuovi_deceduti'] = df_naz['deceduti'] - df_naz['deceduti'].shift(+1)
    df_naz['nuovi_dimessi_guariti'] = df_naz['dimessi_guariti'] - df_naz['dimessi_guariti'].shift(+1)
    df_naz['nuovi_tamponi'] = df_naz['tamponi'] - df_naz['tamponi'].shift(+1)
    
    # filter dates
    i = df_naz['data'] > pd.to_datetime('2020-03-01')
    df_naz = df_naz.loc[i, :]
    
    # shared charts
    charts_dict = build_charts_shared(df = df_naz)
    
    # retrieve last available data from regions
    i = df_reg['data'] == df_reg['data'].max()
    df_reg = df_reg.loc[i, :].groupby(['codice_regione']).sum()
    df_reg.reset_index(inplace = True)
    
    # read populations csv
    pop = pd.read_csv(filepath_or_buffer = dir_home + r'\data_raw\csv\popolazione_regioni_20190101_istat.csv'
                      ,sep = ','
                      ,header = 0)
    
    df_reg = df_reg.merge(right = pop
                          ,how = 'left'
                          ,on = 'codice_regione'
                          )    
        
    # calculated column
    df_reg['totale_positivi_perc'] = (df_reg['totale_positivi'] / df_reg['popolazione'])*100.0
    
    df_reg = df_reg.sort_values(by = ['totale_positivi'], ascending = False)

    # attualmente positivi per regione
    pds = df_reg['totale_positivi']
    pds2 = df_reg['totale_positivi_perc']
    
    df_col = get_colors(
                     pds = pds
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )
    
    df_col2 = get_colors(
                     pds = pds2
                    ,palettable_pal = {'main': palettable_pal_red}
                    ,scale_logic = 'max perc'
                    ,opacity = 0.8
                    ,opacity_border = 1
                    )    
    
    chart_att_positivi_reg = build_chart(
                                    labels_pds = df_reg['regione']
                                    ,labels_freq = 1
                                    ,data_first_dict = {'data': pds.tolist()
                                                    ,'label': 'Attualmente Positivi (% Popolazione)'
                                                    ,'backgroundcolor': df_col['rgba'].tolist()
                                                    ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                    }
                                    ,data_sec_dict = {'data': pds2.tolist()
                                                    ,'label': 'Attualmente Positivi'
                                                    ,'backgroundcolor': df_col2['rgba'].tolist()
                                                    ,'bordercolor': df_col2['rgba_border_fixed'].tolist()
                                                    }
                                ) 
    
    # table summary
    i = df_naz['data'] == df_naz['data'].max()    
    df_naz = df_naz.loc[i, :]
    df_naz['ult_aggiornamento'] = (100 + df_naz['data'].dt.day).astype(str).str.slice(1,3) + r'/' + (100 + df_naz['data'].dt.month).astype(str).str.slice(1,3) + r'/' + (df_naz['data'].dt.year).astype(str)    
    table_summary = {'att_positivi': df_naz['totale_positivi'].tolist()
                    ,'tot_casi': df_naz['totale_casi'].tolist()
                    ,'tot_tamponi': df_naz['tamponi'].tolist()
                    ,'tot_decessi': df_naz['deceduti'].tolist()
                    ,'tot_dimessi': df_naz['dimessi_guariti'].tolist()
                    ,'popolazione': pop['popolazione'].sum().tolist()
                    ,'ult_aggiornamento': df_naz['ult_aggiornamento'].tolist()
                    }
    
    # add index charts to dictionary
    charts_dict['table_summary'] = table_summary
    charts_dict['chart_att_positivi_reg'] = chart_att_positivi_reg
    charts_dict['area'] = {'suffix': pd.Series('Italia').tolist()}
    
    return(charts_dict)    
    
    
# build a dictionary with charts data    
def build_charts_reg(df_reg, df_prov, dir_home):
       
    # dependecies
    import pandas as pd
    from palettable.colorbrewer.sequential import Reds_9 as palettable_pal_red
    
    # add new columns
    df_reg = df_reg.groupby(['stato', 'codice_regione', 'data']).sum()
    df_reg.reset_index(inplace = True)
   
    # retrieve last available data from province
    i = df_prov['data'] == df_prov['data'].max()
    df_prov = df_prov.loc[i, :].groupby(['codice_regione', 'codice_provincia']).sum()
    df_prov.reset_index(inplace = True)
    
    # read populations csv
    pop = pd.read_csv(filepath_or_buffer = dir_home + r'\data_raw\csv\popolazione_province_20190101_istat.csv'
                      ,sep = ','
                      ,header = 0)        
    
    df_prov = df_prov.merge(right = pop
                          ,how = 'left'
                          ,on = 'codice_provincia'
                          ,suffixes = ('', '_pop')
                          )    
            
    # calculated column
    df_prov['totale_casi_perc'] = (df_prov['totale_casi'] / df_prov['popolazione'])*100.0
    
    # build charts for every region
    reg_list = df_reg['codice_regione'].unique()
    charts_dict = {}
    
    for reg in reg_list:

        # filter a region
        i = df_reg['codice_regione'] == reg
        df_reg_temp = df_reg.loc[i, :].copy()
        
        i = df_prov['codice_regione'] == reg
        df_prov_temp = df_prov.loc[i, :].copy()
        
        i = pop['codice_regione'] == reg
        pop_temp = pop.loc[i, :].copy()
        
        # calculated columns
        df_reg_temp = df_reg_temp.sort_values(by = ['stato', 'codice_regione', 'data'])    
        df_reg_temp['nuovi_deceduti'] = df_reg_temp['deceduti'] - df_reg_temp['deceduti'].shift(+1)
        df_reg_temp['nuovi_dimessi_guariti'] = df_reg_temp['dimessi_guariti'] - df_reg_temp['dimessi_guariti'].shift(+1)
        df_reg_temp['nuovi_tamponi'] = df_reg_temp['tamponi'] - df_reg_temp['tamponi'].shift(+1)
    
        # filter dates
        i = df_reg_temp['data'] > pd.to_datetime('2020-03-01')
        df_reg_temp = df_reg_temp.loc[i, :]
        
        # shared charts
        charts_dict_temp = build_charts_shared(df = df_reg_temp)
        
        # province        
        df_prov_temp = df_prov_temp.sort_values(by = ['totale_casi'], ascending = False)
    
        # attualmente positivi per provincia
        pds = df_prov_temp['totale_casi']
        pds2 = df_prov_temp['totale_casi_perc']
        
        df_col = get_colors(
                         pds = pds
                        ,palettable_pal = {'main': palettable_pal_red}
                        ,scale_logic = 'max perc'
                        ,opacity = 0.8
                        ,opacity_border = 1
                        )
        
        df_col2 = get_colors(
                         pds = pds2
                        ,palettable_pal = {'main': palettable_pal_red}
                        ,scale_logic = 'max perc'
                        ,opacity = 0.8
                        ,opacity_border = 1
                        )    
        
        chart_tot_casi_prov = build_chart(
                                        labels_pds = df_prov_temp['provincia']
                                        ,labels_freq = 1
                                        ,data_first_dict = {'data': pds.tolist()
                                                        ,'label': 'Totale Casi (% Popolazione)'
                                                        ,'backgroundcolor': df_col['rgba'].tolist()
                                                        ,'bordercolor': df_col['rgba_border_fixed'].tolist()
                                                        }
                                        ,data_sec_dict = {'data': pds2.tolist()
                                                        ,'label': 'Totale Casi'
                                                        ,'backgroundcolor': df_col2['rgba'].tolist()
                                                        ,'bordercolor': df_col2['rgba_border_fixed'].tolist()
                                                        }
                                    ) 
        
        # table summary
        i = df_reg_temp['data'] == df_reg_temp['data'].max()    
        df_reg_temp = df_reg_temp.loc[i, :]
        df_reg_temp['ult_aggiornamento'] = (100 + df_reg_temp['data'].dt.day).astype(str).str.slice(1,3) + r'/' + (100 + df_reg_temp['data'].dt.month).astype(str).str.slice(1,3) + r'/' + (df_reg_temp['data'].dt.year).astype(str)    
        table_summary = {'att_positivi': df_reg_temp['totale_positivi'].tolist()
                        ,'tot_casi': df_reg_temp['totale_casi'].tolist()
                        ,'tot_tamponi': df_reg_temp['tamponi'].tolist()
                        ,'tot_decessi': df_reg_temp['deceduti'].tolist()
                        ,'tot_dimessi': df_reg_temp['dimessi_guariti'].tolist()
                        ,'popolazione': pop_temp['popolazione'].sum().tolist()
                        ,'ult_aggiornamento': df_reg_temp['ult_aggiornamento'].tolist()                        
                        }
        
        # add index charts to dictionary
        charts_dict_temp['table_summary'] = table_summary
        charts_dict_temp['chart_tot_casi_prov'] = chart_tot_casi_prov
        charts_dict_temp['area'] = {'suffix': pop_temp['regione'].unique().tolist()}
        
        # add region dictionary to main dictionary
        charts_dict[reg] = charts_dict_temp  

    
    return(charts_dict)    



# return geo dataframe
def build_geomap_reg(df, dir_home, col_value):

    # dependecies
    import pandas as pd
    import geopandas as gpd
    #from palettable.colorbrewer.sequential import YlOrRd_9 as palettable_pal
    from palettable.colorbrewer.sequential import Reds_9 as palettable_pal
      
    # retrieve last available data from regions
    i = df['data'] == df['data'].max()
    df = df.loc[i, :].groupby(['codice_regione']).sum()
    df.reset_index(inplace = True)
    
    # read geojson
    gdf = gpd.read_file(dir_home + r'\data_geo\geojson_leaflet\ita_regions.geojson')
    
    # read populations csv
    pop = pd.read_csv(filepath_or_buffer = dir_home + r'\data_raw\csv\popolazione_regioni_20190101_istat.csv'
                      ,sep = ','
                      ,header = 0)
    
    # merge geojson and regions data
    gdf = gdf.merge(right = df
                    ,how = 'left'
                    ,left_on = 'reg_istat_code_num'
                    ,right_on = 'codice_regione'
                    )
    
    gdf = gdf.merge(right = pop
                    ,how = 'left'
                    ,left_on = 'reg_istat_code_num'
                    ,right_on = 'codice_regione'
                    ,suffixes = ('', '_pop')
                    )    
        
    # calculated column
    gdf[col_value + '_perc'] = (gdf[col_value] / gdf['popolazione']) * 100.0

    # series to display with clorophlet map
    pds = gdf[col_value + '_perc']
    
    # get color palette
    df_col = get_colors(pds = pds
                        ,palettable_pal = {'main': palettable_pal}
                        ,scale_logic = 'max perc'                                     
                        )    
    
    # add hex colors
    gdf['hex_color'] = df_col['hex']
       
    # reorder and rename geo dataframe columns   
    col_names = [
             'codice_regione'
            ,'regione'            
            ,'hex_color'
            ,col_value
            ,col_value + '_perc'
            ,'popolazione'
            ,'terapia_intensiva'
            ,'totale_casi'
            ,'tamponi'
            ,'deceduti'
            ,'dimessi_guariti'
            ,'geometry'
        ]
        
    gdf = gdf.loc[:,gdf.columns.intersection(col_names)]
    gdf = gdf.loc[:, col_names]
    gdf.rename(columns = {'deceduti': 'decessi'}, inplace = True)
    
    # return geo dataframe
    return(gdf)


# return geo dataframe
def build_geomap_prov(df_prov, df_reg, dir_home, col_value):

    # dependecies
    import pandas as pd
    import geopandas as gpd
    #from palettable.colorbrewer.sequential import YlOrRd_9 as palettable_pal
    from palettable.colorbrewer.sequential import Reds_9 as palettable_pal
      
    # retrieve last available data from province
    i = df_prov['data'] == df_prov['data'].max()
    df_prov = df_prov.loc[i, :].groupby(['codice_regione', 'codice_provincia']).sum()
    df_prov.reset_index(inplace = True)
       
    i = df_reg['data'] == df_reg['data'].max()
    df_reg = df_reg.loc[i, :].groupby(['codice_regione']).mean()
    df_reg.reset_index(inplace = True)
   
    # read geojson
    gdf = gpd.read_file(dir_home + r'\data_geo\geojson_leaflet\ita_provinces.geojson')
    
    # read populations csv
    pop = pd.read_csv(filepath_or_buffer = dir_home + r'\data_raw\csv\popolazione_province_20190101_istat.csv'
                      ,sep = ','
                      ,header = 0)
    
    # merge geojson and regions data
    gdf = gdf.merge(right = df_prov
                    ,how = 'left'
                    ,left_on = 'prov_istat_code_num'
                    ,right_on = 'codice_provincia'
                    )
    
    gdf = gdf.merge(right = pop
                    ,how = 'left'
                    ,left_on = 'prov_istat_code_num'
                    ,right_on = 'codice_provincia'
                    ,suffixes = ('', '_pop')
                    )    
        
    # calculated column
    gdf[col_value + '_perc'] = (gdf[col_value] / gdf['popolazione']) * 100.0

    # build charts for every region
    reg_list = df_reg['codice_regione'].unique()
    charts_dict = {}
    
    for reg in reg_list:

        # filter a region
        i = gdf.loc[:,'codice_regione'] == reg
        gdf_temp = gdf.loc[i, :].copy()
        
        # get color palette
        df_col = get_colors(pds = gdf_temp[col_value + '_perc']
                            ,palettable_pal = {'main': palettable_pal}
                            ,scale_logic = 'max perc'                                     
                            )
                  
        gdf_temp['hex_color'] = df_col['hex']
        
        # reorder and rename geo dataframe columns   
        col_names = [
                 'codice_regione'
                ,'regione'          
                ,'codice_provincia'
                ,'provincia'
                ,'hex_color'
                ,col_value
                ,col_value + '_perc'
                ,'popolazione'
                ,'geometry'
            ]
            
        gdf_temp = gdf_temp.loc[:, gdf_temp.columns.intersection(col_names)]
        gdf_temp = gdf_temp.loc[:, col_names]    
                
        charts_dict[reg] = gdf_temp
    
    # return geo dataframe
    return(charts_dict)    
    

def write_geojson(gdf, pathfilename):
    
    # write geojson
    gdf.to_file(pathfilename, driver='GeoJSON')
    
    
# write geo dataframe    
def write_geojson_data(obj, pathfilename, split_key):
                    
    if (split_key):
        
        for dict_key in obj:
                        
            write_geojson(obj[dict_key], pathfilename + '\\' + str(dict_key) + '.geojson')
        
    else:
        
      write_geojson(obj, pathfilename)
        
        

# write dictionary to json file
def write_json(charts_dict, pathfilename):
    
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


# write dictionary to json file
def write_charts_data(charts_dict, pathfilename, split_key = False):
        
    if (split_key):
        
        for dict_key in charts_dict:
            
            write_json(charts_dict = charts_dict[dict_key], pathfilename = pathfilename + '\\' + str(dict_key) + '.json')
        
    else:
        
      write_json(charts_dict = charts_dict, pathfilename = pathfilename)
           
