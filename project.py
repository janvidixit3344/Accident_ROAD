from flask import Flask, render_template
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

app = Flask(__name__)

def load_acc_data():
    acc_mode = pd.read_csv('Dataset/acc_mode.csv')
    acc_mode.rename(columns={
    'State/UT':'STATE/UT',
    'Year':'YEAR',
    'Mode':'VEHICLE USED'}, inplace=True)
    return acc_mode

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/graph/1')
def graph_1():
    acc_mode = load_acc_data()
    grouped_obj = acc_mode.groupby(["YEAR"]).sum()
    year = [2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013, 2014]
    fig1 = px.area(grouped_obj, x=grouped_obj.index, y='Total', title='Accident year-wise')
    conclusion = 'The graph shows the accidents yearly.'
    fig1.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    # STATE-WISE DATA 
    grouped_obj = acc_mode.groupby(["STATE/UT"]).sum()
    grouped_obj.drop(['YEAR'], axis=1, inplace=True)
    grouped_obj
    # accidents state-wise
    fig2 = px.area(grouped_obj, x=grouped_obj.index, y='Total', title='Accident year-wise')
    conclusion = 'The graph shows accidents from every State and UT.'
    fig2.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))
    
    # VEHCILE INVOLVEMENT DATA 
    grouped_obj = acc_mode.groupby(["VEHICLE USED"]).sum()
    grouped_obj.drop(['YEAR'], axis=1, inplace=True)
    grouped_obj
    # vehicles involved
    Total = ['Bicycle', 'Bus','Car','Jeep','Other Motor Vehicles','Others','Pedestrian','Three Wheeler','Truck/Lorry','Two Wheeler']
    fig3 = px.bar(grouped_obj, x=grouped_obj.index, y='Total', title='Accident year-wise')
    conclusion = 'The graph shows that accidents due to vehicles involved.'
    fig3.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    return render_template('graph1.html', fig1=fig1.to_html(),fig2=fig2.to_html(), fig3=fig3.to_html())

@app.route('/graph/2')
def graph_2():
    acc_mode = load_acc_data()
    fig4 = px.area(acc_mode, x='VEHICLE USED', y=['Total'], title='Average accident state-wise')
    mean_accidents = acc_mode['Total'].mean()
    fig4.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average accidents state-wise = {mean_accidents:.0f}",showarrow=False)

    fig5 = px.area(acc_mode, x='STATE/UT', y=['Total'], title='Average accident state-wise')
    mean_accidents = acc_mode['Total'].mean()
    fig5.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average accidents state-wise = {mean_accidents:.0f}",showarrow=False)

    fig6 = px.area(acc_mode, x='YEAR', y=['Total'], title='Average accident yearly')
    mean_accidents = acc_mode['Total'].mean()
    fig6.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average accidents year-wise = {mean_accidents:.0f}",showarrow=False)
    return render_template('graph2.html', fig4=fig4.to_html(), fig5=fig5.to_html(), fig6=fig6.to_html())

def load_accident_data():
    accident_data = pd.read_csv('Dataset/accidient_data_of_india.csv')
    accident_data.rename(columns={
    'Years':'Year',
    'Total Number of Road Accidents (in numbers)':'Total accidents',
    'Total Number of Persons Killed (in numbers)':'Total Killed',
    'Total Number of Persons Injured (in numbers)':'Total Injured',
    'Population of India (in thousands)':'Total Population',
    'Total Number of Registered Motor Vehicles (in thousands)':'Total Registered Vehicle',
    'Road Length (in kms)':'Road Length',
    'Number of Accidents per Lakh Population':'Accidents Per Lakh',
    'Number of Accidents per Ten Thousand Vehicles':'Accidents Per 10K Vehicles',
    'Number of Accidents per Ten Thousand Kms of Roads':'Accidents Per 10K KM Road',
    'Number of Persons Killed Per Lakh Population':'Killed Per Lakh',
    'Number of Persons Killed Per Ten Thousand Vehicles':'Killed Per 10K Vehicles',
    'Number of Persons Killed per Ten Thousand Kms of Roads':'Killed Per 10K KM Road',
    'Number of Persons Injured per Lakh Population':'Injured Per Lakh',
    'Number of Persons Injured Per Ten Thousand Vehicles':'Injured Per 10K Vehicles',
    'Number of Persons Injured Per Ten Thousand Kms of Roads':'Injured Per 10K KM Road'}, inplace=True)
    return accident_data


