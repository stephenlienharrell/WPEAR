import pygrib

#def start():
grbs = pygrib.open('GreatLakes.wind.7days.grb')
#print grbs

grbs.seek(0)

for grb in grbs:
	print grb

#grb2 = grbs.select(name='Maximum temperature')[0]
#print '\n'


