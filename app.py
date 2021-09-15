from flask import Flask, render_template, request
import pandas as pd
import csv
import os
import matplotlib.pyplot as plt
import seaborn as  sns 
import folium
from crime import plot_of_crime
import pandas as pd
import json
from folium import plugins

app = Flask(__name__)

@app.route('/analyse',methods=['GET'])
def analyse():

	var = request.json
	plot_of_crime(var['filePath'],var['outputFolder'])
	return json.dumps({'success':True})
		

if __name__ == '__main__':
	app.run(debug=True)
