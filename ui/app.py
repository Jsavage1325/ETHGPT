import streamlit as st
import requests
import pandas as pd


# Get your API key from CoinMarketCap and replace 'your_api_key' with it.
def get_data():
    url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest"
    headers = {
        "Accepts": "application/json",
        "X-CMC_PRO_API_KEY": "02ad7da5-f491-4b24-a32c-384ca799186b",
    }

    # Send a request to the CoinMarketCap API.
    response = requests.get(url, headers=headers)
    return response.json()


data = get_data()

# Extract the top 10 cryptocurrencies and their information.
top_10_cryptos = []
for crypto in data["data"][:10]:
    crypto_name = crypto["name"]
    crypto_symbol = crypto["symbol"]
    crypto_rank = crypto["cmc_rank"]
    crypto_price = crypto["quote"]["USD"]["price"]
    crypto_market_cap = crypto["quote"]["USD"]["market_cap"]
    crypto_volume_24h = crypto["quote"]["USD"]["volume_24h"]

    top_10_cryptos.append(
        (
            crypto_name,
            crypto_symbol,
            crypto_rank,
            crypto_price,
            crypto_market_cap,
            crypto_volume_24h,
        )
    )

# Convert the data to a pandas DataFrame.
df = pd.DataFrame(
    top_10_cryptos,
    columns=["Crypto", "Symbol", "Rank", "Price", "Market Cap", "24h Volume"],
)

# Format the numeric values for better readability.
df["Price"] = df["Price"].apply(lambda x: f"${x:,.2f}")
df["Market Cap"] = df["Market Cap"].apply(lambda x: f"${x:,.2f}")
df["24h Volume"] = df["24h Volume"].apply(lambda x: f"${x:,.2f}")

# Use Streamlit to create the app.
st.title("Some info about crypto!")
st.write(df)
