import pygrib
import numpy

def DataComparator(f_obj, o_obj): 
	#Potentially add column name too once we have more than one column in the cleaned file
	#Comment out file opens if the file is sent
	#grbs_f = pygrib.open(forecast_file)
	#grbs_o = pygrib.open(observed_file)
	
	temp15_arr_f = f_obj.select(name='2 metre temperature')[0]
	temp15_arr_o = o_obj.select(name='2 metre temperature')[0]
	
	#grb = grbs_f.message(12)
	#lats,lons = grb.latlons()
	#print lats.min(), lats.max()
	#print lons.min(), lons.max()
	#Only doing difference for now
	arr = temp15_arr_f.values - temp15_arr_o.values
	#print arr
	ret_file = f_obj
	gobj = ret_file.select(name='2 metre temperature')[0]
	gobj.values=numpy.array(arr)
	
	print gobj.values

	# return grib message
	return gobj

def MultiSetAverage(grb_list, var):	# To change to index referencing: MultiSetAverage(grb_list, index)
	size = len(grb_list)

	if size <= 0:
		return null
	else:		
		#print grb_list[0].select(name=var)[0].values

		arr = grb_list[0].select(name=var)[0].values	# Index referencing: arr = grb_list[0].message(index).values
		del grb_list[0]
		
		for grb_obj in grb_list:
			arr = arr + grb_obj.select(name=var)[0].values		# Index referencing: arr = arr + grb_obj.message(index).values
		
		arr = arr/size
		#print arr
		
		return arr
#MultiSetAverage([pygrib.open('hrrr.t15z.wrfsubhf01.grib2'), pygrib.open('hrrr.t15z.wrfsubhf01.grib2')], '2 metre temperature')
#DataComparator(pygrib.open('hrrr.t15z.wrfsubhf01.grib2'), pygrib.open('hrrr.t15z.wrfsubhf01.grib2'))
