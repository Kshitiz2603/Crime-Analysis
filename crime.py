import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import sklearn
import folium
import pandas as pd
import json
from folium import plugins
import time
import os

def plot_of_crime(filepath,outputfolder):
	if not os.path.exists(outputfolder):
		os.mkdir(outputfolder)
	t1 = time.time()
	data1 = pd.read_csv(filepath)
	data = data1.dropna()
	fig, ax = plt.subplots()
	fig.set_size_inches(20, 8)
	sns_plot = sns.countplot(x = 'District', data = data)
	ax.set_xlabel('District', fontsize=15)
	ax.set_ylabel('Count', fontsize=15)
	ax.set_title('District Distribution', fontsize=15)
	fig = sns_plot.get_figure()
	#save file
	fig.savefig(os.path.join(outputfolder,'district.png'))

	fig, ax = plt.subplots()
	fig.set_size_inches(20, 8)
	sns_plot1 = sns.countplot(x = 'offenseLevel', data = data)
	ax.set_xlabel('Offense', fontsize=15)
	ax.set_ylabel('Count', fontsize=15)
	ax.set_title('Offense Level Distribution', fontsize=15)
	fig = sns_plot1.get_figure()
	#save file
	fig.savefig(os.path.join(outputfolder,'offense_level.png'))

	df = pd.DataFrame(data, columns=['District','offenseLevel','time'])
	from sklearn.preprocessing import LabelEncoder
	labelencoder_X = LabelEncoder()
	df['District'] = labelencoder_X.fit_transform(df['District'])
	df['offenseLevel'] = labelencoder_X.fit_transform(df['offenseLevel'])
	plot2 = df.plot.hexbin(x='offenseLevel',y='time',gridsize=35)
	#save file
	plot2.plot()
	plt.savefig(os.path.join(outputfolder,'heatmap.png'))

	fig, ax = plt.subplots()
	fig.set_size_inches(20, 8)
	sns_plot2 = sns.countplot(x = 'occurenceLocation', data = data)
	ax.set_xlabel('Occurence', fontsize=15)
	ax.set_ylabel('Count', fontsize=15)
	ax.set_title('Occurence Level Distribution', fontsize=15)
	fig = sns_plot2.get_figure()
	#save file
	fig.savefig(os.path.join(outputfolder,'occurense.png'))

	plt.figure(figsize=(20,8), dpi= 200)
	sns.distplot(data.loc[data['offenseLevel'] == 'FELONY', "time"], color="dodgerblue", label="FELONY", hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
	sns.distplot(data.loc[data['offenseLevel'] == 'MISDEMEANOR', "time"], color="yellow", label="MISDEMEANOR", hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
	sns.distplot(data.loc[data['offenseLevel'] == 'VIOLATION', "time"], color="g", label="VIOLATION", hist_kws={'alpha':.7}, kde_kws={'linewidth':3})
	plt.ylim(0, 0.35)
	plt.title('Density Plot of offense type vs time', fontsize=22)
	plt.legend()
	plt.savefig(os.path.join(outputfolder,'density_plot.png'))

	data_2015 = data[(data['year']>= 2015) & (data['month']>=10) & (data['District']=="PERAMBALUR") & (data['offenseDescription']=="ROBBERY")]

	with open('map1.geojson') as f:
	    laArea = json.load(f)

	laMap = folium.Map(location=[12.00000,79.00000], tiles='cartodbpositron', zoom_start=9)

	folium.GeoJson(laArea).add_to(laMap)

	for i,row in data_2015.iterrows():
	    folium.CircleMarker((row.Latitude,row.Longitude), radius=0.5, weight=2, color='red', fill_color='red', fill_opacity=.5).add_to(laMap)

	#save the map as an html    
	laMap.save(os.path.join(outputfolder,'Robberies_in_perambalur_in_year_2015_2.html'))


	for i,row in data_2015.iterrows():
	    folium.CircleMarker((row.Latitude,row.Longitude), radius=1, weight=2, color='red', fill_color='red', fill_opacity=.5).add_to(laMap)


	laMap.add_children(plugins.HeatMap(data=data_2015[['Latitude', 'Longitude']].values, radius=25, blur=10))

	laMap.save(os.path.join(outputfolder,'Robberies_in_perambalur_in_year_2015_heatmap.html'))


	map1 = folium.Map(
	    location=[12.00000,79.00000],
	    tiles='cartodbpositron',
	    zoom_start=12,
	)
	data_2015.apply(lambda row:folium.CircleMarker(location=[row["Latitude"], row["Longitude"]]).add_to(map1), axis=1)

	map1.save(os.path.join(outputfolder,'Robberies_in_perambalur_in_year_2015.html'))

	#Murders in Salem district in the period 2014 and 2015
	data_2014 = data[(data['year']>= 2014) & (data['District']=="SALEM") & (data['offenseDescription']=="MURDER_AND_NON_NEGL_MANSLAUGHTER")]
	for i,row in data_2014.iterrows():
	    folium.CircleMarker((row.Latitude,row.Longitude)).add_to(laMap)

	laMap.save(os.path.join(outputfolder,'MURDER_AND_NON_NEGL_MANSLAUGHTER_in_Salem_from_2014_to_2015.html'))

	print("Time taken: ",time.time()-t1)

if __name__ == '__main__':
	plot_of_crime('/home/kshitiz/Desktop/crime/CrimeData.csv','/home/kshitiz/Desktop/crime/images')