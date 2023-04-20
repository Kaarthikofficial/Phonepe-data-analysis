import pandas as pd
import plotly.express as px
import streamlit as st
import warnings
import plotly.graph_objects as go
import mysql.connector
from plotly.subplots import make_subplots
warnings.filterwarnings('ignore', category=DeprecationWarning)
st.set_page_config(layout='wide')

# Connect to the AWS RDS MySQL instance
cnx = mysql.connector.connect(user=st.secrets["user"], password=st.secrets["password"],
                              host=st.secrets["host"], port=3306, database=st.secrets["database"])

cursor = cnx.cursor()

query = "SELECT * FROM Aggregated_transaction_data"
cursor.execute(query)

data = cursor.fetchall()

# Read a table as a dataframe
Aggregated_Transaction = pd.DataFrame(data, columns=[i[0] for i in cursor.description])
# print(Aggregated_Transaction.info())
# Aggregated_Transaction = pd.read_csv('phonepe data/Aggregated_Transaction_Table.csv')
Aggregated_User_Summary = pd.read_csv('phonepe data/Aggregated_User_Table.csv')
Aggregated_User = pd.read_csv('phonepe data/Aggregated_Brands_Table.csv')
Districts = pd.read_csv('phonepe data/Data_Map_Districts_Longitude_Latitude.csv')
Transaction_Table = pd.read_csv('phonepe data/Map_transaction_Table.csv')
User_Table = pd.read_csv('phonepe data/Map_user_Table.csv')
State_Table = pd.read_csv('phonepe data/Longitude_Latitude_State_Table.csv')


def clean_text(text):
    # Remove punctuation and replace with space
    text = text.translate(str.maketrans('-', ' '))
    # Convert first letter of each word to caps
    text = ' '.join(word.capitalize() for word in text.split())
    return text


c1, c2 = st.columns(2)

with c1:
    Year = st.selectbox('Year', (2018, 2019, 2020, 2021, 2022), key=1)
with c2:
    Quarter = st.selectbox('Quarter', (1, 2, 3, 4), key=2)

Transaction_Table['F_State'] = Transaction_Table['State'].apply(clean_text)
Transaction_Table['F_State'] = Transaction_Table['F_State'].str.replace(' Islands', '')
Transaction_data = Transaction_Table.loc[(Transaction_Table['Year'] == Year) &
                                         (Transaction_Table['Quarter'] == Quarter)].copy()

Transaction_df = Transaction_data.groupby(['Year', 'Quarter',
                                           'F_State'])[['Total_Transactions_count', 'Total_Amount']].sum()
Transaction_df = Transaction_df.rename(columns={'Total_Transactions_count': 'Total_Transactions_count',
                                                'Total_Amount': 'Total_Amount'})


# Creation of state-wise plots
State_Transaction_df = Transaction_df.copy()
State_Table = State_Table.sort_values(by=['state'], ascending=False)
State_Transaction_df = State_Transaction_df.sort_values(by=['F_State'], ascending=False)
Transaction_vol = State_Transaction_df['Total_Transactions_count'].values
Transaction_amount = State_Transaction_df['Total_Amount'].values
State_Table['Transactions'] = Transaction_vol
State_Table['Amount'] = Transaction_amount

fig_ch = px.choropleth(
                    State_Table,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Transactions',
                    color_continuous_scale='emrld',
                    hover_data={'Amount': ":,.2s", 'Transactions': ":,.2s"},
                    height=550,
                    width=700
                    )

fig_ch.update_geos(fitbounds="locations", visible=False)
fig_ch.update_layout(
    title='State transaction Map',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='mercator'
    )
)
# Creation of district-wise scatter plots
Districts.rename(columns={'District': 'Place_Name'}, inplace=True)
match = Transaction_data['Place_Name'][Transaction_data['Place_Name'].isin(Districts['Place_Name'])]
Latitude = Districts.loc[Districts['Place_Name'].isin(match), 'Latitude']
Longitude = Districts.loc[Districts['Place_Name'].isin(match), 'Longitude']
Transaction_data['Latitude'] = Latitude.values
Transaction_data['Longitude'] = Longitude.values
Transaction_data['Year_quarter'] = str(Year) + '-Q' + str(Quarter)

sc = px.scatter_geo(Transaction_data,
                    lon='Longitude',
                    lat='Latitude',
                    size='Total_Transactions_count',
                    hover_name='Place_Name',
                    hover_data=['Total_Transactions_count', 'Total_Amount', 'Year_quarter']
                    )
