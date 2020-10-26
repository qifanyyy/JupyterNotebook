#!/usr/bin/env python3

import plotly.offline as py
from plotly.offline import download_plotlyjs, init_notebook_mode, plot, iplot
import plotly.graph_objs as go
import CsvDataWriter
import pprint
import csv
import glob
import os

pp = pprint.PrettyPrinter(indent=4)

def get_most_recent_data_file():
    list_of_files = glob.glob('./benchmark_data/*') # * means all if need specific format then *.csv
    return max(list_of_files, key=os.path.getctime)

def _plot(data):
    """Takes a dict in the form {"x": [x axis data], "y": [y axis data]} and generates a plot."""
    trace = go.Scatter(
        x=data["x"], 
        y=data["y"], 
        mode='lines+markers', 
        name='lines+markers'
    )
    plotData = [trace]
    layout = go.Layout(
        title="Runtime of Shor's Algorithm", 
        width=800, 
        height=600,
        xaxis=dict(
            title='Average Time to Factorize (10 trials)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        ),
        yaxis=dict(
            title='Input Length (Digits)',
            titlefont=dict(
                family='Courier New, monospace',
                size=18,
                color='#7f7f7f'
            )
        )
    )
    figure = go.Figure(data=plotData, layout=layout)
    # py.image.save_as(figure, filename="test-plot.png")
    return figure

def make_plot(filename):
    return _plot(parse_data(filename))

def transform_data(data):
    x_axis = []
    y_axis = []
    for i in data:
        x_axis.append(i[0])
        y_axis.append(i[len(i) - 1])
    
    plotData = {"x": x_axis, "y": y_axis}
    # print(plotData)
    return plotData

def parse_data(filename):
    x_axis = []
    y_axis = []
    with open(filename) as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            x_axis.append(row["input_len"])
            y_axis.append(row["average"])
    data = {"x": x_axis, "y": y_axis}
    return data
            

if __name__ == "__main__":
    init_notebook_mode(connected=True)
    iplot(make_plot(get_most_recent_data_file()), image_width=800, image_height=600, filename="shors/plot")