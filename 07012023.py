import pandas as pd
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
st.header('Sales Dashboard')
st.markdown('<style>body {text-align: center;}</style>', unsafe_allow_html=True)
df=pd.read_excel("case.xlsx",parse_dates=True)
df['Year']=df['Month Name'].dt.year
st.dataframe(df)
def create_dashboard(df):
    # select area, supervisor, store, or category
    group_by = st.sidebar.selectbox('Group By', ['Area Manager', 'Supervisor', 'Store', 'Category'])
    group_by_value = st.sidebar.selectbox(group_by, df[group_by].unique())
    
    # filter data by area manager, supervisor, store, or category
    filtered_df = df[df[group_by] == group_by_value]
    
    # calculate revenue and its growth YoY
    revenue = filtered_df['Revenue'].sum()
    revenue_prev_year = df[(df['Year'] == filtered_df['Year'].max() - 1) & (df[group_by] == group_by_value)]['Revenue'].sum()
    revenue_growth_yoy = (revenue - revenue_prev_year) / revenue_prev_year * 100
    
    # calculate revenue variance YoY
    revenue_variance_yoy = filtered_df['Revenue'].pct_change() * 100
    
    # calculate basket size value and its trend
    basket_size_value = filtered_df['Revenue'] / filtered_df['Number of Transactions']
    basket_size_value_trend = basket_size_value.pct_change() * 100
    
    # display dashboard elements
    st.write('Total revenue:', revenue)
    st.write('Revenue growth YoY:', revenue_growth_yoy)
    st.write('Revenue variance YoY:', revenue_variance_yoy)
    st.write('Basket size value:', basket_size_value)
    st.write('Basket size value trend:', basket_size_value_trend)
    
    # create line chart with revenue, revenue growth YoY, and revenue variance YoY
    fig = px.line(filtered_df, x='Year', y='Revenue', title='Revenue and Variance')
    fig.add_scatter(x=filtered_df['Year'], y=revenue_growth_yoy, mode='lines', name='Revenue Growth YoY')
    fig.add_scatter(x=filtered_df['Year'], y=revenue_variance_yoy, mode='lines', name='Revenue Variance YoY')
    st.plotly_chart(fig)
create_dashboard(df)
