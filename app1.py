
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Load data
data = pd.read_csv('Airbnb_after_univariate')

# define function for drawing line chart for time col with avg price
def plot_line_chart(col, price, xlabel, ylabel, title):
    
    # getting avg price grouped with specific col
    value_counts = data.groupby(col)[price].mean().sort_index()
    # keys are col unique values
    keys = np.array(value_counts.index)

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=keys, y=value_counts.values,
                             mode='lines+markers',
                             marker=dict(color='skyblue', size=10),
                             line=dict(color='grey', width=3),
                             name=price))
    
    fig.update_layout(title=title,
                      xaxis_title=xlabel,
                      yaxis_title=ylabel,
                      xaxis=dict(tickmode='array', tickvals=keys, tickfont=dict(size=10), tickangle=15),
                      yaxis=dict(tickfont=dict(size=10)))
    st.plotly_chart(fig)


# Sidebar for navigation
st.sidebar.title("Airbnb Listings Analysis")
options = ["Overview", "Neighbourhood Group Analysis", "Price Analysis", "Review Analysis","Service Fee Analysis",
          "Room Type Analysis"]
choice = st.sidebar.selectbox("Select Section", options)

# Overview section
if choice == "Overview":
    st.title("Airbnb Listings Analysis")
    st.write("This dashboard provides insights into Airbnb listings data.")
    st.image("https://digital.hbs.edu/platform-digit/wp-content/uploads/sites/2/2019/10/airbnb-678x381.png")  
    st.write('Objective : ')
    st.write('- Price Analysis : Understand factors affecting on the price.')
    st.write('- Review Analysis : Analyse reviews to know factors that affect on ratings.')
    st.write('Problem Statement : ')
    st.write(' - What are the factors that affect on price ?')
    st.write('- What characteristics of listings having higher reviews ?')
    
    st.write('''In conclusion, this project has provided a comprehensive analysis of the New York City Airbnb dataset,
    shedding light on various aspects of the short-term lodging market. Through data wrangling, exploratory data analysis 
    (EDA), and interpretation of summary statistics, we've uncovered valuable insights into listing distribution, pricing 
    dynamics, host, and review analysis.''')
    
    st.write('''Key findings include the dominance in counts of Entire home/apt listings, the variability in listing 
    counts across neighborhood groups, and the downward trend between property construction year and price. Additionally, 
    the analysis highlighted the significance of strong correlation between listing price and service fee.''')
    
    st.write(''' Furthermore, analysis on guest reviews to understand factors driving customer
    satisfaction and preferences could inform targeted marketing strategies and product improvements for Airbnb.''')
    
    ######################################################################################################
    
# Price Analysis
if choice == "Price Analysis":
    # First chart
    fig = px.scatter(data_frame=data  , x='service fee' , y='price',title="Correlation Between Price and Service Fee :")
    st.plotly_chart(fig)

    # second
    counts = data.groupby('room type').agg({
        'price': 'mean',
        'number of reviews': 'mean',
        'availability 365': 'mean'
    }).reset_index().round(0)
    melted_counts = counts.melt(id_vars='room type', var_name='Metric', value_name='value')
    fig = px.bar(melted_counts, x='room type', y='value', color='Metric', barmode='group',text_auto=True,
                title='Average Price, Reviews & avaliability for Each Room Type :',
                  labels={'room_type': 'Room Type', 'value': 'Average (Price / Num Of Reviews / Availability)'})
    st.plotly_chart(fig)
    
    # third
    fig = px.histogram(data_frame = data , x='neighbourhood group', y='price', color='room type',
              title='Average Price for each Room Type in Neighbourhood :',histfunc='avg',
              text_auto=True)
    st.plotly_chart(fig)
    
    # fourth
    avg_price = data.groupby('road')['price'].mean().nlargest(5).reset_index()
    fig1 = px.bar(avg_price, x='road', y='price', title=f'Average Price over Top 5 Roads :',
                text_auto=True)
    st.plotly_chart(fig1)
    
    # fifth
    avg_price = data.groupby('road')['price'].mean().nsmallest(5).reset_index()
    fig2 = px.bar(avg_price, x='road', y='price', title=f'Average Price over 5 Least Roads : ',
                text_auto=True)
    st.plotly_chart(fig2)
    
    ######################################################################################################
    