sc.update_traces(marker=dict(color="red", line_width=1))
color = '#ABEBC6'
fig = px.choropleth(
                    State_Table,
                    geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                    featureidkey='properties.ST_NM',
                    locations='state',
                    color='Amount',
                    color_continuous_scale=[[0, color], [1, color]],
                    height=550,
                    width=700
                    )

fig.update_geos(fitbounds="locations", visible=False)

fig.add_trace(sc.data[0])
fig.update_layout(
    title='District transaction Map',
    geo=dict(
        showframe=False,
        showcoastlines=False,
        projection_type='mercator'
    )
)

# Top performing states
Top_states = State_Table.groupby('state')['Transactions'].sum().nlargest(5).reset_index(name='Top_transactions')
Low_states = State_Table.groupby('state')['Transactions'].sum().nsmallest(5).reset_index(name='Low_transactions')

t1, t2 = st.tabs(["State wise", "District wise"])
with t1:
    c3, c4 = st.columns((3, 2))
    with c3:
        st.plotly_chart(fig_ch, use_container_width=False)
    with c4:
        fig_br = make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=True)
        fig_br.add_trace(go.Bar(x=list(Top_states['state']), y=Top_states['Top_transactions'],
                                marker=dict(color='#17A589'), name='Top transactions'), row=1, col=1)
        fig_br.add_trace(go.Bar(x=list(Low_states['state']), y=Low_states['Low_transactions'],
                                marker=dict(color='#E74C3C'), name='Least transactions'), row=2, col=1)
        fig_br.update_layout(height=500, width=500, title_text="Transaction Performance by states")
        st.plotly_chart(fig_br)

Top_districts = Transaction_data.groupby('Place_Name')['Total_Transactions_count'].sum().nlargest(5).\
    reset_index(name='Top_transactions')
Low_districts = Transaction_data.groupby('Place_Name')['Total_Transactions_count'].sum().nsmallest(5).\
    reset_index(name='Low_transactions')

with t2:
    c5, c6 = st.columns((3, 2))
    with c5:
        st.plotly_chart(fig, use_container_width=False)
    with c6:
        fig_br = make_subplots(rows=2, cols=1, shared_xaxes=True, shared_yaxes=True)
        fig_br.add_trace(go.Bar(x=list(Top_districts['Place_Name']), y=Top_districts['Top_transactions'],
                                marker=dict(color='#17A589'), name='Top transactions'), row=1, col=1)
        fig_br.add_trace(go.Bar(x=list(Low_districts['Place_Name']), y=Low_districts['Low_transactions'],
                                marker=dict(color='#E74C3C'), name='Least transactions'), row=2, col=1)
        fig_br.update_layout(height=500, width=500, title_text="Transaction Performance by districts")
        st.plotly_chart(fig_br)

Aggregated_Transaction['Average_transaction'] = Aggregated_Transaction['Total_Amount'] / Aggregated_Transaction['Total_Transactions']
# Average_transaction = pd.DataFrame(Aggregated_Transaction['Total_Amount'].values / Aggregated_Transaction['Total_Transactions'].values, columns=['Avg_transaction'])
# Aggregated_Transaction['Avg_transaction'] = Average_transaction['Avg_transaction'].values
Aggregated_Transaction['Year_quarter'] = Aggregated_Transaction['Year'].astype(str) + '-Q' + \
                                         Aggregated_Transaction['Quarter'].astype(str)


