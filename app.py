# import visualization packages
import streamlit as st
import plotly.graph_objects as go
from plotly.offline import plot
import plotly.express as px

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


def get_earnings_dates(ticker):
    stock = yf.Ticker(ticker)

    earnings_dates = stock.get_earnings_dates(limit=11).dropna(axis=0).reset_index()

    # if earnings is after market close, set earnings date to next day
    earnings_dates.loc[earnings_dates['Earnings Date'].dt.hour > 6, 'Earnings Date'] =  earnings_dates['Earnings Date'] + dt.timedelta(days=1)

    earnings_dates = earnings_dates['Earnings Date'].dt.date
    return earnings_dates.to_list()


def main():
    # get the desired ticker symbol from user
    ticker = st.selectbox(label='Ticker', options=['AAPL'])

    # fetch valid earnings dates
    earnings_dates = get_earnings_dates(ticker)
    earnings_dates = [adate.strftime('%Y-%m-%d') for adate in earnings_dates]
    earnings_dates.append('agg')
    
    # get desired earnings date from user
    the_date = st.selectbox(label='Date or Type', options=earnings_dates)

    # get desired expiration horizon from user
    expiration = st.selectbox(label='Choose an expiration horizon', options=['near', 'med', 'far'])


    if the_date == 'agg':
        agg = pickle.load(open(f'data/{ticker}/{ticker}-{the_date}-{expiration}.pickle','rb'))
        avg_days = agg['avg_days']
        fig = px.imshow(agg['mean'].round(1), color_continuous_scale=[(0,'red'), (0.5,'white'), (1.0, 'green')], range_color=(-100 ,100), text_auto=True)
        fig.update(data=[{'customdata': np.dstack((agg['median'], agg['max'], agg['min'])),
            'hovertemplate': '<b>mean:%{z:.1f}</b> <br>median: %{customdata[0]:.1f} <br>max: %{customdata[1]:.1f} <br>min: %{customdata[2]:.1f}'}])
        fig.update_xaxes(rangebreaks=[dict(bounds=["sat", "mon"])]),  # hide weekends, eg. hide sat to before mon])
        fig.update_yaxes(autorange='reversed')
        fig.update_layout(
            title=f'{ticker} ATM Straddle Performance in percent<br>expires ~{avg_days} days after earnings',
            title_x=0.5,
            yaxis_title='Straddle Initiated',
            xaxis_title='Trading Days Remaining')


    fig = go.Figure(data=go.Heatmap(z=agg['mean']))
    fig.update_coloraxes(color_continuous_scale=[(0,'red'), (0.5,'white'), (1.0, 'green')])
    fig.update(data=[{'customdata': np.dstack((agg['median'], agg['max'], agg['min'])),
        'hovertemplate': '<b>mean:%{z:.1f}</b> <br>median: %{customdata[0]:.1f} <br>max: %{customdata[1]:.1f} <br>min: %{customdata[2]:.1f}<extra></extra>'}])
    fig.update_yaxes(autorange='reversed')

    st.plotly_chart(fig)

if __name__ == '__main__':
    main()
