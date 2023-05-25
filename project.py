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
    
    return render_template('graph1.html', fig1=fig1.to_html(), f2=fig2.to_html(), fig3=fig3.to_html(), fig4=fig4.to_html(), fig5=fig5.to_html(), fig6=fig6.to_html())

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
    for col in accident_data.select_dtypes(include=['object']).columns:
        accident_data[col] = accident_data[col].apply(clean_numerical_columns)
    accident_data.drop(index = accident_data[accident_data['Year'] == 1].index, inplace=True)   
    return accident_data

@app.route('/graph/2')
def graph_2():
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
    
    grouped_obj = accident_data.groupby(['Year']).sum()
    grouped_obj

    fig10 = px.area(accident_data, x='Year', y=['Total Injured','Total accidents'], title='Total injuries due to accidents per year')
    fig10.add_scatter(x=accident_data['Year'], y=accident_data['Total Injured'], mode='markers', name='Injured', marker=dict(color='indigo', size=10))
    mean_accidents = accident_data['Total Injured'].mean()
    fig10.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average Injuries per year = {mean_accidents:.0f}",showarrow=False)

    fig11 = px.area(accident_data, x='Year', y=['Total Killed','Total accidents'], title='Total Killed per year')
    fig11.add_scatter(x=accident_data['Year'], y=accident_data['Total Killed'], mode='markers', name='Killed', marker=dict(color='blue', size=10))
    mean_accidents = accident_data['Total Killed'].mean()
    fig11.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Average Killed per year = {mean_accidents:.0f}",showarrow=False)

    fig12 = px.area(accident_data, x='Year', y=['Total accidents','Total Population'], title='Accidents out of total population per year')
    fig12.add_scatter(x=accident_data['Year'], y=accident_data['Total accidents'], mode='markers', name='Accidents', marker=dict(color='grey', size=10))
    mean_accidents = accident_data['Total accidents'].mean()
    fig12.add_annotation(xref='paper', yref='paper', x=0.1, y=1, text=f"Accidents out of total population = {mean_accidents:.0f}",showarrow=False)
    
    fig13 = px.sunburst(accident_data, path=['Year', 'Total accidents'], values='Total accidents', title='Total accidents per year')

    fig14 = px.sunburst(accident_data, path=['Year', 'Total Killed'], values='Total Killed', title='Total Killed per year')

    fig15 = px.sunburst(accident_data, path=['Year', 'Total Injured'], values='Total Injured', title='Total Injured per year')

    fig16 = px.sunburst(accident_data, path=['Year', 'Total Registered Vehicle'], values='Total Registered Vehicle', title='Total Registered Vehicle per year')

    fig17 = px.pie(accident_data, values='Total Injured', names='Year', title='Total accidents per year')

    fig18 = px.pie(accident_data, values='Total Killed', names='Year', title='Total Killed per year')

    fig19 = px.pie(accident_data, values='Total Injured', names='Year', title='Total Injured per year')

    fig20 = px.treemap(accident_data, path=['Year', 'Total accidents'], values='Total accidents', title='Total accidents per year')

    return render_template('graph2.html', fig7=fig7.to_html(), fig8=fig8.to_html(), fig9=fig9.to_html(),
                fig10=fig10.to_html(), fig11=fig11.to_html(), fig12=fig12.to_html(), fig13=fig13.to_html(),
                fig14=fig14.to_html(), fig15=fig15.to_html(), fig16=fig16.to_html(), fig17=fig17.to_html(),
                fig18=fig18.to_html(), fig19=fig19.to_html(), fig20=fig20.to_html())


