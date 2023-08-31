import os
import pandas as pd
import numpy as np

mean_time, exposure = [], []
lon_mean, lat_mean, delta_lat, alt_mean = [], [], [], []
cps_0_64, cps_64_128, cps_128_192, cps_192_256 = [], [], [], []
sat = []

## different sbins
path_list_4 = []
path_list_8 = []
path_list_16 = []
path_list_32 = []

file_name = 'rate_multi_ch.txt'
path_base = r'/space/GRBAlpha/processed_data/IDL/Data_firmware_2'
for dirname in os.listdir(path_base):
	if np.logical_or('2021' in dirname,'2022' in dirname):
		if ('sbin4' in dirname):
			path_list_4.append(path_base + '/' + dirname + '/')
		elif ('sbin8' in dirname):
			path_list_8.append(path_base + '/' + dirname + '/')
		elif ('sbin16' in dirname):
			path_list_16.append(path_base + '/' + dirname + '/')
		elif ('sbin32' in dirname):
			path_list_32.append(path_base + '/' + dirname + '/')

path_base = r'/space/GRBAlpha/processed_data/IDL/Data_firmware_3'
for dirname in os.listdir(path_base):
	if np.logical_or('2022' in dirname,'2023' in dirname):
		if ('sbin4' in dirname):
			path_list_4.append(path_base + '/' + dirname + '/')
		elif ('sbin8' in dirname):
			path_list_8.append(path_base + '/' + dirname + '/')
		elif ('sbin16' in dirname):
			path_list_16.append(path_base + '/' + dirname + '/')
		elif ('sbin32' in dirname):
			path_list_32.append(path_base + '/' + dirname + '/')

#path_base = r'/space/vzlusat2/processed_data/IDL/Data_firmware_initial'
#for dirname in os.listdir(path_base):
#    if np.logical_or('2022' in dirname,'2023' in dirname):
#        if ('sbin4' in dirname):
#            path_list_4.append(path_base + '/' + dirname + '/')
#        elif ('sbin8' in dirname):
#            path_list_8.append(path_base + '/' + dirname + '/')
#        elif ('sbin16' in dirname):
#            path_list_16.append(path_base + '/' + dirname + '/')
#        elif ('sbin32' in dirname):
#            path_list_32.append(path_base + '/' + dirname + '/')

## removing unwanted directories - wrong timestamps
path_list_4 = [x for x in path_list_4 if '2021-04-25' not in x]
path_list_4 = [x for x in path_list_4 if '2021-05-12' not in x]
path_list_4 = [x for x in path_list_4 if '2021-05-23' not in x]
path_list_4 = [x for x in path_list_4 if '2021-06-30' not in x]
path_list_4 = [x for x in path_list_4 if '2022-02-16-18' not in x]
#path_list_4 = [x for x in path_list_4 if '2022-09-03_22-26-06' not in x]
#path_list_4 = [x for x in path_list_4 if '2022-04-21_21-01-40' not in x]
#path_list_4 = [x for x in path_list_4 if '2022-11-10_04-41-35' not in x]
path_list_4 = [x for x in path_list_4 if 'combined' not in x]

## removing unwanted directories - different sbins; exp120s
path_list_8 = [x for x in path_list_8 if '2021-04-15_23-53-42' not in x]
path_list_8 = [x for x in path_list_8 if '2021-04-16_10-45-42' not in x]

