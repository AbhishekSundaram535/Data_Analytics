import yfinance as yf
import pandas as pd
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from plotly.subplots import make_subplots

def make_graph(stock_data, revenue_data, stock):
    fig = make_subplots(rows=2, cols=1, shared_xaxes=True, subplot_titles=("Historical Share Price", "Historical Revenue"), vertical_spacing = .3)
    stock_data_specific = stock_data[stock_data.Date <= '2021--06-14']
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30']
    fig.add_trace(go.Scatter(x=pd.to_datetime(stock_data_specific.Date, infer_datetime_format=True), y=stock_data_specific.Close.astype("float"), name="Share Price"), row=1, col=1)
    fig.add_trace(go.Scatter(x=pd.to_datetime(revenue_data_specific.Date, infer_datetime_format=True), y=revenue_data_specific.Revenue.astype("float"), name="Revenue"), row=2, col=1)
    fig.update_xaxes(title_text="Date", row=1, col=1)
    fig.update_xaxes(title_text="Date", row=2, col=1)
    fig.update_yaxes(title_text="Price ($US)", row=1, col=1)
    fig.update_yaxes(title_text="Revenue ($US Millions)", row=2, col=1)
    fig.update_layout(showlegend=False,
    height=900,
    title=stock,
    xaxis_rangeslider_visible=True)
    fig.show()

#Code for GME Data
gme=yf.Ticker("GME")
data=gme.history(period="max")
gme_data=pd.DataFrame(data)
gme_data.reset_index(inplace=True)
gme_data

#Code for GME Revenue
url="https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
data=requests.get(url).text
soup=BeautifulSoup(data,'html.parser')
table=soup.find_all("tbody")[1]
gme_revenue=pd.DataFrame(columns=["Date","Revenue"])
for i,x in enumerate(table.find_all('tr')):
    col=x.find_all('td')
    date=col[0].text
    revenue=col[1].text
    gme_revenue=gme_revenue.append({"Date":date,"Revenue":revenue},ignore_index=True)
    gme_revenue["Revenue"]=gme_revenue['Revenue'].str.replace(",|\$","")
gme_revenue
    
make_graph(gme_data,gme_revenue,'GameStop')