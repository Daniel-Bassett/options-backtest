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

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

ticker = 'AAPL'
the_date = 'agg'
expiration = 'near'
agg = pickle.load(open(f'data/{ticker}/{ticker}-{the_date}-{expiration}.pickle','rb'))
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



app.layout = html.Div([

        html.Div([
            html.Div([
                html.H5('Straddle Performance', className='title_text')
            ], className='title_container twelve columns'),
            
        ], className='row flex_display'),

        dbc.Col([ dcc.Graph(id='my-graph', figure=fig)], width=12),
        

        
    

], className='mainContainer', style={'display': 'flex', 'flex-direction': 'column'})


# callback functions defined here
# @app.callback(Output(component_id='calculations', component_property='children'),
#              [Input(component_id='select_years', component_property='value')])
# def display_data(select_years):
#     pass


if __name__ == '__main__':
    app.run_server(debug=True)