def load_driverresponse():
    driver_response = pd.read_csv('Dataset/driverresponse.csv')
    driver_response.rename(columns={
    'stateut':'State/UT',
    'region':'GEO_Region',
    'regionid':'R_ID',
    'alcintake2014':'AIntake_14',
    'overspeed2014':'Speeding_14',
    'overtaking2014':'Overtake_14',
    'lanejumping2014':'LaneJump_14',
    'wrongside2014':'WrongSide_14',
    'signalavoid2014':'SignalAvoid_14',
    'asleep2014':'Sleep_14',
    'othercause2014':'Others_14',
    'alcintake2016':'AIntake_16',
    'overspeed2016':'Sppeding_16',
    'signalavoid2016':'SignalAvoid_16',
    'wrongside2016':'WrongSide_16',
    'lanejumping2016':'LaneJump_16',
    'overtaking2016':'Overtake_16',
    'asleep2016':'Sleeping_16',
    'othercause2016':'Others_16'}, inplace=True)

    driver_response['Overtake'] = driver_response['Overtake_14'] + driver_response['Overtake_16']
    driver_response.drop(columns=['Overtake_16','Overtake_14'], inplace=True)
    driver_response['AiIntake'] = driver_response['AIntake_16'] + driver_response['AIntake_14'] 
    driver_response.drop(columns=['AIntake_16','AIntake_14'], inplace=True)
    driver_response['LaneJump'] = driver_response['LaneJump_16'] + driver_response['LaneJump_14']
    driver_response.drop(columns=['LaneJump_16','LaneJump_14'], inplace=True)
    driver_response['Sleeping'] = driver_response['Sleeping_16'] + driver_response['Sleep_14']
    driver_response.drop(columns=['Sleeping_16','Sleep_14'], inplace=True)
    driver_response['Speeding'] = driver_response['Sppeding_16'] + driver_response['Speeding_14']
    driver_response.drop(columns=['Sppeding_16','Speeding_14'], inplace=True)
    driver_response['WrongSide'] = driver_response['WrongSide_16'] + driver_response['WrongSide_14']
    driver_response.drop(columns=['WrongSide_16','WrongSide_14'], inplace=True)
    driver_response['SignalAvoid'] = driver_response['SignalAvoid_16'] + driver_response['SignalAvoid_14']
    driver_response.drop(columns=['SignalAvoid_16','SignalAvoid_14'], inplace=True)
    driver_response['Others'] = driver_response['Others_16'] + driver_response['Others_14']
    driver_response.drop(columns=['Others_16','Others_14'], inplace=True)
    return driver_response

@app.route('/graph/3')
def graph_3():
    driver_response = load_driverresponse()

    # state wise lane jumper in violin plot
    fig21 = px.bar(driver_response, y="LaneJump", x="State/UT", color="State/UT",hover_data=driver_response.columns)
    conclusion = 'The graph shows that Tamil Nadu has the highest LaneJumpers.'
    fig21.add_annotation(text=conclusion, xref='paper', yref='paper', x=0, y=1, showarrow=False, font=dict(size=12))

    fig22 = px.funnel(driver_response.sort_values('LaneJump'), x='State/UT', y=['LaneJump','Overtake','AiIntake'])

    # state wise over-speeding in violin plot
    fig23 = px.bar(driver_response, y="Speeding", x="State/UT", color="State/UT",hover_data=driver_response.columns)
    conclusion = 'The graph shows that Tamil Nadu has the highest OverSpeeders.'
    fig23.add_annotation(text=conclusion, xref='paper', yref='paper', x=0, y=1, showarrow=False, font=dict(size=12))

    # state wise sleeping in violin plot
    fig24 = px.bar(driver_response, y="Sleeping", x="State/UT", color="State/UT",hover_data=driver_response.columns)
    conclusion = "The graph shows that Kerala has the highest accidents due to driver's sleep."
    fig24.add_annotation(text=conclusion, xref='paper', yref='paper', x=0, y=1, showarrow=False, font=dict(size=12))

    fig25 = px.funnel(driver_response.sort_values('Speeding'), x='State/UT', y=['Overtake', 'Sleeping'])

    fig26 = px.parallel_coordinates(driver_response, color="Sleeping", labels={"State/UT": "State/UT", "Sleeping": "Sleeping"})

    return render_template('graph3.html', fig21=fig21.to_html(), fig22=fig22.to_html(), fig23=fig23.to_html(),
                fig24=fig24.to_html(), fig25=fig25.to_html(), fig26=fig26.to_html())

def load_month_data():
    month_wise = pd.read_csv('Dataset/only_road_accidents_data_month2.csv')
    return month_wise

