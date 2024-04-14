import matplotlib
import matplotlib.pyplot as plt
from matplotlib import rc, cm
import cartopy
import cartopy.io.shapereader as shpreader
import cartopy.crs as ccrs
import numpy as np
import pandas as pd
from matplotlib.colors import ListedColormap, LinearSegmentedColormap
import maxminddb

file = open('targets.txt', 'r')
geolite_filepath = 'GeoLite2-City.mmdb'
ping_targets_geoinfo = {}
with maxminddb.open_database(geolite_filepath) as reader:
    for line in file:
        line = line.strip()
        response = reader.get(line)
        ping_targets_geoinfo[line] = response


def formatSize(width=16, height=4.94, legendFontsize='20'):
    params = {'legend.fontsize': legendFontsize,
              'figure.figsize': (width, height),
              'axes.labelsize': 30,
              'axes.titlesize':30,
              'xtick.labelsize': 22,
              'ytick.labelsize': 22,
              'font.weight': 'normal'}  
    matplotlib.rcParams.update(params)

    
#Set up the color map
# The scale of the colorbar.  We go from -40 -- 40, so N=80 worked
# best.  N is also needed later to determine the color.
N = 80

RdGyGn = LinearSegmentedColormap.from_list(
    name='RdGyGn',
    colors = [
              (1, 0, 0), #red
              (1, 153/255, 51/255), #orange
              (1, 1, 51/255), #yellow
              (51/255, 204/255, 153/255), # blue green
              #(0, 130/255, 130/255), # teal
              #    (0, 1, 0), # green
              #(0, 0, 1), # blue
              (0, 33/255, 203/255), #indigo
    ],
    N=N)

cm.register_cmap(name='RdGyGn', cmap=RdGyGn)
colorbarMappable = cm.ScalarMappable(cmap=RdGyGn)
colorbarMappable.set_array([-1 * (N/2), (N/2)])



##########
#
# This section sets up the figure, loops through the countries, and
# sets the colors according the the above colormap
#
#########

formatSize(height=4.94, legendFontsize=12)
ax = plt.axes(projection=ccrs.PlateCarree())
ax.add_feature(cartopy.feature.LAND, color='lightgrey')
ax.add_feature(cartopy.feature.OCEAN, color='white')
# ax.add_feature(cartopy.feature.BORDERS, linestyle='-', alpha=.2)
ax.set_extent([-130, 180, -50, 75], crs=ccrs.PlateCarree())

# Pull in country info, including full name and two letter
# abbreviation.
shpfilename = shpreader.natural_earth(resolution='110m',
                                      category='cultural',
                                      name='admin_0_countries')
reader = shpreader.Reader(shpfilename)
countries = reader.records()

# Add the datacenter location to the map
pop2lat_lon = {
    'tokyo': (35.7845551716681, 139.79904704417174),
    "frankfurt": (50.141205008354625, 8.664006892540352),
    "newyork": (40.78780881756055, -74.18404489341317),
    'chicago': (41.94618613674771, -87.49145561978457),
    'seattle': (47.71363771777337, -122.31625978108252),
    'mumbai': (19.256414933028722, 72.85908810657308),
    'london': (51.56067889556891, -0.21129100742921114),
    'amsterdam': (52.40988015227054, 4.964688906371022),
    'atlanta': (33.75233505143144, -84.38406143342769),
    'losangeles': (34.05556087637232, -118.29937358131049),
    'dallas': (32.86354031221057, -96.81842699534002),
    'singapore': (1.358144723499965, 103.87066124353105),
    'seoul': (37.608736860935025, 126.82547985938471),
    'paris': (48.85908151621847, 2.3516222127201387),
    'stockholm': (59.33458272396572, 18.070591836721842),
    'silicon': (37.397266121710715, -122.05277838325178),
    'madrid': (40.42532590166732, -3.700829745538672),
    'toronto': (43.6704208941205, -79.37614803483865),
    'sydney': (-33.84406911202259, 151.20958386664287),
    'johannesburg': (-26.167181761557384, 28.146802918352527),
    'saopaulo': (-23.501346850507527, -46.53772609752225),
    'warsaw': (52.424474284700636, 20.953900522190814),
    'delhi': (28.87127484875151, 76.80706611492809),
    'melbourne': (-37.36180956999166, 144.93928749193603),
    'bangalore': (13.18196485524777, 77.67543068686498),
    'mexico': (19.48016287132275, -99.06009192296797),
    'miami': (25.763222066551855, -80.19444179522998),
}
xs, ys = [], []
for city in pop2lat_lon:
    x, y = pop2lat_lon[city]
    xs.append(x)
    ys.append(y)
ax.scatter(ys, xs,
   color="b", s=40, alpha = 1, transform=ccrs.Geodetic(), zorder=150)

ipsnotfound = []
xs, ys = [], []
for ip in ping_targets_geoinfo:
    try:
        x, y = ping_targets_geoinfo[ip]['location']['latitude'], ping_targets_geoinfo[ip]['location']['longitude']
        xs.append(x)
        ys.append(y)
    except:
        ipsnotfound.append(ip)
ax.scatter(ys, xs, color='g', s=5, marker='*', alpha = 1, transform=ccrs.Geodetic(), zorder=100)


# Manually set the colorbar ticks, otherwise the auto detect/populate
# messes things up
# plt.colorbar(colorbarMappable, pad=.01, ticks=[-40, -30, -20, -10, 0, 10, 20, 30, 40])
lgnd = plt.legend(['Vultr PoPs', 'Ping Targets'], fontsize=15, loc='upper right', fancybox=True, framealpha=0.8)
lgnd.set_zorder(200)
lgnd.legendHandles[0]._sizes = [30]
lgnd.legendHandles[1]._sizes = [30]
plt.plot()

# I saved to pdf so it renders better
plt.savefig('Vultr-Map.pdf', bbox_inches='tight')