# Neighbourhood Analysis
if choice == "Neighbourhood Group Analysis":
    
    # first chart
    fig = px.histogram(data_frame= data , x='neighbourhood group' , title = 'Counts of Neighbourhood Group Uniques : ',
            text_auto=True , category_orders={'neighbourhood group': data['neighbourhood group'].value_counts().index})
    st.plotly_chart(fig)

    # second
    fig = px.histogram(data_frame= data , x='neighbourhood group' , 
            title = 'Counts of Neighbourhood Group Accross Room Type : ',color='room type',
            text_auto=True , category_orders={'neighbourhood group': data['neighbourhood group'].value_counts().index})
    st.plotly_chart(fig)
    
    # third
    avg_price = data.groupby('neighbourhood group')['price'].mean().reset_index()
    fig = px.bar(avg_price, x='neighbourhood group', y='price', title=f'Average Price by Neighbourhood Group :',
        text_auto=True , category_orders={'neighbourhood group': data['neighbourhood group'].value_counts().index})
    st.plotly_chart(fig)
    
    # fourth
    fig = px.histogram(data_frame = data , x='neighbourhood group', y='review rate number', color='room type',
              title='Average Reviews Rate with Neighbourhood over Room Type :',histfunc='count',
              text_auto=True)
    st.plotly_chart(fig)
    
    # fifth
    st.subheader("Map to visualize neighbourhood group with room type :")
    fig = px.scatter_mapbox(data,
           lat="lat",
           lon="long",
           opacity = 0.9,
           hover_name="neighbourhood group",
           hover_data=["neighbourhood group", "room type"],
           color="room type",
            color_discrete_sequence=px.colors.qualitative.Dark24,
           title = "Comparing places ",
           zoom=10
           )
    fig.update_layout(mapbox_style="open-street-map")
    fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0},font = dict(size=17,family="Franklin Gothic"))
    st.plotly_chart(fig)
    
    ######################################################################################################
    
#  Review Analysis   
if choice == "Review Analysis":

    # First 
    plot_line_chart("last_review_(year)",'number of reviews', "Last Review (Year)", 'Average Reviews',
                    'Average Reviews per Last Review Year :')
    
    # Second 
    plot_line_chart("last_review_(month)",'number of reviews', "Last Review (Month)", 'Average Reviews',
                    'Average Reviews per Last Review Month :')
    # Third 
    plot_line_chart("last_review_(day_name)", 'number of reviews', "Last Review (Day Name)", 'Average Reviews',
                    'Average Reviews per Last Review Day Name')
    
    ######################################################################################################

# Room Type analysis
if choice == "Room Type Analysis": 
    
    # first
    counts = data.groupby('room type').agg({
        'minimum nights': 'mean',
        'calculated host listings count': 'mean'
    }).reset_index().round(0)

    melted_counts = counts.melt(id_vars='room type', var_name='Metric', value_name='value')

    fig = px.bar(melted_counts, x='room type', y='value', color='Metric', barmode='group',text_auto=True,
                title='Average of minimum nights & calculated hosts for Each Room Type :',
                  labels={'room_type': 'Room Type', 'value': 'Average (Minimum Nights / Calculated hosts)'})
    st.plotly_chart(fig)
    
    # second
    avg_price = data.groupby('room type')['price'].mean().reset_index()
    fig = px.bar(avg_price, x='room type', y='price', title=f'Average Price by Room Type : ',
            text_auto=True , category_orders={'room type': data['room type'].value_counts().index})
    st.plotly_chart(fig)
    
        ######################################################################################################

# Service Fee analysis
if choice == "Service Fee Analysis": 
    
    # first
    grouped_data = data.groupby(['room type']).agg(
    avg_service_fee=('service fee', 'mean')
    ).reset_index()
    grouped_data['avg_service_fee'] = grouped_data['avg_service_fee'].round(1)

    fig = px.histogram(grouped_data,x='room type',y='avg_service_fee', text_auto=True)
    fig.update_layout(
        title='Average Service Fee with Room Type : ',
        xaxis_title='Room Type',yaxis_title='Average Service Fee')
    st.plotly_chart(fig)
    
    # second
    grouped_data = data.groupby(['neighbourhood group', 'review rate number']).agg(
    avg_service_fee=('service fee', 'mean')
    ).reset_index()
    grouped_data['avg_service_fee'] = grouped_data['avg_service_fee'].round(1)

    fig = px.histogram(grouped_data,x='neighbourhood group',y='avg_service_fee', color='review rate number',
                       text_auto=True)
    fig.update_layout(
        title='Average Service Fee with Nighbourhood Group & Review Rate',
        xaxis_title='Neighbourhood Group',yaxis_title='Average Service Fee')
    st.plotly_chart(fig)
