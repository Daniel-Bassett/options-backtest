import dash
from dash import html 
from dash import dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

# import visualization packages
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px
from plotly.subplots import make_subplots

# import yahoo finance api to get past earnings dates
import yfinance as yf

# import pandas and market calendar
import pandas_market_calendars as mcal
import pandas as pd
import numpy as np

# import time datetime
from datetime import datetime
import datetime as dt
import time

import warnings
warnings.filterwarnings('ignore')

# for importing data
import pickle


meta_tags = [{'name': 'viewport', 'content': 'width=device-width'}]
external_stylesheets = [meta_tags]

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.MINTY])
server = app.server


app.layout = html.Div([

        dbc.Row([
            html.Div([
                html.H5('Straddle Performance', className='title_text')
            ], className='title_container twelve columns'),
            
        ], className='row flex_display'),


        
        dbc.Row([
            dbc.Col([
                dcc.Dropdown(options=['AAPL', 'AMZN', 'FDX', 'NVDA', 'BAC'], value='AAPL', id='ticker'),
                dcc.Dropdown(id='earnings_dates', value='agg')
                ], width=2, class_name='flex_display'),
            dbc.Col([
                dcc.RadioItems(options=['near', 'med', 'far'], value='near', id='horizon')
                ], width=2, class_name='flex_display'),
        ]),

            
        dbc.Col([ 
            dbc.Row([
                dcc.Graph(id='graph-output')
            ],className='graph')
        ], width=9)
        
        
        

        
    

], className='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


# callback functions defined here

# get the valid earnings dates for the selected ticker
@app.callback(Output(component_id='earnings_dates', component_property='options'),
             [Input(component_id='ticker', component_property='value')])
def get_earnings_dates(ticker):
    earnings_dates = pickle.load(open(f'data/{ticker}/{ticker}-earnings-dates.pickle','rb'))
    earnings_dates.insert(0, 'agg')
    return [{'label': i, 'value': i} for i in earnings_dates]


@app.callback(Output(component_id='earnings_dates', component_property='value'),
             [Input(component_id='ticker', component_property='value')])
def get_earnings_dates(ticker):
     return 'agg'


# make graph
@app.callback(Output(component_id='graph-output', component_property='figure'),
             (Input(component_id='ticker', component_property='value')),
             (Input(component_id='earnings_dates', component_property='value')),
             (Input(component_id='horizon', component_property='value'))
             )
def display_data(ticker, earnings_date, horizon):
    if earnings_date == 'agg':
        agg = pickle.load(open(f'data/{ticker}/{ticker}-{earnings_date}-{horizon}.pickle','rb'))
        avg_days = agg['avg_days']
        fig = px.imshow(agg['mean'].round(1), color_continuous_scale=[(0,'red'), (0.5,'white'), (1.0, 'green')], range_color=(-100 ,100), text_auto=True)
        fig.update(data=[{'customdata': np.dstack((agg['median'], agg['max'], agg['min'])),
            'hovertemplate': '<b>mean:%{z:.1f}</b> <br>median: %{customdata[0]:.1f} <br>max: %{customdata[1]:.1f} <br>min: %{customdata[2]:.1f}<extra></extra>'}])
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])]),  # hide weekends, eg. hide sat to before mon])
        fig.update_yaxes(autorange='reversed')
        fig.update_layout(
            title=f'{ticker} ATM Straddle Performance in percent<br>expires ~{avg_days} days after earnings',
            title_x=0.5,
            yaxis_title='Straddle Initiated',
            xaxis_title='Trading Days Remaining',
            width=1000,
            height=1000
            )
        return fig
    else:
        try:
            df = pickle.load(open(f'data/{ticker}/{ticker}-{earnings_date}-{horizon}.pickle','rb'))
            days_df = df['days_df']
            date_df = df['date_df']
            days_after_earnings = df['days after earnings']
            fig = px.imshow(days_df.round(1), color_continuous_scale=[(0,'red'), (0.5,'white'), (1.0, 'green')], range_color=(-100 ,100), text_auto=True)
            fig.update(data=[{'customdata': np.dstack((days_df.round(1), date_df)),
                'hovertemplate': '<b>return: %{z:.1f}</b> <br>date: %{customdata[1]}<extra></extra>'}])
            fig.update_layout(
                title=f'{ticker} ATM Straddle Performance in percent (expires {days_after_earnings} days after earnings) for {earnings_date}',
                title_x=0.5,
                yaxis_title='Straddle Initiated',
                xaxis_title='Trading Days Remaining',
                width=1000,
                height=1000
            )
            fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])]),  # hide weekends, eg. hide sat to before mon])
            return fig
        except:
            fig = px.scatter_3d(title="Select a Valid Date")
            return fig

                

    
        days_df = df['days_df']
        date_df = df['date_df']
        days_after_earnings = df['days after earnings']
        fig = px.imshow(days_df.round(1), color_continuous_scale=[(0,'red'), (0.5,'white'), (1.0, 'green')], range_color=(-100 ,100), text_auto=True)
        fig.update(data=[{'customdata': np.dstack((days_df.round(1), date_df)),
            'hovertemplate': '<b>return: %{z:.1f}</b> <br>date: %{customdata[1]}<extra></extra>'}])
        fig.update_layout(
            title=f'{ticker} ATM Straddle Performance in percent (expires {days_after_earnings} days after earnings) for {earnings_date}',
            title_x=0.5,
            yaxis_title='Straddle Initiated',
            xaxis_title='Trading Days Remaining',
            width=1000,
            height=1000
        )
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])]),  # hide weekends, eg. hide sat to before mon])
        return fig



if __name__ == '__main__':
    app.run_server(debug=True)