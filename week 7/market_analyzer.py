import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import sys
import os
from streamlit.web import cli as stcli

DATA_FILE = "producer-prices-nga.csv"

def read_market_data(filename):
    try:
        df = pd.read_csv(filename, skiprows=[1])
        df.rename(columns={
            'Year': 'date',
            'Item': 'commodity',
            'Value': 'price',
            'Unit': 'unit'
        }, inplace=True)
        return df
    except FileNotFoundError:
        return None
    except Exception as e:
        st.error(f"An error occurred while processing the data: {e}")
        st.stop()

def calculate_statistics(data):
    if 'price' in data.columns:
        return data['price'].describe()
    else:
        return pd.DataFrame()

def plot_price_trends(data, commodity_name):
    commodity_data = data[data['commodity'] == commodity_name]
    unit = commodity_data['unit'].iloc[0] if not commodity_data.empty else "Price"

    fig, ax = plt.subplots()
    ax.plot(commodity_data['date'], commodity_data['price'], marker='o', linestyle='-')
    ax.set_title(f"Producer Price Trend for {commodity_name}")
    ax.set_xlabel("Year")
    ax.set_ylabel(f"Price ({unit})")
    st.pyplot(fig)

def main():
    st.title("Nigerian Producer Price Analyzer")
    st.write("This dashboard helps you analyze and visualize annual producer prices for various commodities in Nigeria, based on FAO data.")

    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_path = os.path.join(script_dir, DATA_FILE)

    market_data = read_market_data(data_path)
    if market_data is None:
        st.error(f"Error: The file '{DATA_FILE}' was not found. Please ensure it is in the same directory as the script.")
    else:
        st.sidebar.header("Filters")
        commodities = sorted(market_data['commodity'].unique())
        selected_commodity = st.sidebar.selectbox("Select a Commodity", commodities)

        st.header(f"Analysis for: {selected_commodity}")

        col1, col2 = st.columns([2, 1])

        filtered_data = market_data[market_data['commodity'] == selected_commodity]

        with col1:
            plot_price_trends(filtered_data, selected_commodity)

        with col2:
            st.subheader("Summary Statistics")
            st.write(calculate_statistics(filtered_data))

        st.subheader("Raw Data for " + selected_commodity)
        st.dataframe(filtered_data)

if __name__ == "__main__":
    if st.runtime.exists():
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]
        sys.exit(stcli.main())