t3, t4 = st.tabs(['Transactions by each state', 'Transactions during covid'])
with t3:
    c7, c8, c9 = st.columns(3)

    with c7:
        State = st.selectbox('State', tuple(Aggregated_Transaction['State'].unique()), key=3)
    with c8:
        Year = st.selectbox('Year', tuple(Aggregated_Transaction['Year'].unique()), key=4)
    with c9:
        Quarter = st.selectbox('Quarter', tuple(Aggregated_Transaction['Quarter'].unique()), key=5)

    Aggregated_Transaction_df = Aggregated_Transaction.loc[(Aggregated_Transaction['Year'] == Year) &
                                                           (Aggregated_Transaction['State'] == State) &
                                                           (Aggregated_Transaction['Quarter'] == Quarter)].copy()

    c10, c11, c12 = st.columns([1, 1, 1])
    with c10:
        layout = go.Layout(title='Total transaction volume', xaxis=dict(title='Payment_mode'),
                           yaxis=dict(title='Total_transactions'), width=300, height=500)

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x=Aggregated_Transaction_df['Payment_Mode'],
                             y=Aggregated_Transaction_df['Total_Transactions'],
                             marker=dict(line=dict(width=1)), textposition='outside', name='Volume'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(texttemplate='%{y:.2s}')
        st.plotly_chart(fig)
    with c11:
        layout = go.Layout(title='Total transaction amount', xaxis=dict(title='Payment_mode'),
                           yaxis=dict(title='Total_transactions'), width=300, height=500)

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x=Aggregated_Transaction_df['Payment_Mode'],
                             y=Aggregated_Transaction_df['Total_Amount'],
                             marker=dict(line=dict(width=1)), textposition='outside', name='Amount'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(texttemplate='%{y:.2s}')
        st.plotly_chart(fig)
    with c12:
        layout = go.Layout(title='Avg_transaction_amount')
        fig = go.Figure(data=[go.Pie(labels=Aggregated_Transaction_df['Payment_Mode'],
                                     values=Aggregated_Transaction_df['Avg_transaction'], hole=0.5)], layout=layout)
        st.plotly_chart(fig)
with t4:
    c13, c14 = st.columns((2, 2))
    Payment_mode = st.selectbox('Payment_mode', tuple(Aggregated_Transaction['Payment_Mode'].unique()), key=6)

    with c13:
        year_quarter = ['2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4', '2022-Q1', '2022-Q2']
        Transaction_year_df = Aggregated_Transaction.loc[(Aggregated_Transaction['Year_quarter'].isin(year_quarter)) &
                                                         (Aggregated_Transaction['Payment_Mode'] == Payment_mode)].copy()
        transaction = Transaction_year_df.groupby(['Payment_Mode', 'Year_quarter'])['Total_Transactions'].sum().\
            reset_index(name='Transactions')

        layout = go.Layout(title='Total transaction volume', xaxis=dict(title='Year-quarter'),
                           yaxis=dict(title='Total_transactions'), width=600, height=500)

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x=transaction['Year_quarter'],
                             y=transaction['Transactions'],
                             name='Volume'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(texttemplate='%{y:.2s}')
        st.plotly_chart(fig)

    with c14:
        year_quarter = ['2021-Q1', '2021-Q2', '2021-Q3', '2021-Q4', '2022-Q1', '2022-Q2']
        Transaction_year_df = Aggregated_Transaction.loc[(Aggregated_Transaction['Year_quarter'].isin(year_quarter)) &
                                                         (Aggregated_Transaction[
                                                              'Payment_Mode'] == Payment_mode)].copy()
        transaction = Transaction_year_df.groupby(['Payment_Mode', 'Year_quarter'])['Total_Amount'].sum(). \
            reset_index(name='Amount')

        layout = go.Layout(title='Total transaction volume', xaxis=dict(title='Year-quarter'),
                           yaxis=dict(title='Total_transactions'), width=600, height=500)

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x=transaction['Year_quarter'],
                             y=transaction['Amount'],
                             name='Volume'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(texttemplate='%{y:.2s}')
        st.plotly_chart(fig)


Aggregated_User_Summary['F_State'] = Aggregated_User_Summary['State'].apply(clean_text)
Aggregated_User_Summary['F_State'] = Aggregated_User_Summary['F_State'].str.replace(' Islands', '')

c15, c16 = st.columns(2)

with c15:
    Year = st.selectbox('Year', (2018, 2019, 2020, 2021, 2022), key=7)
with c16:
    Quarter = st.selectbox('Quarter', (1, 2, 3, 4), key=8)

t5, t6 = st.tabs(['Registered Users by state', 'Registered Users by districts'])

