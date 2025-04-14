import streamlit as st
import plotly.express as px
import pandas as pd
import geopandas as gpd

st.set_page_config(layout="wide")
st.title("Data Dashboard For Household Water Access In Kenya")

# Read the file containing
waterdata= gpd.read_file ('assets/ken_water_county_new.geojson')
with st.container():
    col1,col2=st.columns([1,1], border=True) 
    with col1:
        selected_category= st.selectbox('Select Option: Choose a parameter to view', waterdata.columns[7:14])
    
    with col2:
            st.write("This dashboard allows you to view the different ways that Kenyan households access water. Use the select option to view the particular parameter you are interested in. You can also hoover your mouse on the map and graph to get more information. A data table is also available for a deeper analysis of the numbers")
cutoff=[0,20,40,60,80,100]
labels= ["Very Low:0-20%", "Low:20-40%", "Average:40-60%", "High:60-80%", "Very High:80-100%"]
#score =pd.cut(waterdata[selected_category], bins=cutoff, labels= labels)
waterdata["Score"] =pd.cut(waterdata[selected_category], bins=cutoff, labels= labels)
waterdata.sort_values(['Score'], inplace=True)
#Define how the categories will be ordered
category_order_list = [
        'Very High:80-100%',
        'High:60-80%',
        'Average:40-60%',
        'Low:20-40%',
        'Very Low:0-20%'
]  
waterdata_select=waterdata.filter(items=['County Name','County ID','Surface Water','Ground Water','Piped Water','Bottled Water','Rain Water','Water Vendor','Public Tap'])
waterdata_select['Score']= pd.cut(waterdata[selected_category], bins=cutoff, labels= labels) # Adds a column called score to the water_select datafram which has cutoff values
waterdata_select=waterdata_select.dropna() # drops the values with none
waterdata_select=waterdata_select.sort_values(by='County ID') # sorts values accoding to the count ID
waterdata_select=waterdata_select.filter(items=['County Name','County ID', selected_category,'Score'])
waterdata_select = waterdata_select.set_index('County ID') # Removes the index and sets county id as the index

# Define the color map
color_map= {
           'Very High:80-100%':'#071c90',
           'High:60-80%': '#624cab',
           'Average:40-60%': '#758ecd',
           'Low:20-40%':'#97a5fe', 
           'Very Low:0-20%':'#d1d8ff'
            }
with st.container():
    col1,col2=st.columns([1.5,1], border=True) 
    with col1:
        #st.write("You selected:", selected_category)#This line just verifies that the columns are selected
        figure= px.choropleth_map(waterdata,
                      locations=waterdata.index,
                      geojson=waterdata.geometry,
                      color= waterdata.Score, # This uses the selected column as input
                      color_discrete_map= color_map,
                      zoom=5,
                      center = {"lat": -0.0, "lon": 37.0},
                      height= 600,
                      hover_data=['County Name', selected_category, 'Score'] # This adds county name to hover options
                                                                )
        figure.update_layout(
                    title_text = f'Percentage of Kenyan Households using {selected_category} per county',
                    legend_title_text="Rating Score", # Updates the title of the legend
                    map_style="carto-positron", # Puts a background map on the choropleth
                    legend_traceorder="reversed", # Reverses the sorting order for lengend so it is from vhigh to vlow
                    # Style the hoover label
                    hoverlabel=dict(
                        bgcolor="#F0F0F0",
                        bordercolor="#BEBEBE",
                        font_size=12,
                        font_family="Arial",
                        font_color="#484848"                       
                     ),
                    # Puts the legend at the bottom
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=0,
                        xanchor="center",
                        x=0.5
                    ),
                     margin=dict(l=50, r=50, t=100, b=50)
                                   
                    )
        figure.update_traces(
                # This updates the data in the hover_data. It has 3 elements hence from 0-2. Make sure to add this to figure.update _traces and not update figure otherwise it wont work. To automatically pick the selected category, use an f-string but remember to double the curly brackects on the customdata becasue it already has a curly bracket
                  hovertemplate= "<b>County:</b> %{customdata[0]}<br>" +
                  f"<b>{selected_category}:</b> %{{customdata[1]}}%<br>" +
                  "<b>Rating Score:</b> %{customdata[2]}" +
                  "<extra></extra>",
                # Styling the map borders
                 marker_line_width=1.0,
                 marker_opacity=0.9, 
                 marker_line_color= "#e7e7e7",
                                  )
        st.plotly_chart(figure)
    with col2:
     # Draw a bar graph linked to the selected options
        score_summary = waterdata.groupby('Score').size().reset_index(name='Count of Counties')
        fig_bar = px.bar(
                score_summary,
                x='Score',
                y='Count of Counties',
                color= 'Score',
                color_discrete_map=color_map,
                title= f'Number of Counties In Each Category For {selected_category}',
                labels={ # Optional: Rename axes for clarity
                'Score': 'Rating Score Category',
                'Count of Counties': 'Number of Counties'
                },
                text='Count of Counties' # Optional: Display the count value on top of each bar
                )
        fig_bar.update_layout(
                height=600,
                # Style the hoover label
                hoverlabel=dict(
                bgcolor="#F0F0F0",
                bordercolor="#BEBEBE",
                font_size=12,
                font_family="Arial",
                font_color="#484848"                       
                ),
        #showlegend=False
        legend=dict(
            orientation="h",
            yanchor="top",
            y=-0.5,
            xanchor="center",
            x=0.5
            ),
        margin=dict(l=50, r=50, t=100, b=50)
        )
        st.plotly_chart(fig_bar)

with st.container():    
    col1,col2=st.columns([1.5,1], border=True) 
    with col1:
        if selected_category=="Surface Water":
            with open ("assets/surface-water.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Ground Water":
             with open ("assets/ground-water.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Piped Water":
            with open ("assets/piped-water.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Bottled Water":
            with open ("assets/bottled-water.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Rain Water":
            with open ("assets/rain-water.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Water Vendor":
            with open ("assets/water-vendor.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
        elif selected_category=="Public Tap":
            with open ("assets/public-tap.md") as f:
                st.markdown(f.read(), unsafe_allow_html=True)
    with col2:
        if selected_category=="Surface Water":
            st.image("assets/surface-water.jpg",caption="Women fetching water at a river")
        elif selected_category=="Ground Water":
            st.image("assets/ground-water.jpg",caption="Children getting water from a well")
        elif selected_category=="Piped Water":
            st.image("assets/piped-water.jpg",caption="A boy drinking from water piped into the compound")
        elif selected_category=="Bottled Water":
            st.image("assets/bottled-water.jpg",caption="Bottled water sellers")
        elif selected_category=="Rain Water":
            st.image("assets/rain-water.jpg",caption="Rain water harvesting")
        elif selected_category=="Water Vendor":
            st.image("assets/water-vendor.jpg",caption="Water delivery by a water vendor")
        elif selected_category=="Public Tap":
            st.image("assets/public-tap.jpg",caption="Children fectching water at a public tap")
with st.container(border=True):
    st.write("### Data Table For", selected_category,"Household Usage")
    st.dataframe(waterdata_select)