@app.route('/graph/4')
def graph_4():
    month_wise = load_month_data()
    grouped_obj = month_wise.groupby(["YEAR"]).sum()
    grouped_obj.drop(['TOTAL'], axis=1, inplace=True)
    grouped_obj
    month = ['JANUARY', 'FEBRUARY', 'MARCH', 'APRIL', 'MAY', 'JUNE', 'JULY', 'AUGUST', 'SEPTEMBER', 'OCTOBER','NOVEMBER', 'DECEMBER']
    fig27 = px.area(grouped_obj, x=grouped_obj.index, y=month, title='Accident YEAR-wise')
    conclusion = 'The graph shows accidents monthly.'
    fig27.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    grouped_obj = month_wise.groupby(['TOTAL']).sum()
    grouped_obj.drop(['YEAR'], axis=1, inplace=True)
    grouped_obj
    fig28 = px.scatter(grouped_obj, x='TOTAL', y=['JANUARY','FEBRUARY','MARCH'], title='Accidents in First Quarter', trendline='ols', log_x=True)

    fig29 = px.scatter(grouped_obj, x='TOTAL', y=['APRIL','MAY','JUNE'], title='Accidents in Second Quarter', trendline='ols', log_y=True)

    fig30 = px.scatter(grouped_obj, x='TOTAL', y=['JULY','AUGUST','SEPTEMBER'], title='Accidents in Third Quarter', trendline='ols', log_y=True)

    fig31 = px.scatter(grouped_obj, x='TOTAL', y=['OCTOBER','NOVEMBER','DECEMBER'], title='Accidents in Fourth Quarter', trendline='ols', log_y=True)

    fig32 = px.scatter(grouped_obj, x='TOTAL', y=['JANUARY','MARCH','MAY', 'JULY', 'SEPTEMBER', 'NOVEMBER'], title='Accidents in Half-Yearly basis', trendline='ols', log_y=True)

    fig33 = px.scatter(grouped_obj, x='TOTAL', y=['FEBRUARY','APRIL','JUNE', 'AUGUST', 'OCTOBER', 'DECEMBER'], title='Accidents in Half-Yearly Basis', trendline='ols', log_y=True)
    
    fig34 = px.treemap(grouped_obj, path=['TOTAL'], values='TOTAL', title='Accidents in Year-wise')

    return render_template('graph4.html', fig27=fig27.to_html(), fig28=fig28.to_html(), fig29=fig29.to_html(),
                fig30=fig30.to_html(), fig31=fig31.to_html(), fig32=fig32.to_html(), 
                fig33=fig33.to_html(), fig34=fig34.to_html())

def load_time_data():
    time_wise = pd.read_csv('Dataset/only_road_accidents_data3.csv')
    time_wise.rename(columns={
        '0-3 hrs. (Night)':'MIDNIGHT',
        '3-6 hrs. (Night)':'DAWN',
        '6-9 hrs (Day)':'MORNING',
        '9-12 hrs (Day)':'MIDDAY',
        '12-15 hrs (Day)':'AFTERNOON',
        '15-18 hrs (Day)':'DUSK',
        '18-21 hrs (Night)':'EVENING',

        '21-24 hrs (Night)':'NIGHT'}, inplace=True)
    return time_wise

@app.route('/graph/5')
def graph_5():
    time_wise = load_time_data()
    # YEARLY DATA 
    grouped_obj = time_wise.groupby(["STATE/UT"]).sum()
    grouped_obj.drop(['YEAR'], axis=1, inplace=True)
    grouped_obj
    # accident per state throughout the day
    time = ['MORNING','AFTERNOON','EVENING', 'NIGHT']
    fig35 = px.area(grouped_obj, x=grouped_obj.index, y=time, title='Accident per state throughout the day')
    conclusion = 'The graph shows that the accident in the evening is more than rest of the day.'
    fig35.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey',  showarrow=False, font=dict(size=12))

    # accident per state in morning time
    time = ['MIDNIGHT','DAWN','MORNING']
    fig36 = px.area(grouped_obj, x=grouped_obj.index, y=time, title='Accident per state in morning time')
    conclusion = 'The graph shows that the accident in the morning is more than the midnight and dawn.'
    fig36.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    # accident per state in day time
    time = ['MIDDAY','AFTERNOON','DUSK']
    fig37 = px.area(grouped_obj, x=grouped_obj.index, y=time, title='Accident per state in day time')
    conclusion = 'The graph shows that the accident in the dusk is more than the midday and afternoon.'
    fig37.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    # accident per state in night time
    time = ['EVENING','NIGHT']
    fig38 = px.area(grouped_obj, x=grouped_obj.index, y=time, title='Accident per state in night time')
    conclusion = 'The graph shows that the accident in the night is more than evening.'
    fig38.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    # TOTAL DATA 
    grouped_obj1= time_wise.groupby(["YEAR"]).sum()
    grouped_obj1
    # accident throughout the day
    time = ["MIDNIGHT","DAWN","MORNING","MIDDAY","AFTERNOON","DUSK","EVENING","NIGHT"]
    fig39 = px.funnel(grouped_obj1, x=grouped_obj1.index, y=time, title='Accident yearly')
    conclusion = 'The graph shows that accident yearly throughout the day.'
    fig39.add_annotation(text=conclusion, xref='paper', yref='paper', x=.5, y=1, bgcolor='grey', showarrow=False, font=dict(size=12))

    return render_template('graph5.html', fig35=fig35.to_html(), fig36=fig36.to_html(), fig37=fig37.to_html(),
                           fig38=fig38.to_html(), fig39=fig39.to_html())

if(__name__ == '__main__'):
    app.run(host='0.0.0.0', port=8080, debug=True)