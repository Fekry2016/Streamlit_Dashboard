import pandas as pd
df=pd.read_excel("case.xlsx",parse_dates=True)
df['Year']=df['Month Name'].dt.year
#print(df)
# import necessary libraries
import plotly.express as px
import streamlit as st

st.set_page_config(page_title="Sales Dashboard",
                   page_icon=":bar_chart:",
                   layout="wide")
st.dataframe(df)
st.header('Sales Dashboard')
st.markdown('<style>body {text-align: center;}</style>', unsafe_allow_html=True)

# define dashboard function
def create_dashboard(df):
    # select area to filter data
    area = st.selectbox('Select area:', df['Area'].unique())
    area_df = df[df['Area'] == area]
    # select supervisor to filter data
    supervisor = st.selectbox('Select supervisor:', area_df['Supervisor'].unique())
    supervisor_df = area_df[area_df['Supervisor'] == supervisor]
    # select store to filter data
    store = st.selectbox('Select store:', supervisor_df['Store'].unique())
    store_df = supervisor_df[supervisor_df['Store'] == store]
    # select category to filter data
    category = st.selectbox('Select category:', store_df['Category'].unique())
    category_df = store_df[store_df['Category'] == category]
    
    # calculate total revenue, revenue growth YoY, and revenue variance YoY
    revenue = category_df['Revenue'].sum()
    revenue_prev_year = df[(df['Year'] == category_df['Year'].max() - 1) & (df['Area'] == area) & (df['Supervisor'] == supervisor) & (df['Store'] == store) & (df['Category'] == category)]['Revenue'].sum()
    revenue_growth_yoy = (revenue - revenue_prev_year) / revenue_prev_year * 100
    revenue_variance_yoy = category_df[category_df['Year'] == category_df['Year'].max()]['Revenue'].sum() - category_df[category_df['Year'] == category_df['Year'].max() - 1]['Revenue'].sum()
    
    # calculate basket size value and its growth YoY
    basket_size_value = category_df['Revenue'].sum() / category_df['Number of Transactions'].sum()
    basket_size_value_prev_year = df[(df['Year'] == category_df['Year'].max() - 1) & (df['Area'] == area) & (df['Supervisor'] == supervisor) & (df['Store']==store)& (df['Category'] == category)]['Number of Transactions'].sum()
    basket_size_value_growth_yoy = (basket_size_value - basket_size_value_prev_year) / basket_size_value_prev_year * 100
    #calculate basket units and its growth YoY                                                                                                                               
    basket_units = category_df['Number of Transactions'].sum()
    basket_units_prev_year = df[(df['Year'] == category_df['Year'].max() - 1) & (df['Area'] == area) & (df['Supervisor'] == supervisor) & (df['Store'] == store) & (df['Category'] == category)]['Number of Transactions'].sum()
    basket_units_growth_yoy = (basket_units - basket_units_prev_year) / basket_units_prev_year * 100
    
    # calculate online sales contribution
    online_sales = category_df['Online Sales'].sum()
    online_sales_contribution = online_sales / revenue * 100

    # calculate private label contribution
    private_label_sales = category_df['Private Label'].sum()
    private_label_contribution = private_label_sales / revenue * 100
    
    # display dashboard elements
    st.write('Total revenue:', revenue)
    st.write('Revenue growth YoY:', revenue_growth_yoy)
    st.write('Revenue variance YoY:', revenue_variance_yoy)
    st.write('Basket size value:', basket_size_value)
    st.write('Basket size value growth YoY:', basket_size_value_growth_yoy)
    st.write('Basket units:', basket_units)
    st.write('Basket units growth YoY:', basket_units_growth_yoy)
    st.write('Online sales contribution:', online_sales_contribution)
    st.write('Private label contribution:', private_label_contribution)
    
    # create combo chart with revenue and basket size value
    fig = px.line(category_df, x='Year', y='Revenue', title='Revenue and Basket Size Value')
    fig.add_scatter(x=category_df['Year'], y=category_df['Revenue'] / category_df['Number of Transactions'], mode='lines', name='Basket Size Value')
    st.plotly_chart(fig)
    # create wrapper function to run dashboard in Streamlit
    def main(df):
        create_dashboard(df)
create_dashboard(df)
