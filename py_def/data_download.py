# read configuration files
def get_config(dir_home, sep, header):

	# dependecies
	import csv

	# url master
	with open(file = dir_home + r'\data_cfg\repo_master.csv') as file_toread:
		
		file_reader = csv.reader(file_toread, delimiter = sep)
		file_header = header
		
		if(file_header):
			next(file_reader)
			file_header = False
		
		for row in file_reader:
			url_home = row[0]      

	# url files
	with open(file = dir_home + r'\data_cfg\repo_master_files.csv') as file_toread:
		
		file_reader = csv.reader(file_toread, delimiter = sep)
		file_header = header
		
		if(file_header):
			next(file_reader)
			file_header = False
		
		url_files = {}
		for row in file_reader:

			if(row[0] not in url_files):
				url_files[row[0]] = {}

			url_files[row[0]][row[1]] = {'file_url': url_home + row[2], 'file_disk': dir_home + row[3]}

	return url_files



# download and save data to local disk
def get_data(diz_files):
    # dependecies
    import urllib

    for diz_key in diz_files:
    
        diz_file = diz_files[diz_key]            
        urllib.request.urlretrieve(url = diz_file['file_url'], filename = diz_file['file_disk'])





    
    