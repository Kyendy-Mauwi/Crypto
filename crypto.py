import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import joblib
import numpy as np

# Load cryptocurrency data
@st.cache_data
def load_data():
    data = pd.read_csv('Data/Cryptodata.csv')
    return data

data = load_data()

# Load the trained machine learning model
# model = joblib.load('Data/best_model.pkl')

st.title("Cryptocurrency Data Analysis")

# Sidebar
st.sidebar.title("Cryptocurrency Data Analysis")

# dictionary
coin_name_mapping = {
    'BTC': 'Bitcoin',
    'ETH': 'Ethereum',
    'ADA': 'Cardano',
    'USDt': 'Tether',
    'USDC': 'UCD Coin',
    'SOL': 'Solana',
    'TRX': 'Tron',
    'DOT': 'Polkadot',
    'MATIC': 'Polygon',
    'LTC': 'Litecoin',
    'WBTC': 'Wrapped BTC',
    'SHIB': 'Shiba-inu',
    'BCH': 'BTC Cash',
    'LINK': 'Chainlink',
    'Leo': 'Unus-sed-leo'
}
# list of coin options for user selection
coin_options = list(coin_name_mapping.keys())

# Map coin abbreviations to their full names for user display
coin_options_display = [f"{abbr} - {name}" for abbr, name in coin_name_mapping.items()]

# Display the coin abbreviation key
st.write("## Coin Abbreviation Key")
key_data = {'Abbreviation': coin_name_mapping.keys(), 'Full Name': coin_name_mapping.values()}
key_df = pd.DataFrame(key_data)
st.dataframe(key_df)


# Select feature1
feature1 = st.sidebar.selectbox("Select a cryptocurrency", data['name'].unique())

# Create a filtered dataset based on feature1
filtered_data = data[data['name'] == feature1]

# Main content


# Data Information Section
st.write("## Data Information")
st.write("This app provides insights into cryptocurrency data. You can select a cryptocurrency from the sidebar to explore its trends and statistics.")
st.write(f"Number of Rows: {filtered_data.shape[0]}")
st.write(f"Number of Columns: {filtered_data.shape[1]}")
st.write("Columns:")
st.write(filtered_data.columns.tolist())

# Show dataset description
st.write("## Dataset Description")
st.write(filtered_data.describe())

# Line Chart for Price Over Time
st.write("## Cryptocurrency Price Over Time")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=filtered_data, x='timestamp', y='quote.KES.price')
# x = filtered_data['timestamp'].to_numpy()
# y = filtered_data['quote.KES.price'].to_numpy()
# sns.lineplot(x=x, y=y)
plt.xticks(rotation=90)
plt.xlabel("Date")
plt.ylabel("Price (KES)")
plt.title(f"{feature1} Price Over Time")
st.pyplot(fig)
# # Line Chart for Price Over Time
# st.write("## Cryptocurrency Price Over Time")
# fig, ax = plt.subplots(figsize=(10, 6))
# # Convert 'timestamp' to datetime
# filtered_data['timestamp'] = pd.to_datetime(filtered_data['timestamp'])
# # Sort the data by 'timestamp' to ensure it's in chronological order
# filtered_data = filtered_data.sort_values(by='timestamp')
# # Create the line chart
# sns.lineplot(data=filtered_data, x='timestamp', y='quote.KES.price')
# plt.xticks(rotation=90)
# plt.xlabel("Date")
# plt.ylabel("Price (KES)")
# plt.title(f"{feature1} Price Over Time")
# st.pyplot(fig)

# Histogram for Price Distribution
st.write("## Price Distribution")
# fig, ax = plt.subplots(figsize=(8, 5))
# # sns.histplot(data=filtered_data, x='quote.KES.price', kde=True, color='skyblue')
# sns.histplot(data=np.array(filtered_data['quote.KES.price']), kde=True, color='skyblue')
# plt.xlabel("Price (KES)")
# plt.ylabel("Frequency")
# plt.title(f"{feature1} Price Distribution")
# st.pyplot(fig)
plt.figure(figsize=(8, 5))
plt.hist(filtered_data['quote.KES.price'], bins=30, color='skyblue', alpha=0.7, density=True)
plt.xlabel("Price (KES)")
plt.ylabel("Density")
plt.title(f"{feature1} Price Distribution")
st.pyplot(plt)

# Scatter Plot: Price vs. Market Cap
st.write("## Price vs. Market Cap")
fig, ax = plt.subplots(figsize=(8, 6))
sns.scatterplot(x='quote.KES.market_cap', y='quote.KES.price', data=filtered_data, color='purple', alpha=0.7)
plt.xlabel("Market Cap (KES)")
plt.ylabel("Price (KES)")
plt.title(f"Scatter Plot: {feature1} Price vs. Market Cap")
st.pyplot(fig)

# Bar Chart for Top 10 Cryptocurrencies by Market Cap
st.write("## Top 10 Cryptocurrencies by Market Cap")
top_10_data = data.sort_values(by='quote.KES.market_cap', ascending=False).head(100)
fig = px.bar(top_10_data, x='name', y='quote.KES.market_cap', color='name',
             labels={'quote.KES.market_cap': 'Market Cap (KES)'})
fig.update_layout(xaxis_title='Cryptocurrency', yaxis_title='Market Cap (KES)')
st.plotly_chart(fig)

