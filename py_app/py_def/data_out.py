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

	labels[i] = ''

	# create dictionary with chart data
	if(len(y_sec_dict) > 0):
		data_out = {
				'labels': labels.tolist()
				,'data_first': y_first_dict['data']
				,'label_first': y_first_dict['label']
				,'data_sec': y_sec_dict['data']
				,'label_sec': y_sec_dict['label']
			}
	else :
		data_out = {
				'labels': labels.tolist()
				,'data_first': y_first_dict['data']
				,'label_first': y_first_dict['label']
			}
	
	return(data_out)
		
	
	
# build a dictionary with charts data	
def build_charts_naz(df):
	
	# add new columns
	df = df.sort_values(by = ['data', 'stato'])
	df['nuovi_deceduti'] = df['deceduti'] - df['deceduti'].shift(+1)
	df['nuovi_dimessi_guariti'] = df['dimessi_guariti'] - df['dimessi_guariti'].shift(+1)	  
	df['nuovi_tamponi'] = df['tamponi'] - df['tamponi'].shift(+1)
	
	# build charts
	chart_a = build_linechart_dates(x_pds_dt = df['data']
									,x_freq = 2
									,y_first_dict = {'data': df['nuovi_attualmente_positivi'].tolist(), 'label': 'Nuovi Positivi'}
									,y_sec_dict = {'data': df['nuovi_tamponi'].tolist(), 'label': 'Nuovi Tamponi'}
									)

	chart_b = build_linechart_dates(x_pds_dt = df['data']
									,x_freq = 2
									,y_first_dict = {'data': df['totale_attualmente_positivi'].tolist(), 'label': 'Attualmente Positivi'}									
									)

	chart_c = build_linechart_dates(x_pds_dt = df['data']
									,x_freq = 2
									,y_first_dict = {'data': df['terapia_intensiva'].tolist(), 'label': 'Terapia Intensiva'}
									)

	chart_d = build_linechart_dates(x_pds_dt = df['data']
									,x_freq = 2
									,y_first_dict = {'data': df['nuovi_deceduti'].tolist(), 'label': 'Deceduti'}
									,y_sec_dict = {'data': df['nuovi_dimessi_guariti'].tolist(), 'label': 'Dimessi Guariti'}
									)
	
	# dictionary with all charts
	charts_dict = {
				 'chart_a': chart_a
				,'chart_b': chart_b
				,'chart_c': chart_c
				,'chart_d': chart_d
				}

	return(charts_dict)
	
	
	
# write dictionary to json file
def write_charts_data(charts_dict, pathfilename):

	# dependecies
	import json
	
	# write json
	with open(file = pathfilename, mode = 'w') as file_towrite:	
		
		json.dump(obj = charts_dict, fp = file_towrite)	

	