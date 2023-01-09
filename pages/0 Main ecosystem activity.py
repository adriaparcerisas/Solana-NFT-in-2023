#!/usr/bin/env python
# coding: utf-8

# In[18]:


import streamlit as st
import pandas as pd
import numpy as np
from shroomdk import ShroomDK
import seaborn as sns
import matplotlib.pyplot as plt
import matplotlib.dates as md
import matplotlib.ticker as ticker
import numpy as np
import plotly.express as px
sdk = ShroomDK("7bfe27b2-e726-4d8d-b519-03abc6447728")


# In[19]:


st.title('Main ecosystem activity')


# In[20]:


st.markdown('This part shows the basic activity trends on **Solana** ecosystem. It is intended to provide an overview of the current activity on Solana.')


# In[5]:


st.markdown('In this section, we are gonna track the basic activity metrics registered on **Solana Ecosystem** so far such as:') 
st.write('- Evolution of transactions, transactors and transactions per user')
st.write('- Evolution of NFT sales, buyers and buys per user')
st.write('- Average user activity')
st.write('')


# In[10]:


sql = f"""
with 
t1 as (
SELECT
trunc(x.block_timestamp,'day') as date,
count(distinct x.tx_id) as transactions,
count(distinct x.signers[0]) as active_users,
transactions/active_users as avg_tx_per_user,
sum(fee/pow(10,6)) as fees,
avg(fee/pow(10,6)) as avg_tx_fee
  from solana.core.fact_transactions x
  where x.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  ),
  t2 as (
  select
trunc(y.block_timestamp,'day') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from solana.core.fact_swaps y
  where y.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'day') as date,
count(distinct z.tx_id) as nft_sales,
count(distinct z.purchaser) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from solana.core.fact_nft_sales z
  where z.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  )
  SELECT
  t1.date, 
  transactions,sum(transactions) over (order by t1.date) as cum_transactions,
  active_users,sum(active_users) over (order by t1.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t1.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t1.date) as cum_swaps,
  swappers,sum(swappers) over (order by t1.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t1.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t1.date) as cum_buyers,
  nft_bought_per_user
  from t1,t2,t3 where t1.date=t2.date and t1.date=t3.date
order by 1 asc 
"""

sql2 = f"""
with 
t1 as (
SELECT
trunc(x.block_timestamp,'week') as date,
count(distinct x.tx_id) as transactions,
count(distinct x.signers[0]) as active_users,
transactions/active_users as avg_tx_per_user,
sum(fee/pow(10,6)) as fees,
avg(fee/pow(10,6)) as avg_tx_fee
  from solana.core.fact_transactions x
  where x.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  ),
  t2 as (
  select
trunc(y.block_timestamp,'week') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from solana.core.fact_swaps y
  where y.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'week') as date,
count(distinct z.tx_id) as nft_sales,
count(distinct z.purchaser) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from solana.core.fact_nft_sales z
  where z.block_timestamp>=current_date-INTERVAL '1 MONTH'
  group by 1
  )
  SELECT
  t1.date, 
  transactions,sum(transactions) over (order by t1.date) as cum_transactions,
  active_users,sum(active_users) over (order by t1.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t1.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t1.date) as cum_swaps,
  swappers,sum(swappers) over (order by t1.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t1.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t1.date) as cum_buyers,
  nft_bought_per_user
  from t1,t2,t3 where t1.date=t2.date and t1.date=t3.date
order by 1 asc 
"""

