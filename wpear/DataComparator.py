import pygrib
import numpy

def DataComparator(forecast_file, observed_file): 
	#Potentially add column name too once we have more than one column in the cleaned file
	#Comment out file opens if the file is sent
	grbs_f = pygrib.open(forecast_file)
	grbs_o = pygrib.open(observed_file)
	
	temp15_arr_f = grbs_f.select(name='2 metre temperature')[0]
	temp15_arr_o = grbs_o.select(name='2 metre temperature')[0]
	
	#grb = grbs_f.message(12)
	#lats,lons = grb.latlons()
	#print lats.min(), lats.max()
	#print lons.min(), lons.max()
	#Only doing difference for now
	arr = temp15_arr_f.values - temp15_arr_o.values
	#print arr
	ret_file = pygrib.open(forecast_file)
	gobj = ret_file.select(name='2 metre temperature')[0]
	gobj.values=numpy.array(arr)
	
	print gobj.values

	# return grib message
	return gobj

DataComparator('hrrr.t15z.wrfsubhf01.grib2', 'hrrr.t15z.wrfsubhf01.grib2')
