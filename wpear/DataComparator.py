import pygrib
import numpy

def DataComparator(f_msg, o_msg):
	#Potentially add column name too once we have more than one column in the cleaned file
	#Comment out file opens if the file is sent
	#grbs_f = pygrib.open(f_msg)
	#grbs_o = pygrib.open(observed_file)
	#for grb in f_msg:
	#	print grb
	#lats,lons = grb.latlons()
	#print lons.min(), lons.max()
	#Only doing difference for now
	#print f_msg.values
	arr = f_msg.values - o_msg.values
	#print arr
	gobj = f_msg
	#gobj.values=arr#numpy.array(arr)
	
	#print gobj.values

	# return grib message
	return gobj

def MultiSetAverage(grb_list):	# To change to index referencing: MultiSetAverage(grb_list, index)
	size = len(grb_list)
	print grb_list[0].values
	if size <= 0:
		return None
	else:		
		#print grb_list[0].select(name=var)[0].values

		arr = grb_list[0].values	# Index referencing: arr = grb_list[0].message(index).values
		del grb_list[0]
		
		for grb_obj in grb_list:
			arr = arr + grb_obj.values		# Index referencing: arr = arr + grb_obj.message(index).values
		
		arr = arr/size
		print arr
		
		return arr
#MultiSetAverage([pygrib.open('hrrr.t15z.wrfsubhf01.grib2').select(name='2 metre temperature')[0], pygrib.open('hrrr.t15z.wrfsubhf01.grib2').select(name='2 metre temperature')[0]])
#DataComparator(pygrib.open('in_hrrr.t00z.wrfsfcf00.grib2').select(name='Temperature')[0], pygrib.open('in_hrrr.t00z.wrfsfcf10.grib2').message(1))