#load_accident_data.drop(columns=['Unnamed: 0'], inplace=True)

import re
def clean_numerical_columns(value):
    if isinstance(value, str):
        if value.count('.') == 0:
            value = re.sub(r'[^0-9]+', '', value)
            value = int(value) if value else np.nan
        else:
            value = re.sub(r'[^0-9.]+', '', value)
            value = float(value) if value else np.nan
        return value
    print(value)
    return np.nan

for col in load_accident_data.select_dtypes(include=['object']).columns:
    load_accident_data[col] = load_accident_data[col].apply(clean_numerical_columns)

#load_accident_data.drop(index = load_accident_data[load_accident_data['Year'] == 1].index, inplace=True)

@app.route('/graph/3')
def graph_3():
    accident_data = load_accident_data()
    
    # total accidents per year
    fig7 = px.area(accident_data, x='Year', y='Total accidents', title='Total accidents per year')
    fig7.add_scatter(x=accident_data['Year'], y=accident_data['Total accidents'], mode='markers', name='Accidents', marker=dict(color='blue', size=10))
    mean_accidents = accident_data['Total accidents'].mean()
    fig7.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average accidents per year = {mean_accidents:.0f}",showarrow=False)

    # killed per year
    fig8 = px.area(accident_data, x='Year', y='Total Killed', title='Total Killed per year')
    fig8.add_scatter(x=accident_data['Year'], y=accident_data['Total Killed'], mode='markers', name='Killed', marker=dict(color='green', size=10))
    mean_accidents = accident_data['Total Killed'].mean()
    fig8.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average Killed per year = {mean_accidents:.0f}",showarrow=False)

    # injuries per year
    fig9 = px.area(accident_data, x='Year', y='Total Injured', title='Total Injured per year')
    fig9.add_scatter(x=accident_data['Year'], y=accident_data['Total Injured'], mode='markers', name='Injured', marker=dict(color='red', size=10))
    mean_accidents = accident_data['Total Injured'].mean()
    fig9.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average Injuries per year = {mean_accidents:.0f}",showarrow=False)
    render_template('graph3.html', fig7=fig7.to_html(), fig8=fig8.to_html(), fig9=fig9.to_html())

@app.route('/graph/4')
def graph_4():
    def load_accident_data():
        accident_data = pd.read_csv('Dataset/accidient_data_of_india.csv')
        accident_data.rename(columns={
        'Years':'Year',
        'Total Number of Road Accidents (in numbers)':'Total accidents',
        'Total Number of Persons Killed (in numbers)':'Total Killed',
        'Total Number of Persons Injured (in numbers)':'Total Injured',
        'Population of India (in thousands)':'Total Population',
        'Total Number of Registered Motor Vehicles (in thousands)':'Total Registered Vehicle',
        'Road Length (in kms)':'Road Length',
        'Number of Accidents per Lakh Population':'Accidents Per Lakh',
        'Number of Accidents per Ten Thousand Vehicles':'Accidents Per 10K Vehicles',
        'Number of Accidents per Ten Thousand Kms of Roads':'Accidents Per 10K KM Road',
        'Number of Persons Killed Per Lakh Population':'Killed Per Lakh',
        'Number of Persons Killed Per Ten Thousand Vehicles':'Killed Per 10K Vehicles',
        'Number of Persons Killed per Ten Thousand Kms of Roads':'Killed Per 10K KM Road',
        'Number of Persons Injured per Lakh Population':'Injured Per Lakh',
        'Number of Persons Injured Per Ten Thousand Vehicles':'Injured Per 10K Vehicles',
        'Number of Persons Injured Per Ten Thousand Kms of Roads':'Injured Per 10K KM Road'}, inplace=True)
    accident_data = load_accident_data()

    grouped_obj = load_accident_data.groupby(['Year']).sum()
    # injuries due to accidents
    fig10 = px.area(load_accident_data, x='Year', y=['Total Injured','Total accidents'], title='Total injuries due to accidents per year')
    fig10.add_scatter(x=load_accident_data['Year'], y=load_accident_data['Total Injured'], mode='markers', name='Injured', marker=dict(color='indigo', size=10))
    mean_accidents = load_accident_data['Total Injured'].mean()
    fig10.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average Injuries per year = {mean_accidents:.0f}",showarrow=False)
    render_template('graph4.html', fig10=fig10.to_html())

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8080, debug=True)