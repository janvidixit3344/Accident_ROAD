from flask import Flask, render_template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

def load_data():
    df = pd.read_csv('Dataset/acc_mode.csv')
    return df

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph/1')
def graph_1():
    acc_mode = load_data()
    year = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
    fig1 = px.area(acc_mode, x=acc_mode.index, y='Total', title='Accident year-wise')
    fig2 = px.bar(acc_mode, x=acc_mode.index, y='Total', title='Accident year-wise')
    fig3 = px.bar(acc_mode, x=acc_mode.index, y='Total', title='Accident year-wise')
    return render_template('graph1.html', fig1=fig1.to_html(),fig2=fig2.to_html(), fig3=fig3.to_html())

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8080, debug=True)