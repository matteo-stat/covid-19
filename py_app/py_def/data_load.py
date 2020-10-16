# load data
def load_data(path, get_last_year = True, fix_reg = False):
	
	# dependecies
	import pandas as pd
	
	# read downloaded data
	df = pd.read_csv(filepath_or_buffer = path
					,sep = ','
					,header = 0)

	# convert ISO8601 to datetime
	df['data'] = pd.to_datetime(df['data'])

	# filter data to last available year
	if(get_last_year):
		# filter data to last avail year
		i = df['data'].dt.year == df['data'].dt.year.max()
		df = df.loc[i, ]
	
	# fix regions code
	if(fix_reg):
		df['codice_regione'].replace(to_replace = [21,22], value = 4, inplace = True)        

	return(df)