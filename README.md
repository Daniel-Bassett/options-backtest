# options-backtest

## Introduction
This project seeks to find the historical performance of at-the-money straddles placed before earnings to answer this question: As we approach earnings,
does the rise in implied volatility outweigh the loss from time decay? I looked at the straddle pricing history of 60+ stocks over 
the last 1.5 to 2 years placed at different times 
and for different expiration dates. 
<br></br>
## Packages
#### Raw Data
<li>yfinance API for earnings dates</li>
<li>pandas_market_calendars package for getting trading days (excludes weekends/holidays)</li>
<li>polygon.io for historical options/underlying pricing</li>

#### Data Wrangling
<li>pandas</li>
<li>numpy</li>
<li>datetime</li>

#### Visualization
<li>pickle for data exporting to the visualization tool</li>
<li>plotly express for graphing</li>
<li>plotly dash  for the application</li>

## The End-User App
The end product can be found [here](https://earnings-straddle.onrender.com/)

<ol>
<li>Choose a ticker symbol</li>
<li>Choose an expiration date. "agg" shows aggregate values (mean, median, range) across all expiration dates</li>
<li>"Expiration Horizon" changes the expiration date of the straddle. All expirations analyzed occur AFTER earnings have been announced.</li>
</ol>

This heatmap illustrates how at-the-money straddles have performed leading up to earnings. The top row is for a straddle that 
was initiated 22 trading days before earnings. The bottom rows show straddles initiated much closer to earnings. The "After Earnings" column on the far right 
shows the profit/loss AFTER earnings has occurred, so prices fluctuate a lot around that point.
<br></br>
How to use this graph? Look at the aggregate for green days that have good means and medians with mins that are not too low. If you see something you like, take a closer look by looking at individual earnings dates.


Important Information:
<li>"Days" are trading days, so weekends/holidays are not included</il>
<li>Prices are end-of-day close</il>
<li>The data only goes back 1.5-2 years</il>
<li>There can be missing data due to no volume for the straddle on that day or because my data source is lacking</il>
