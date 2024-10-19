import pandas as pd
from sklearn.linear_model import LinearRegression
import os
import scipy.constants as const

#  constant
# radius of earth (meters) from https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html using Equatorial radius
radius_of_earth_m=6378137
# mass of earth (kg) from https://nssdc.gsfc.nasa.gov/planetary/factsheet/earthfact.html
earth_mass = 5972200000000000000000000

# import original csv file
pd.options.display.max_rows = 999
idf = pd.read_csv('/Users/michael/Desktop/20241020.Phys.2.Kepler Law Investigation/USC.csv', encoding='cp1252')
df = idf[["Current Official Name of Satellite","Perigee (km)", "Apogee (km)","Period (minutes)"]]

#  selecting name, perigee, apogee, and period
df = df.rename(axis=1,mapper={"Current Official Name of Satellite":"name", "Perigee (km)":"Perigee_km", "Apogee (km)":"Apogee_km","Period (minutes)":"Period_m"})

# start cleaning up:
# convert string to numers
df.Apogee_km = df.Apogee_km.str.replace(',', '')
df.Perigee_km = df.Perigee_km.str.replace(',', '')
df.Period_m = df.Period_m.str.replace(',', '')
df.Apogee_km = pd.to_numeric(df.Apogee_km, downcast='signed')
df.Perigee_km = pd.to_numeric(df.Perigee_km, downcast='signed')
df.Period_m = pd.to_numeric(df.Period_m, downcast='signed')
# drop NaN
df.dropna()
# drop orbits that are too elliptic here defined as apogee being more than two times of perigee
df = df[(abs(df.Apogee_km-df.Perigee_km)<(df.Perigee_km))]
# tried to dropped NaN again
df=df.dropna()

# calculating orbit radius:

# "the squares of the orbital periods of the planets are directly proportional to the cubes of the semi-major axes of their orbits"
# from https://science.nasa.gov/resource/orbits-and-keplers-laws/

# semi-major radius = half of the sum of the perihelion (which is Apogee) and the aphelion (which is Perigee)
# from https://pressbooks.online.ucf.edu/osuniversityphysics/chapter/13-5-keplers-laws-of-planetary-motion/
# also backed up by this: https://study.com/academy/lesson/semi-major-axis-of-an-ellipse.html#:~:text=The%20semi%2Dmajor%20axis%20is%20half%20of%20the%20major%20axis,the%20foci%20of%20the%20ellipse.
fdf = pd.DataFrame(data={"r":(df.Apogee_km+df.Perigee_km)/2*1000+radius_of_earth_m, "t":df.Period_m*60})
fdf = pd.DataFrame(data={"r":fdf.r*fdf.r*fdf.r, "t":fdf.t*fdf.t})

# finding min and max for r3 and t2 for exel horizontal axis
rmin = fdf.r.min()
rmax = fdf.r.max()
tmin = fdf.t.min()
tmax = fdf.t.max()
print(rmin)
print(rmax)
print(tmin)
print(tmax)

# export cleared data to csv to exel for graph
# fdf.to_csv('20241020.Phys.2.Keplers Law Investigation.data.cleaned up.csv', index=False)

# linear regression
x=fdf[["t"]]
y=fdf["r"]
model = LinearRegression()
model.fit(x,y)

# calculating mass
calculated_mass=model.coef_*4*const.pi*const.pi/const.G
print(calculated_mass)

# percent error (in decimals)
percent_error = abs(earth_mass-calculated_mass)/earth_mass
print(percent_error)
