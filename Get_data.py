import os
from os import walk
from pathlib import Path
import pandas as pd
import warnings
from sqlalchemy import create_engine
warnings.filterwarnings('ignore', category=DeprecationWarning)

# Aggregated_transaction_data = pd.DataFrame({})
#
#
# def transaction(state, year, quarter, path):
#     global Aggregated_transaction_data
#     df = pd.read_json(path)
#     data = df['data']['transactionData']
#     for i in data:
#         rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Payment Mode': i['name'],
#                 'Total Transactions': i['paymentInstruments'][0]['count'],
#                 'Total Amount': i['paymentInstruments'][0]['amount']}
#         Aggregated_transaction_data = Aggregated_transaction_data.append(rows, ignore_index=True)
#
#
# tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\aggregated\transaction\country\india\state'
# state_n = os.listdir(tr_state)
# for states in state_n:
#     s = os.path.join(tr_state, states)  # tr_state+'\\'+states
#     year_n = os.listdir(s)
#     for years in year_n:
#         y = os.path.join(s, years)  # s+'\\'+years
#         file = []
#         for paths, dirs, files in walk(y):
#             file.extend(files)
#             break
#         for q in file:
#             p = os.path.join(y, q)  # y+'\\'+q
#             quarter_n = Path(p).stem
#             transaction(states, years, quarter_n, p)
# # Aggregated_transaction_data.to_csv('Aggregated_Transaction_Table.csv', index=False)
# print(len(Aggregated_transaction_data))
# print(Aggregated_transaction_data.head())
#
#
# Aggregated_user_data = pd.DataFrame({})
# Aggregated_brands_data = pd.DataFrame({})
#
#
# def users(state, year, quarter, path):
#     global Aggregated_user_data
#     global Aggregated_brands_data
#     df = pd.read_json(path)
#     ru = df['data']['aggregated']['registeredUsers']
#     ap = df['data']['aggregated']['appOpens']
#     row = {'State': state, 'Year': year, 'Quarter': quarter, 'Registered_Users': ru, 'AppOpenings': ap}
#     Aggregated_user_data = Aggregated_user_data.append(row, ignore_index=True)
#
#     ubd = df['data']['usersByDevice']
#     if ubd:
#         for j in ubd:
#             rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Brand Name': j['brand'],
#                     'Users count': j['count'], 'Percentage share of Brand': j['percentage']}
#             Aggregated_brands_data = Aggregated_brands_data.append(rows, ignore_index=True)
#
#
# tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\aggregated\user\country\india\state'
# state_n = os.listdir(tr_state)
#
# for states in state_n:
#     s = os.path.join(tr_state, states)  # tr_state+'\\'+states
#     year_n = os.listdir(s)
#     for years in year_n:
#         y = os.path.join(s, years)  # s+'\\'+years
#         file = []
#         for paths, dirs, files in walk(y):
#             file.extend(files)
#             break
#         for q in file:
#             p = os.path.join(y, q)  # y+'\\'+q
#             quarter_n = Path(p).stem
#             users(states, years, quarter_n, p)
# Aggregated_user_data.to_csv('Aggregated_User_Table.csv', index=False)
# print(len(Aggregated_user_data))
# print(Aggregated_user_data.head())
#
# Aggregated_brands_data.to_csv('Aggregated_Brands_Table.csv', index=False)
# print(len(Aggregated_brands_data))
# print(Aggregated_brands_data.head())