with t5:
    c17, c18 = st.columns(2)
    with c17:
        State_users = Aggregated_User_Summary.loc[(Aggregated_User_Summary['Year'] == Year) &
                                                  (Aggregated_User_Summary['Quarter'] == Quarter)].copy()

        State_users.drop(State_users.index[(State_users['F_State'] == 'India')], axis=0, inplace=True)
        State_user_total = State_users.groupby(['Year', 'Quarter', 'F_State'])['Registered_Users'].sum().\
            reset_index(name='Users_count')

        fig_us = px.choropleth(
                            State_user_total,
                            geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                            featureidkey='properties.ST_NM',
                            locations='F_State',
                            color='Users_count',
                            color_continuous_scale='emrld',
                            range_color=[min(State_user_total['Users_count']), max(State_user_total['Users_count'])],
                            color_continuous_midpoint=State_user_total['Users_count'].median(),
                            hover_data={'Users_count': ":,.2s"},
                            height=500,
                            width=700
                            )

        fig_us.update_geos(fitbounds="locations", visible=False)
        fig_us.update_layout(
            title='State User Map',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='mercator'
            ),
            coloraxis_colorbar=dict(
                x=-0.15)
        )
        fig_us.update_layout(coloraxis_colorbar=dict(title='Registered Users'))
        st.plotly_chart(fig_us, use_container_width=False)

    with c18:
        Brand_user = Aggregated_User.loc[(Aggregated_User['Year'] == Year) &
                                         (Aggregated_User['Quarter'] == Quarter)].copy()
        layout = go.Layout(title='Users_count')
        fig = go.Figure(data=[go.Pie(labels=Brand_user['Brand Name'],
                                     values=Brand_user['Registered_Users_Count'], hole=0.5)], layout=layout)
        fig.update_layout(
            autosize=False,
            width=600,
            height=400,
            margin={"r": 0, "t": 60, "l": 0, "b": 0},
            legend=dict(
                orientation="v",
                yanchor="top",
                y=0.95,
                xanchor="right",
                x=2
            )
        )
        st.plotly_chart(fig)
with t6:
    c19, c20 = st.columns(2)
    with c19:
        District_users = User_Table.loc[(User_Table['Year'] == Year) & (User_Table['Quarter'] == Quarter)].copy()
        District_users['F_State'] = District_users['State'].apply(clean_text)
        District_users['F_State'] = District_users['F_State'].str.replace(' Islands', '')

        matched = District_users['Place Name'][District_users['Place Name'].isin(Districts['Place_Name'])]
        Lat = Districts.loc[Districts['Place_Name'].isin(matched), 'Latitude']
        Long = Districts.loc[Districts['Place_Name'].isin(matched), 'Longitude']
        District_users['Latitude'] = Lat.values
        District_users['Longitude'] = Long.values
        District_users['Year_quarter'] = str(Year) + '-Q' + str(Quarter)

        d_sc = px.scatter_geo(
            District_users,
            lon='Longitude',
            lat='Latitude',
            size='Registered Users Count',
            hover_name='Place Name',
            hover_data=['Registered Users Count', 'App Openings']
            )

        d_sc.update_traces(marker=dict(color="red", line_width=1))
        color = '#ABEBC6'
        fig_ds = px.choropleth(
                District_users,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='F_State',
                color='Registered Users Count',
                color_continuous_scale=[[0, color], [1, color]],
                hover_data={"Registered Users Count": ":,.2s", "App Openings": ":,.2s"},
                height=550,
                width=700
                )

        fig_ds.update_geos(fitbounds="locations", visible=False)
        fig_ds.add_trace(d_sc.data[0])
        fig_ds.update_layout(
            title='District User Map',
            geo=dict(
                showframe=False,
                showcoastlines=False,
                projection_type='mercator'
            )
        )
        fig_ds.update_traces(
            hovertemplate=
            "<b>%{hovertext}</b><br>Registered Users Count: %{customdata[0]:,.2s}<br>App Openings: %{customdata[1]:,.2s}"
        )
        fig_ds.update_layout(coloraxis_colorbar=dict(title='Registered Users'))
        st.plotly_chart(fig_ds, use_container_width=False)

    with c20:
        layout = go.Layout(title='Total users per brand', xaxis=dict(title='Brand Name'),
                           yaxis=dict(title='Total_users'), width=600, height=500)
        Users_per_brand = Aggregated_User.groupby('Brand Name')['Registered_Users_Count'].sum().\
            reset_index(name='Total_users')

        fig = go.Figure(layout=layout)
        fig.add_trace(go.Bar(x=Users_per_brand['Brand Name'],
                             y=Users_per_brand['Total_users'],
                             marker=dict(line=dict(width=1)), textposition='outside', name='Users_count'))
        fig.update_xaxes(showgrid=False)
        fig.update_yaxes(showgrid=False)
        fig.update_traces(texttemplate='%{y:.2s}')
        st.plotly_chart(fig)