sql3 = f"""
with 
t1 as (
SELECT
trunc(x.block_timestamp,'month') as date,
count(distinct x.tx_id) as transactions,
count(distinct x.signers[0]) as active_users,
transactions/active_users as avg_tx_per_user,
sum(fee/pow(10,6)) as fees,
avg(fee/pow(10,6)) as avg_tx_fee
  from solana.core.fact_transactions x
  where x.block_timestamp>=current_date-INTERVAL '2 MONTHS'
  group by 1
  ),
  t2 as (
  select
trunc(y.block_timestamp,'month') as date,
count(distinct y.tx_id) as swaps,
count(distinct swapper) as swappers,
swaps/swappers as avg_swaps_per_swapper
  from solana.core.fact_swaps y
  where y.block_timestamp>=current_date-INTERVAL '2 MONTHS'
  group by 1
  ),
  t3 as (
  select
  trunc(z.block_timestamp,'month') as date,
count(distinct z.tx_id) as nft_sales,
count(distinct z.purchaser) as nft_buyers,
nft_sales/nft_buyers as nft_bought_per_user
  from solana.core.fact_nft_sales z
  where z.block_timestamp>=current_date-INTERVAL '2 MONTHS'
  group by 1
  )
  SELECT
  t1.date, 
  transactions,sum(transactions) over (order by t1.date) as cum_transactions,
  active_users,sum(active_users) over (order by t1.date) as cum_users,
  avg_tx_per_user,
  fees,sum(fees) over (order by t1.date) as cum_fees,
  avg_tx_fee,
  swaps,sum(swaps) over (order by t1.date) as cum_swaps,
  swappers,sum(swappers) over (order by t1.date) as cum_swappers,
  avg_swaps_per_swapper,
  nft_sales,sum(nft_sales) over (order by t1.date) as cum_sales,
  nft_buyers,sum(nft_buyers) over (order by t1.date) as cum_buyers,
  nft_bought_per_user
  from t1,t2,t3 where t1.date=t2.date and t1.date=t3.date
order by 1 asc 
"""

# In[11]:


st.experimental_memo(ttl=21600)
def compute(a):
    data=sdk.query(a)
    return data

results = compute(sql)
df = pd.DataFrame(results.records)
df.info()

results2 = compute(sql2)
df2 = pd.DataFrame(results2.records)
df2.info()

results3 = compute(sql3)
df3 = pd.DataFrame(results3.records)
df3.info()
#st.subheader('Terra general activity metrics regarding transactions')
#st.markdown('In this first part, we can take a look at the main activity metrics on Terra, where it can be seen how the number of transactions done across the protocol, as well as some other metrics such as fees and TPS.')


# In[22]:


