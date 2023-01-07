
import streamlit as st
import pandas as pd
import plotly.express as px

# load data into dataframe
df = pd.read_excel('case.xlsx')
df=df.fillna(10000)

# create dashboard function
def create_dashboard(df):
    # select area, supervisor, and store
    area = st.sidebar.selectbox('Area', df['Area'].unique())
    supervisor = st.sidebar.selectbox('Supervisor', df['Supervisor'].unique())
    store = st.sidebar.selectbox('Store', df['Store'].unique())
    
    # filter data by area, supervisor, and store
    filtered_df = df[(df['Area'] == area) & (df['Supervisor'] == supervisor) & (df['Store'] == store)]
    
    # calculate revenue and its growth YoY
    revenue = filtered_df['Revenue'].sum()
    revenue_prev_year = df[(df['Year'] == filtered_df['Year'].max() - 1) & (df['Area'] == area) & (df['Supervisor'] == supervisor) & (df['Store'] == store)]['Revenue'].sum()
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
# create wrapper function to run dashboard in Streamlit
#def main(df):
    #st.beta_container(lambda: create_dashboard(df))

#if __name__ == '__main__':
    #main(df)