## sbin4
for path in path_list_4:
	if np.logical_and('ch0' in os.listdir(path),'ch1' in os.listdir(path)):
		ch_list = ['ch0','ch1']
	elif np.logical_and('ch0' in os.listdir(path),'ch2' in os.listdir(path)):
		ch_list = ['ch0','ch2']
	elif ('ch2' in os.listdir(path)):
		ch_list = ['ch2']
	elif ('ch1' in os.listdir(path)):
		ch_list = ['ch1']
	else:
		ch_list = ['ch0'] 
	
	for channel in ch_list:
		new_path = path + channel + '/'
		for name in os.listdir(new_path):
			if os.path.isdir(new_path + name):
				if np.logical_and(np.logical_and('part' in name,'HV' not in name), file_name in os.listdir(new_path + name)):
					temp_path = new_path + name + '/' + file_name
					#print(temp_path)
					temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
					for j in range(len(temp_data)):
						try:
							temp_data['lon_end'][j] = float(temp_data['lon_end'][j]) 
							temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
						except:
							continue
						mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
															pd.to_datetime(temp_data['exp_end_time'][j])))))
						exposure.append(temp_data['exposure(s)'][j])
						# temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
						# temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
						delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
						# crossing prime meridian
						if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
							delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
							if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
								elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
							elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
								elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
						else:
							lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
						lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
						alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
						if ('Data_firmware_3' in temp_path):
							cps_0_64.append(temp_data['cps_band000'][j])
							cps_64_128.append(temp_data['cps_band001'][j])
							cps_128_192.append(temp_data['cps_band002'][j])
							cps_192_256.append(temp_data['cps_band003'][j])
						else:
							cps_0_64.append(temp_data['cps_band0'][j])
							cps_64_128.append(temp_data['cps_band1'][j])
							cps_128_192.append(temp_data['cps_band2'][j])
							cps_192_256.append(temp_data['cps_band3'][j])
						sat.append(path[7:15])
			elif (name == file_name):
				temp_path = new_path + name 
				#print(temp_path)
				temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
				for j in range(len(temp_data)):
					try:
						temp_data['lon_end'][j] = float(temp_data['lon_end'][j]) 
						temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
					except:
						continue
					mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
														pd.to_datetime(temp_data['exp_end_time'][j])))))
					exposure.append(temp_data['exposure(s)'][j])
					# temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
					# temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
					delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
					# crossing prime meridian
					if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
						delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
						if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
							if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
							elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
						elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
							if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
							elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
					else:
						lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
					lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
					alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
					if ('Data_firmware_3' in temp_path):
						cps_0_64.append(temp_data['cps_band000'][j])
						cps_64_128.append(temp_data['cps_band001'][j])
						cps_128_192.append(temp_data['cps_band002'][j])
						cps_192_256.append(temp_data['cps_band003'][j])
					else:
						cps_0_64.append(temp_data['cps_band0'][j])
						cps_64_128.append(temp_data['cps_band1'][j])
						cps_128_192.append(temp_data['cps_band2'][j])
						cps_192_256.append(temp_data['cps_band3'][j])
					sat.append(path[7:15])

## sbin8 
for path in path_list_8:
	if np.logical_and('ch0' in os.listdir(path),'ch1' in os.listdir(path)):
		ch_list = ['ch0','ch1']
	elif np.logical_and('ch0' in os.listdir(path),'ch2' in os.listdir(path)):
		ch_list = ['ch0','ch2']
	elif ('ch2' in os.listdir(path)):
		ch_list = ['ch2']
	elif ('ch1' in os.listdir(path)):
		ch_list = ['ch1']
	else:
		ch_list = ['ch0'] 
	
	for channel in ch_list:
		new_path = path + channel + '/'
		for name in os.listdir(new_path):
			if os.path.isdir(new_path + name):
				if np.logical_and('part' in name,file_name in os.listdir(new_path + name)):
					temp_path = new_path + name + '/' + file_name
					#print(temp_path)
					temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
					for j in range(len(temp_data)):
						mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
															pd.to_datetime(temp_data['exp_end_time'][j])))))
						exposure.append(temp_data['exposure(s)'][j])
						#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
						#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
						delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
						# crossing prime meridian
						if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
							delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
							if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
								elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
							elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
								elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
						else:
							lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
						lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
						alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
						if ('Data_firmware_3' in temp_path):
							cps_0_64.append(temp_data['cps_band001'][j])
							cps_64_128.append(temp_data['cps_band002'][j]+temp_data['cps_band003'][j])
							cps_128_192.append(temp_data['cps_band004'][j]+temp_data['cps_band005'][j])
							cps_192_256.append(temp_data['cps_band006'][j]+temp_data['cps_band007'][j])
						else:
							cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j])
							cps_64_128.append(temp_data['cps_band2'][j]+temp_data['cps_band3'][j])
							cps_128_192.append(temp_data['cps_band4'][j]+temp_data['cps_band5'][j])
							cps_192_256.append(temp_data['cps_band6'][j]+temp_data['cps_band7'][j])
						sat.append(path[7:15])
			elif (name == file_name):
				temp_path = new_path + name 
				#print(temp_path)
				temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
				for j in range(len(temp_data)):
					mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
														pd.to_datetime(temp_data['exp_end_time'][j])))))
					exposure.append(temp_data['exposure(s)'][j])
					#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
					#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
					delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
					# crossing prime meridian
					if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
						delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
						if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
							if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
							elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
						elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
							if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
							elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
					else:
						lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
					lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
					alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
					if ('Data_firmware_3' in temp_path):
						cps_0_64.append(temp_data['cps_band001'][j])
						cps_64_128.append(temp_data['cps_band002'][j]+temp_data['cps_band003'][j])
						cps_128_192.append(temp_data['cps_band004'][j]+temp_data['cps_band005'][j])
						cps_192_256.append(temp_data['cps_band006'][j]+temp_data['cps_band007'][j])
					else:
						cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j])
						cps_64_128.append(temp_data['cps_band2'][j]+temp_data['cps_band3'][j])
						cps_128_192.append(temp_data['cps_band4'][j]+temp_data['cps_band5'][j])
						cps_192_256.append(temp_data['cps_band6'][j]+temp_data['cps_band7'][j])
					sat.append(path[7:15])