import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily transactions", secondary_y=False)
fig1.update_yaxes(title_text="Total transactions", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly transactions", secondary_y=False)
fig2.update_yaxes(title_text="Total transactions", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['transactions'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_transactions'],
                name='# of transactions',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly transactions',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly transactions", secondary_y=False)
fig3.update_yaxes(title_text="Total transactions", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily transactions", "Weekly transactions", "Monthly transactions"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[15]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily active users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily active users", secondary_y=False)
fig1.update_yaxes(title_text="Total active users", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly active users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly active users", secondary_y=False)
fig2.update_yaxes(title_text="Total active users", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['active_users'],
                name='Users',
                marker_color='rgb(132, 243, 132)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_users'],
                name='Users',
                marker_color='rgb(21, 174, 21)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly active users',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly active users", secondary_y=False)
fig3.update_yaxes(title_text="Total active users", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily active users", "Weekly active users", "Monthly active users"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


# In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily swaps", secondary_y=False)
fig1.update_yaxes(title_text="Total swaps", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly swaps", secondary_y=False)
fig2.update_yaxes(title_text="Total swaps", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swaps'],
                name='# of swaps',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swaps'],
                name='# of swaps',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly swaps',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly swaps", secondary_y=False)
fig3.update_yaxes(title_text="Total swaps", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily swaps", "Weekly swaps", "Monthly swaps"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
    
    
    # In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily swappers", secondary_y=False)
fig1.update_yaxes(title_text="Total swappers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly swappers", secondary_y=False)
fig2.update_yaxes(title_text="Total swappers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['swappers'],
                name='# of swappers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_swappers'],
                name='# of swappers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly swappers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly swappers", secondary_y=False)
fig3.update_yaxes(title_text="Total swappers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily swappers", "Weekly swappers", "Monthly swappers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)


    
    
    


# In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['nft_sales'],
                name='# of nft sales',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_sales'],
                name='# of nft sales',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily NFT sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily sales", secondary_y=False)
fig1.update_yaxes(title_text="Total sales", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['nft_sales'],
                name='# of sales',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_sales'],
                name='# of sales',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly sales", secondary_y=False)
fig2.update_yaxes(title_text="Total sales", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['nft_sales'],
                name='# of sales',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_sales'],
                name='# of sales',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly sales',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly sales", secondary_y=False)
fig3.update_yaxes(title_text="Total sales", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily sales", "Weekly sales", "Monthly sales"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
    
    
    
    
    # In[16]:


# Create figure with secondary y-axis
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily buyers", secondary_y=False)
fig1.update_yaxes(title_text="Total buyers", secondary_y=True)


# Create figure with secondary y-axis
fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df['date'],
                y=df2['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df['date'],
                y=df2['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly buyers", secondary_y=False)
fig2.update_yaxes(title_text="Total buyers", secondary_y=True)


# Create figure with secondary y-axis
fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df['date'],
                y=df3['nft_buyers'],
                name='# of buyers',
                marker_color='rgb(229, 141, 146)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df['date'],
                y=df3['cum_buyers'],
                name='# of buyers',
                marker_color='rgb(119, 27, 138)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly buyers',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly buyers", secondary_y=False)
fig3.update_yaxes(title_text="Total buyers", secondary_y=True)

tab1, tab2, tab3 = st.tabs(["Daily buyers", "Weekly buyers", "Monthly buyers"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)



    
fig1 = make_subplots(specs=[[{"secondary_y": True}]])

fig1.add_trace(go.Bar(x=df['date'],
                y=df['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig1.add_trace(go.Line(x=df['date'],
                y=df['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig1.update_layout(
    title='Daily user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig1.update_yaxes(title_text="Daily user activity", secondary_y=False)
fig1.update_yaxes(title_text="Total user activity", secondary_y=True)


fig2 = make_subplots(specs=[[{"secondary_y": True}]])

fig2.add_trace(go.Bar(x=df2['date'],
                y=df2['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig2.add_trace(go.Line(x=df2['date'],
                y=df2['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig2.update_layout(
    title='Weekly user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig2.update_yaxes(title_text="Weekly user activity", secondary_y=False)
fig2.update_yaxes(title_text="Total user activity", secondary_y=True)


fig3 = make_subplots(specs=[[{"secondary_y": True}]])

fig3.add_trace(go.Bar(x=df3['date'],
                y=df3['avg_tx_per_user'],
                name='# of transactions',
                marker_color='rgb(163, 203, 249)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['avg_swaps_per_swapper'],
                name='# of swaps',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y'))
fig3.add_trace(go.Line(x=df3['date'],
                y=df3['nft_bought_per_user'],
                name='# of nfts',
                marker_color='rgb(11, 78, 154)'
                , yaxis='y2'))

fig3.update_layout(
    title='Monthly user activity',
    xaxis_tickfont_size=14,
    legend=dict(
        x=0,
        y=1.0,
        bgcolor='rgba(255, 255, 255, 0)',
        bordercolor='rgba(255, 255, 255, 0)'
    ),
    barmode='group',
    bargap=0.15, # gap between bars of adjacent location coordinates.
    bargroupgap=0.1 # gap between bars of the same location coordinate.
)

# Set y-axes titles
fig3.update_yaxes(title_text="Monthly user activity", secondary_y=False)
fig3.update_yaxes(title_text="Total user activity", secondary_y=True)


tab1, tab2, tab3 = st.tabs(["Daily user activity", "Weekly user activity", "Monthly user activity"])

with tab1:
    st.plotly_chart(fig1, theme="streamlit", use_container_width=True)

with tab2:
    st.plotly_chart(fig2, theme="streamlit", use_container_width=True)

with tab3:
    st.plotly_chart(fig3, theme="streamlit", use_container_width=True)