# Map_transaction_data = pd.DataFrame({})
#
#
# def tmap(state, year, quarter, path):
#     global Map_transaction_data
#     df = pd.read_json(path)
#     hd = df['data']['hoverDataList']
#     for i in hd:
#         rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Place Name': i['name'],
#                 'Total Transactions count': i['metric'][0]['count'], 'Total Amount': i['metric'][0]['amount']}
#         Map_transaction_data = Map_transaction_data.append(rows, ignore_index=True)
#
#
# tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\map\transaction\hover\country\india\state'
# state_n = os.listdir(tr_state)
# for states in state_n:
#     s = os.path.join(tr_state, states)  # tr_state+'\\'+states
#     year_n = os.listdir(s)
#     for years in year_n:
#         y = os.path.join(s, years)  # s+'\\'+years
#         file = []
#         for paths, dirs, files in walk(y):
#             file.extend(files)
#             break
#         for q in file:
#             p = os.path.join(y, q)  # y+'\\'+q
#             quarter_n = Path(p).stem
#             tmap(states, years, quarter_n, p)
# Map_transaction_data.to_csv('Map_transaction_Table.csv', index=False)
# print(len(Map_transaction_data))
# print(Map_transaction_data.head())

# Map_user_data = pd.DataFrame({})
#
#
# def umap(state, year, quarter, path):
#     global Map_user_data
#     df = pd.read_json(path)
#     hd = df['data']['hoverData']
#     for i in hd:
#         rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Place Name': i,
#                 'Registered Users Count': hd[i]['registeredUsers'], 'App Openings': hd[i]['appOpens']}
#
#         Map_user_data = Map_user_data.append(rows, ignore_index=True)
#
#
# tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\map\user\hover\country\india\state'
# state_n = os.listdir(tr_state)
# for states in state_n:
#     s = os.path.join(tr_state, states)  # tr_state+'\\'+states
#     year_n = os.listdir(s)
#     for years in year_n:
#         y = os.path.join(s, years)  # s+'\\'+years
#         file = []
#         for paths, dirs, files in walk(y):
#             file.extend(files)
#             break
#         for q in file:
#             p = os.path.join(y, q)  # y+'\\'+q
#             quarter_n = Path(p).stem
#             umap(states, years, quarter_n, p)
# Map_user_data.to_csv('Map_user_Table.csv', index=False)
# print(len(Map_user_data))
# print(Map_user_data.head())


Top_transaction_districts = pd.DataFrame({})


def ttop(state, year, quarter, path):
    global Top_transaction_districts
    df = pd.read_json(path)
    hd = df['data']['districts']
    for i in hd:
        rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Place Name': i['entityName'],
                'Total Transactions count': i['metric']['count'], 'Total Amount': i['metric']['amount']}
        Top_transaction_districts = Top_transaction_districts.append(rows, ignore_index=True)


tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\top\transaction\country\india\state'
state_n = os.listdir(tr_state)
for states in state_n:
    s = os.path.join(tr_state, states)  # tr_state+'\\'+states
    year_n = os.listdir(s)
    for years in year_n:
        y = os.path.join(s, years)  # s+'\\'+years
        file = []
        for paths, dirs, files in walk(y):
            file.extend(files)
            break
        for q in file:
            p = os.path.join(y, q)  # y+'\\'+q
            quarter_n = Path(p).stem
            ttop(states, years, quarter_n, p)
# Top_transaction_districts.to_csv('Top_transaction_districts_table.csv', index=False)
# print(len(Top_transaction_districts))
# print(Top_transaction_districts.head())
#
#
Top_transaction_areas = pd.DataFrame({})


def ttop(state, year, quarter, path):
    global Top_transaction_areas
    df = pd.read_json(path)
    hd = df['data']['pincodes']
    for i in hd:
        rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Place Name': i['entityName'],
                'Total Transactions count': i['metric']['count'], 'Total Amount': i['metric']['amount']}
        Top_transaction_areas = Top_transaction_areas.append(rows, ignore_index=True)


tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\top\transaction\country\india\state'
state_n = os.listdir(tr_state)
for states in state_n:
    s = os.path.join(tr_state, states)  # tr_state+'\\'+states
    year_n = os.listdir(s)
    for years in year_n:
        y = os.path.join(s, years)  # s+'\\'+years
        file = []
        for paths, dirs, files in walk(y):
            file.extend(files)
            break
        for q in file:
            p = os.path.join(y, q)  # y+'\\'+q
            quarter_n = Path(p).stem
            ttop(states, years, quarter_n, p)
