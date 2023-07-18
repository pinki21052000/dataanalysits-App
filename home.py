import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
# change plotly theme

st.set_page_config(layout='wide')

# function to load the data only once
@st.cache_data()
def load_titanic_data():
    df = pd.read_excel('dataset/titanic3.xls')
    return df

st.sidebar.image('images/hero.png')
with st.spinner("loading dataset"):
    df = load_titanic_data()

st.sidebar.header("Navigation")

if st.sidebar.checkbox("Show titanic dataset"):
    st.subheader('📅 Raw dataset')
    st.dataframe(df)

st.subheader('Analysis of Data')
rows,cols = df.shape
total_survivors = df['survived'].sum()
deaths = int( rows - total_survivors)
gender_count = df['sex'].value_counts()
level_wise_count = df['pclass'].value_counts()
boarding_count = df['embarked'].value_counts()
c1, c2, c3 = st.columns(3)
c1.metric('Total Records', rows)    
c2.metric('Total Columns', cols)
c3.metric('Survivors', total_survivors, delta=-deaths )
# if we have a dataframe - then we can use column names
# if we have a series - then we use index and values 
st.subheader('distribution of records')
c1, c2, c3 = st.columns(3)
fig1 = px.pie(gender_count, gender_count.index, gender_count.values, title='gender distribution')
fig2 = px.pie(level_wise_count, level_wise_count.index, level_wise_count.values, title='ship population on each level')
fig3 = px.pie(boarding_count, boarding_count.index, boarding_count.values, title='boarding count per port')
c1.plotly_chart(fig1)
c2.plotly_chart(fig2)
c3.plotly_chart(fig3)

st.subheader("Numerical data analysis")
num_cols = df.select_dtypes(include=np.number).columns.tolist()
col = st.sidebar.selectbox('Select a column to visualize', num_cols)

fig4 = px.area(df, df.index, col, title=f'column {col}')
st.plotly_chart(fig4, use_container_width=True)


