
import streamlit as st
import numpy as np
import plotly.figure_factory as ff
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

# st.title("demo app")
# st.write("welocme to streamlit")


def load_data():
    df= pd.read_csv("Unicorn_Companies.csv")
    df.loc[:, "Valuation ($)"] =df.loc[:, "Valuation"].str.replace("$","").str.replace("B","000000000").astype("int64")
    df.loc[:, "Funding ($)"] =df.loc[:, "Funding"].str.replace("$","").str.replace("Unknown","-1").str.replace("M","000000").str.replace("B","000000000").astype("int64")
    df.drop(columns=["Valuation","Funding"],axis=1,inplace=True)
    df['Date Joined'] =pd.to_datetime(df["Date Joined"])
    df.loc[:,"year joined"]=df["Date Joined"].dt.year
    df.loc[:,"Count"] = 1

    return df

df=load_data()
st.title("unicorn data companies")

# st.dataframe(df)

# create filter

industry_list = df["Industry"].unique()
selected_industry = st.sidebar.multiselect("Industry",industry_list)
filtered_industry = df[df["Industry"].isin(selected_industry)]

City_list = df["City"].unique()
selected_city = st.sidebar.multiselect("City",City_list)
filtered_city = df[df["City"].isin(selected_city)]

country_list = df['Country/Region'].unique()
selected_country = st.sidebar.multiselect('Country/Region',country_list)
filtered_country= df[df['Country/Region'].isin(selected_country)]



#this is the data if industry is selected and/if none
if selected_industry and selected_country:
   combined_table = df[df["Industry"].isin(selected_industry) & df['Country/Region'].isin(selected_country)]

   st.dataframe(combined_table)
elif selected_industry:
    st.dataframe(filtered_industry)

elif selected_country:
    st.dataframe(filtered_country)




elif selected_city:
    st.dataframe(filtered_city)

elif selected_country:
    st.dataframe(filtered_country)
    
else:
    combined_table = df
    st.dataframe(df)
    
# calculate some metrics
total_valuation=F"$ {round(df["Valuation ($)"].sum()/1000000000,2)} B"
total_funding=F"$ {round(df["Funding ($)"].sum())} B"
no_of_companies=len(df)

# dispaly these metrics
# using streamlit cointaner / column components

col1,col2,col3 = st.columns(3)
with col1:
    st.metric("no of companies", no_of_companies)

    with col2:
        st.metric("Total valuation",total_valuation)

        with col3:
            st.metric("Total funding",total_funding)

con = st.container()
# create different chart

with con:
    st.subheader("charts section")
    bar_plot_1 = sns.countplot(data=df,x=df["Industry"])
    plt.xticks(rotation=45)
    plt.ylabel("no of companies")    
    st.pyplot(bar_plot_1.get_figure())

# plotly charts
# line chart
    line_1 =px.bar(df,x="Industry",y="Count")
    st.plotly_chart(line_1)