## sbin16
for path in path_list_16:
	if np.logical_and('ch0' in os.listdir(path),'ch1' in os.listdir(path)):
		ch_list = ['ch0','ch1']
	elif np.logical_and('ch0' in os.listdir(path),'ch2' in os.listdir(path)):
		ch_list = ['ch0','ch2']
	elif ('ch2' in os.listdir(path)):
		ch_list = ['ch2']
	elif ('ch1' in os.listdir(path)):
		ch_list = ['ch1']
	else:
		ch_list = ['ch0'] 
	
	for channel in ch_list:
		new_path = path + channel + '/'
		for name in os.listdir(new_path):
			if os.path.isdir(new_path + name):
				if np.logical_and('part' in name,file_name in os.listdir(new_path + name)):
					temp_path = new_path + name + '/' + file_name
					#print(temp_path)
					temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
					for j in range(len(temp_data)):
						mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
															pd.to_datetime(temp_data['exp_end_time'][j])))))
						exposure.append(temp_data['exposure(s)'][j])
						#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
						#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
						delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
						# crossing prime meridian
						if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
							delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
							if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
								elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
							elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
								elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
						else:
							lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
						lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
						alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
						if ('Data_firmware_3' in temp_path):
							cps_0_64.append(temp_data['cps_band000'][j]+temp_data['cps_band001'][j]+
											  temp_data['cps_band002'][j]+temp_data['cps_band003'][j])
							cps_64_128.append(temp_data['cps_band004'][j]+temp_data['cps_band005'][j]+
											  temp_data['cps_band006'][j]+temp_data['cps_band007'][j])
							cps_128_192.append(temp_data['cps_band008'][j]+temp_data['cps_band009'][j]+
											   temp_data['cps_band010'][j]+temp_data['cps_band011'][j])
							cps_192_256.append(temp_data['cps_band012'][j]+temp_data['cps_band013'][j]+
											   temp_data['cps_band014'][j]+temp_data['cps_band015'][j])
						else:
							cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j]+
											  temp_data['cps_band2'][j]+temp_data['cps_band3'][j])
							cps_64_128.append(temp_data['cps_band4'][j]+temp_data['cps_band5'][j]+
											  temp_data['cps_band6'][j]+temp_data['cps_band7'][j])
							cps_128_192.append(temp_data['cps_band8'][j]+temp_data['cps_band9'][j]+
											   temp_data['cps_band10'][j]+temp_data['cps_band11'][j])
							cps_192_256.append(temp_data['cps_band12'][j]+temp_data['cps_band13'][j]+
											   temp_data['cps_band14'][j]+temp_data['cps_band15'][j])
						sat.append(path[7:15])
			elif (name == file_name):
				temp_path = new_path + name 
				#print(temp_path)
				temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
				for j in range(len(temp_data)):
					mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
														pd.to_datetime(temp_data['exp_end_time'][j])))))
					exposure.append(temp_data['exposure(s)'][j])
					#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
					#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
					delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
					# crossing prime meridian
					if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
						delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
						if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
							if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
							elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
						elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
							if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
							elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
					else:
						lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
					lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
					alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
					if ('Data_firmware_3' in temp_path):
						cps_0_64.append(temp_data['cps_band003'][j])
						cps_64_128.append(temp_data['cps_band004'][j]+temp_data['cps_band005'][j]+
										  temp_data['cps_band006'][j]+temp_data['cps_band007'][j])
						cps_128_192.append(temp_data['cps_band008'][j]+temp_data['cps_band009'][j]+
										   temp_data['cps_band010'][j]+temp_data['cps_band011'][j])
						cps_192_256.append(temp_data['cps_band012'][j]+temp_data['cps_band013'][j]+
										   temp_data['cps_band014'][j]+temp_data['cps_band015'][j])
					else:
						cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j]+
											  temp_data['cps_band2'][j]+temp_data['cps_band3'][j])
						cps_64_128.append(temp_data['cps_band4'][j]+temp_data['cps_band5'][j]+
										  temp_data['cps_band6'][j]+temp_data['cps_band7'][j])
						cps_128_192.append(temp_data['cps_band8'][j]+temp_data['cps_band9'][j]+
										   temp_data['cps_band10'][j]+temp_data['cps_band11'][j])
						cps_192_256.append(temp_data['cps_band12'][j]+temp_data['cps_band13'][j]+
										   temp_data['cps_band14'][j]+temp_data['cps_band15'][j])
					sat.append(path[7:15])

