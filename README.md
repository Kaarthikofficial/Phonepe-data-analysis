# Phonepe-data-analysis
This dashboard is created to visualize the analysis of data received 
from PhonePe git repository. It is built in python using streamlit and plotly.

## Segments of dashboard
* Overall transaction analysis
* Transaction analysis by payment modes
* User analysis
* Brand analysis

## Choropleth map

### Overall transaction analysis
**State transaction map**
`I have created a choropleth map using plotly to map the total transactions happened in each state by each quarter of every year. From this, we can 
infer the volume of transactions and their growth in each state. Along with that, a bar graph is built in motive to bring up the predominant contributors 
and minor contributors among them.`

**District transaction map**
`This is created in overlapping of the choropleth map with district wise transaction using scatter geo. It will mainly gives a deep meaning of
transaction development in various cities. I replicate the same bar graph representation which I used in state map to get some deep insights`

## Bar graphs and Donut chart

### Transaction analysis by payment modes

**Transaction volume**
`I create this bar chart to find the volume of transaction happened in terms of each payment modes. With this, we can arrive at the
conclusion which mode has done more often.`

**Transaction amount**
`This is quite similar to the previous one but the only change is transaction amount used instead of volume. This might bring
some info on the contribution of value by each payment modes.`

**Average transaction**
`This one is created to identify the average transaction value per payment modes in each quarter of every year.`

### Transaction during covid
It is created in view of impact by covid on mode of transaction in the time-line of q1-2021 to q2-2022. And actually, by covid the amount 
of transactions as well as amount of transactions were enormously raised.

## Choropleth map and donut chart

**Registered user analysis**
`Registered users are the ones who play vital role in the growth of any organization. This choropleth map will bring some good
info on the raise of users by each quarter of every year. And also with respect to some districts created in the additional tab.`

### Brand analysis
Total users per brand in each quarter of every year can be identified with the help of donut chart. Added to that, the
count of total users in each brand is represented by bar chart in the additional tab.

*Streamlit app link:* [Phonepe-data-analysis](https://kaarthikofficial-phonepe-data-analysis-phonepe-ssphfb.streamlit.app/)