# Top_transaction_areas.to_csv('Top_transaction_areas_table.csv', index=False)
# print(len(Top_transaction_areas))
# print(Top_transaction_areas.head())
#
Top_user_districts = pd.DataFrame({})


def ttop(state, year, quarter, path):
    global Top_user_districts
    df = pd.read_json(path)
    hd = df['data']['districts']
    for i in hd:
        rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Place Name': i['name'],
                'Total Users count': i['registeredUsers']}
        Top_user_districts = Top_user_districts.append(rows, ignore_index=True)


tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\top\user\country\india\state'
state_n = os.listdir(tr_state)
for states in state_n:
    s = os.path.join(tr_state, states)  # tr_state+'\\'+states
    year_n = os.listdir(s)
    for years in year_n:
        y = os.path.join(s, years)  # s+'\\'+years
        file = []
        for paths, dirs, files in walk(y):
            file.extend(files)
            break
        for q in file:
            p = os.path.join(y, q)  # y+'\\'+q
            quarter_n = Path(p).stem
            ttop(states, years, quarter_n, p)
# Top_user_districts.to_csv('Top_user_districts_table.csv', index=False)
# print(len(Top_user_districts))
# print(Top_user_districts.head())
#
#
Top_user_areas = pd.DataFrame({})


def utop(state, year, quarter, path):
    global Top_user_areas
    df = pd.read_json(path)
    hd = df['data']['pincodes']
    for i in hd:
        rows = {'State': state, 'Year': year, 'Quarter': quarter, 'Pincode': i['name'],
                'Total Users count': i['registeredUsers']}
        Top_user_areas = Top_user_areas.append(rows, ignore_index=True)


tr_state = r'C:\Users\Karthikeyan Sridhar\PycharmProjects\Phonepe\pulse\data\top\user\country\india\state'
state_n = os.listdir(tr_state)
for states in state_n:
    s = os.path.join(tr_state, states)  # tr_state+'\\'+states
    year_n = os.listdir(s)
    for years in year_n:
        y = os.path.join(s, years)  # s+'\\'+years
        file = []
        for paths, dirs, files in walk(y):
            file.extend(files)
            break
        for q in file:
            p = os.path.join(y, q)  # y+'\\'+q
            quarter_n = Path(p).stem
            utop(states, years, quarter_n, p)
# Top_user_areas.to_csv('Top_user_areas_table.csv', index=False)
# print(len(Top_user_areas))
# print(Top_user_areas.head())


# Replace the placeholders with your own values
username = 'admin'
password = 'Renga1795'
hostname = 'rds-instances.ckdyhuhypvzi.us-east-1.rds.amazonaws.com'
port = 3306
database_name = 'phonepe'

# Create the connection string
connection_string = f'mysql+pymysql://{username}:{password}@{hostname}:{port}/{database_name}'

# Create the engine object
engine = create_engine(connection_string)
# Aggregated_transaction_data.to_sql(name='Aggregated_transaction_data', con=engine, if_exists='replace', index=False)
# Aggregated_user_data.to_sql(name='Aggregated_user_data', con=engine, if_exists='replace', index=False)
# Aggregated_brands_data.to_sql(name='Aggregated_brands_data', con=engine, if_exists='replace', index=False)
# Map_transaction_data.to_sql(name='Map_transaction_data', con=engine, if_exists='replace', index=False)
# Map_user_data.to_sql(name='Map_user_data', con=engine, if_exists='replace', index=False)
# Top_transaction_districts.to_sql(name='Top_transaction_districts', con=engine, if_exists='replace', index=False)
# Top_transaction_areas.to_sql(name='Top_transaction_areas', con=engine, if_exists='replace', index=False)
Top_user_districts.to_sql(name='Top_user_districts', con=engine, if_exists='replace', index=False)
Top_user_areas.to_sql(name='Top_user_areas', con=engine, if_exists='replace', index=False)

