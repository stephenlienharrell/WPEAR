import pygrib

def DataComparator(forecast_file, observed_file): 
	#Potentially add column name too once we have more than one column in the cleaned file
	#Comment out file opens if the file is sent
	grbs_f = pygrib.open(forecast_file)
	grbs_o = pygrib.open(observed_file)
	
	temp15_arr_f = grbs_f.select(name='2 metre temperature')[0]
	temp15_arr_o = grbs_o.select(name='2 metre temperature')[0]
	
	#grb = grbs_f.message(12)
	#print grb
	#Only doing difference for now
	arr = temp15_arr_f.values - temp15_arr_o.values
	#print arr
	msg = arr.tostring()
	print msg

	# return grib message
	return msg

DataComparator('hrrr.t15z.wrfsubhf01.grib2', 'hrrr.t15z.wrfsubhf01.grib2')
