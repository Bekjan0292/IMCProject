import streamlit as st
import yfinance as yf
import plotly.graph_objects as go
import pandas as pd

# Define pages as functions
def main_page():
    st.title("Stock Analysis Application")
    st.markdown("""
    Welcome to the Stock Analysis Application! This tool helps you analyze stocks using **technical analysis** and **fundamental analysis**.

    ### What is Technical Analysis?
    - Examines historical price charts, trends, and patterns.
    - Uses tools like moving averages, RSI, and MACD to identify trading opportunities.

    ### What is Fundamental Analysis?
    - Evaluates financial health, earnings, and company metrics.
    - Focuses on valuation, growth prospects, and business fundamentals.

    Enter a stock ticker below and select the type of analysis to proceed.
    """)
    st.divider()
    
    # Input for ticker and analysis type
    ticker = st.text_input("Enter Stock Ticker", "")
    analysis_type = st.selectbox("Select Analysis Type", ["", "Technical Analysis", "Fundamental Analysis"])
    go_button = st.button("Go")

    if go_button:
        if not ticker or not analysis_type:
            st.warning("Please enter a stock ticker and select an analysis type.")
        else:
            perform_analysis(ticker, analysis_type)

def perform_analysis(ticker, analysis_type):
    if analysis_type == "Technical Analysis":
        st.subheader(f"Technical Analysis for {ticker}")
        st.write("Performing technical analysis...")
        # Add your technical analysis logic here
    elif analysis_type == "Fundamental Analysis":
        st.subheader(f"Fundamental Analysis for {ticker}")
        stock = yf.Ticker(ticker)
        info = stock.info
        historical = stock.history(period="1y")

        # Company Information
        st.title(f"{info.get('longName', ticker.upper())}")
        with st.expander("About the Company"):
            st.write(info.get("longBusinessSummary", "Company information is not available."))

        st.write(f"**Industry:** {info.get('industry', 'N/A')}")
        st.write(f"**Country:** {info.get('country', 'N/A')}")
        st.markdown(f"[**Website**]({info.get('website', 'N/A')})", unsafe_allow_html=True)

        # Candlestick Chart
        fig = go.Figure()
        fig.add_trace(
            go.Candlestick(
                x=historical.index,
                open=historical['Open'],
                high=historical['High'],
                low=historical['Low'],
                close=historical['Close']
            )
        )
        fig.update_layout(
            xaxis_title="Date",
            yaxis_title="Price (USD)",
            template="plotly_white"
        )
        st.plotly_chart(fig)

        # Key Statistics
        st.subheader("Key Statistics")
        stats_data = [
            ["Current Price", f"${info.get('currentPrice', 'N/A'):.2f}"],
            ["Market Cap", f"${info.get('marketCap', 'N/A') / 1e9:.2f}B"],
            ["52W Range", f"{info.get('fiftyTwoWeekLow', 'N/A'):.2f} - {info.get('fiftyTwoWeekHigh', 'N/A'):.2f}"],
            ["Beta", f"{info.get('beta', 'N/A'):.2f}"],
            ["P/E Ratio", f"{info.get('trailingPE', 'N/A'):.2f}" if info.get("trailingPE") else "N/A"],
        ]
        stats_df = pd.DataFrame(stats_data, columns=["Metric", "Value"])
        st.table(stats_df)

        # Balance Sheet and Income Statement
        if st.button("View Income Statement"):
            st.write("Income statement logic goes here (extract from provided code).")
        if st.button("View Balance Sheet"):
            st.write("Balance sheet logic goes here (extract from provided code).")

        # Recommendation
        st.subheader("Recommendation")
        recommendations = [
            ["Metric", "Current Value", "Recommendation"],
            ["P/E Ratio", info.get('trailingPE', "N/A"), "Buy" if info.get('trailingPE', 0) < 15 else "Hold"]
        ]
        st.table(pd.DataFrame(recommendations, columns=["Metric", "Value", "Recommendation"]))

def glossary_page():
    st.title("Glossary of Terms")
    st.markdown("""
    ### Key Terms for Stock Analysis
    - **EPS (Earnings Per Share)**: Indicates a company's profitability.
    - **P/E Ratio (Price-to-Earnings)**: Shows the relationship between a company's stock price and its earnings.
    - **RSI (Relative Strength Index)**: A momentum indicator used in technical analysis.
    - **MACD (Moving Average Convergence Divergence)**: Used to identify trends and reversals.
    - Add more terms here as needed.
    """)

def news_page():
    st.title("Market News")
    st.markdown("""
    ### Latest Stock Market News
    Placeholder for news integration. Use APIs like Yahoo Finance, Google News, or others to display relevant stock news.
    """)
    # Add news-fetching logic here

def about_page():
    st.title("About")
    st.markdown("""
    ### About This Application
    This Stock Analysis Application was developed to simplify stock research and help you make informed investment decisions.
    """)

# Navigation
st.sidebar.title("Navigation")
pages = {
    "Main Page": main_page,
    "Glossary": glossary_page,
    "News": news_page,
    "About": about_page
}

selected_page = st.sidebar.radio("Go to", list(pages.keys()))

# Display the selected page
pages[selected_page]()