## sbin32
for path in path_list_32:
	if np.logical_and('ch0' in os.listdir(path),'ch1' in os.listdir(path)):
		ch_list = ['ch0','ch1']
	elif np.logical_and('ch0' in os.listdir(path),'ch2' in os.listdir(path)):
		ch_list = ['ch0','ch2']
	elif ('ch2' in os.listdir(path)):
		ch_list = ['ch2']
	elif ('ch1' in os.listdir(path)):
		ch_list = ['ch1']
	else:
		ch_list = ['ch0'] 
	
	for channel in ch_list:
		new_path = path + channel + '/'
		for name in os.listdir(new_path):
			if os.path.isdir(new_path + name):
				if np.logical_and('part' in name,file_name in os.listdir(new_path + name)):
					temp_path = new_path + name + '/' + file_name
					#print(temp_path)
					temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
					for j in range(len(temp_data)):
						mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
															pd.to_datetime(temp_data['exp_end_time'][j])))))
						exposure.append(temp_data['exposure(s)'][j])
						#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
						#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
						delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
						# crossing prime meridian
						if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
							delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
							if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
								elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
							elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
								elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
									lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
						else:
							lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
						lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
						alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
						if ('Data_firmware_3' in temp_path):
							cps_0_64.append(temp_data['cps_band000'][j]+temp_data['cps_band001'][j]+
											  temp_data['cps_band002'][j]+temp_data['cps_band003'][j]+
											  temp_data['cps_band004'][j]+temp_data['cps_band005'][j]+
											  temp_data['cps_band005'][j]+temp_data['cps_band006'][j])
							cps_64_128.append(temp_data['cps_band008'][j]+temp_data['cps_band009'][j]+
											  temp_data['cps_band010'][j]+temp_data['cps_band011'][j]+
											  temp_data['cps_band012'][j]+temp_data['cps_band013'][j]+
											  temp_data['cps_band014'][j]+temp_data['cps_band015'][j])
							cps_128_192.append(temp_data['cps_band016'][j]+temp_data['cps_band017'][j]+
											   temp_data['cps_band018'][j]+temp_data['cps_band019'][j]+
											   temp_data['cps_band020'][j]+temp_data['cps_band021'][j]+
											   temp_data['cps_band022'][j]+temp_data['cps_band023'][j])
							cps_192_256.append(temp_data['cps_band024'][j]+temp_data['cps_band025'][j]+
											   temp_data['cps_band026'][j]+temp_data['cps_band027'][j]+
											   temp_data['cps_band028'][j]+temp_data['cps_band029'][j]+
											   temp_data['cps_band030'][j]+temp_data['cps_band031'][j])
						else:
							cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j]+
											  temp_data['cps_band2'][j]+temp_data['cps_band3'][j]+
											  temp_data['cps_band4'][j]+temp_data['cps_band5'][j]+
											  temp_data['cps_band5'][j]+temp_data['cps_band6'][j])
							cps_64_128.append(temp_data['cps_band8'][j]+temp_data['cps_band9'][j]+
											  temp_data['cps_band10'][j]+temp_data['cps_band11'][j]+
											  temp_data['cps_band12'][j]+temp_data['cps_band13'][j]+
											  temp_data['cps_band14'][j]+temp_data['cps_band15'][j])
							cps_128_192.append(temp_data['cps_band16'][j]+temp_data['cps_band17'][j]+
											   temp_data['cps_band18'][j]+temp_data['cps_band19'][j]+
											   temp_data['cps_band20'][j]+temp_data['cps_band21'][j]+
											   temp_data['cps_band22'][j]+temp_data['cps_band23'][j])
							cps_192_256.append(temp_data['cps_band24'][j]+temp_data['cps_band25'][j]+
											   temp_data['cps_band26'][j]+temp_data['cps_band27'][j]+
											   temp_data['cps_band28'][j]+temp_data['cps_band29'][j]+
											   temp_data['cps_band30'][j]+temp_data['cps_band31'][j])
						sat.append(path[7:15])
			elif (name == file_name):
				temp_path = new_path + name 
				#print(temp_path)
				temp_data = pd.read_csv(temp_path,skiprows=8,sep='\s+\s+')
				for j in range(len(temp_data)):
					mean_time.append(np.mean(pd.Series((pd.to_datetime(temp_data['exp_start_time'][j]),
														pd.to_datetime(temp_data['exp_end_time'][j])))))
					exposure.append(temp_data['exposure(s)'][j])
					#temp_data['lon_end'][j] = float(temp_data['lon_end'][j])
					#temp_data['lon_start'][j] = float(temp_data['lon_start'][j])
					delta_lat.append(temp_data['lat_end'][j]-temp_data['lat_start'][j])
					# crossing prime meridian
					if abs(temp_data['lon_end'][j] - temp_data['lon_start'][j]) > 100:
						delta_lon = 360-abs(temp_data['lon_end'][j]-temp_data['lon_start'][j])
						if (temp_data['lon_start'][j] < temp_data['lon_end'][j]):
							if (temp_data['lon_start'][j] > 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] - delta_lon/2)
							elif (temp_data['lon_start'][j] < 360 - temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] + delta_lon/2)
						elif (temp_data['lon_start'][j] > temp_data['lon_end'][j]):
							if (360 - temp_data['lon_start'][j] > temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_start'][j] + delta_lon/2)
							elif (360 - temp_data['lon_start'][j] < temp_data['lon_end'][j]):
								lon_mean.append(temp_data['lon_end'][j] - delta_lon/2)
					else:
						lon_mean.append(np.mean((temp_data['lon_start'][j],temp_data['lon_end'][j])))
					lat_mean.append(np.mean((temp_data['lat_start'][j],temp_data['lat_end'][j])))
					alt_mean.append(np.mean((temp_data['alt_start'][j],temp_data['alt_end'][j])))
					if ('Data_firmware_3' in temp_path):
						cps_0_64.append(temp_data['cps_band000'][j]+temp_data['cps_band001'][j]+
											  temp_data['cps_band002'][j]+temp_data['cps_band003'][j]+
											  temp_data['cps_band004'][j]+temp_data['cps_band005'][j]+
											  temp_data['cps_band005'][j]+temp_data['cps_band006'][j])
						cps_64_128.append(temp_data['cps_band008'][j]+temp_data['cps_band009'][j]+
										  temp_data['cps_band010'][j]+temp_data['cps_band011'][j]+
										  temp_data['cps_band012'][j]+temp_data['cps_band013'][j]+
										  temp_data['cps_band014'][j]+temp_data['cps_band015'][j])
						cps_128_192.append(temp_data['cps_band016'][j]+temp_data['cps_band017'][j]+
										   temp_data['cps_band018'][j]+temp_data['cps_band019'][j]+
										   temp_data['cps_band020'][j]+temp_data['cps_band021'][j]+
										   temp_data['cps_band022'][j]+temp_data['cps_band023'][j])
						cps_192_256.append(temp_data['cps_band024'][j]+temp_data['cps_band025'][j]+
										   temp_data['cps_band026'][j]+temp_data['cps_band027'][j]+
										   temp_data['cps_band028'][j]+temp_data['cps_band029'][j]+
										   temp_data['cps_band030'][j]+temp_data['cps_band031'][j])
					else:
						cps_0_64.append(temp_data['cps_band0'][j]+temp_data['cps_band1'][j]+
											  temp_data['cps_band2'][j]+temp_data['cps_band3'][j]+
											  temp_data['cps_band4'][j]+temp_data['cps_band5'][j]+
											  temp_data['cps_band5'][j]+temp_data['cps_band6'][j])
						cps_64_128.append(temp_data['cps_band8'][j]+temp_data['cps_band9'][j]+
										  temp_data['cps_band10'][j]+temp_data['cps_band11'][j]+
										  temp_data['cps_band12'][j]+temp_data['cps_band13'][j]+
										  temp_data['cps_band14'][j]+temp_data['cps_band15'][j])
						cps_128_192.append(temp_data['cps_band16'][j]+temp_data['cps_band17'][j]+
										   temp_data['cps_band18'][j]+temp_data['cps_band19'][j]+
										   temp_data['cps_band20'][j]+temp_data['cps_band21'][j]+
										   temp_data['cps_band22'][j]+temp_data['cps_band23'][j])
						cps_192_256.append(temp_data['cps_band24'][j]+temp_data['cps_band25'][j]+
										   temp_data['cps_band26'][j]+temp_data['cps_band27'][j]+
										   temp_data['cps_band28'][j]+temp_data['cps_band29'][j]+
										   temp_data['cps_band30'][j]+temp_data['cps_band31'][j])
					sat.append(path[7:15])

df = pd.DataFrame(columns=['sat','time','exposure(s)','longitude','latitude','altitude','delta_lat','direction', 'cps_0_64', 'cps_64_128','cps_128_192','cps_192_256'])
df['sat'] = sat
df['time'] = pd.to_datetime(mean_time).round('ms')
df['exposure(s)'] = exposure
df['longitude'] = np.round(np.array(lon_mean),3)
df['latitude'] = np.round(np.array(lat_mean),3)
df['delta_lat'] = delta_lat
df['direction'][df['delta_lat'] > 0] = 'south-to-north'  
df['direction'][df['delta_lat'] < 0] = 'north-to-south'
df['altitude'] = np.round(np.array(alt_mean),3)
df['cps_0_64'] = np.round(np.array(cps_0_64),3) # 0 - 64 ADC
df['cps_64_128'] = np.round(np.array(cps_64_128),3) # 64 - 128 ADC
df['cps_128_192'] = np.round(np.array(cps_128_192),3) # 128 - 192 ADC
df['cps_192_256'] = np.round(np.array(cps_192_256),3) # 192 - 256 ADC

df = df.drop(['delta_lat'], axis=1)

# # data with cps = 0.0
#cond = df['cps_64_128'] != 0.0
#df = df[cond]

## sort by time
df = df.sort_values(by='time')

df.to_csv('all_cubesat_data.csv',index=False)
