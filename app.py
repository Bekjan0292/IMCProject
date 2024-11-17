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

# Recommendation Section
st.subheader("Recommendation")
pe_ratio = info.get("trailingPE", "N/A")
pb_ratio = info.get("priceToBook", "N/A")
de_ratio = info.get("debtToEquity", "N/A")
fcf = info.get("freeCashflow", "N/A")

# Placeholder for industry values (replace with actual data)
industry_pe = 20  # Example value for Industry P/E
industry_pb = 2.5  # Example value for Industry P/B
industry_de = 0.7  # Example value for Industry D/E
industry_fcf = "Positive"  # Example for Industry FCF (replace if numeric)

# Convert free cash flow to millions and format it
fcf_text = f"{(fcf / 1e6):,.2f}M USD" if isinstance(fcf, (int, float)) else "N/A"

# Define recommendations with explanations, pros, and cons
recommendation_data = [
    {
        "Metric": "P/E Ratio",
        "Current Value": f"{pe_ratio:.2f}" if isinstance(pe_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_pe:.2f}" if isinstance(industry_pe, (int, float)) else "N/A",
        "Explanation": "The Price-to-Earnings (P/E) Ratio measures the stock price relative to its earnings. "
                       "A lower P/E indicates better value compared to earnings, but it can vary by industry.",
        "Pros": "Widely used; allows easy comparison with industry averages.",
        "Cons": "May be misleading for low-earning or high-growth companies.",
        "Recommendation": "Buy" if pe_ratio < 15 else "Hold" if 15 <= pe_ratio <= 25 else "Sell"
    },
    {
        "Metric": "P/B Ratio",
        "Current Value": f"{pb_ratio:.2f}" if isinstance(pb_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_pb:.2f}" if isinstance(industry_pb, (int, float)) else "N/A",
        "Explanation": "The Price-to-Book (P/B) Ratio compares the stock price to the book value of the company. "
                       "Useful for determining undervalued or overvalued stocks in asset-heavy industries.",
        "Pros": "Effective for asset-heavy industries like real estate or manufacturing.",
        "Cons": "Less relevant for service-oriented or tech companies.",
        "Recommendation": "Buy" if pb_ratio < 1 else "Hold" if 1 <= pb_ratio <= 3 else "Sell"
    },
    {
        "Metric": "D/E Ratio",
        "Current Value": f"{de_ratio:.2f}" if isinstance(de_ratio, (int, float)) else "N/A",
        "Industry Current Value": f"{industry_de:.2f}" if isinstance(industry_de, (int, float)) else "N/A",
        "Explanation": "The Debt-to-Equity (D/E) Ratio evaluates a company's financial leverage by comparing its total debt "
                       "to shareholders' equity. A lower ratio indicates less financial risk.",
        "Pros": "Highlights the financial stability and leverage of the company.",
        "Cons": "Varies significantly by industry; may not always reflect operational risk.",
        "Recommendation": "Buy" if de_ratio < 0.5 else "Hold" if 0.5 <= de_ratio <= 1 else "Sell"
    },
    {
        "Metric": "Free Cash Flow (FCF)",
        "Current Value": fcf_text,
        "Industry Current Value": industry_fcf,  # Replace if numeric
        "Explanation": "Free Cash Flow (FCF) measures the cash a company generates after accounting for capital expenditures. "
                       "It reflects financial health and ability to fund growth or return value to shareholders.",
        "Pros": "Indicates financial health and growth potential.",
        "Cons": "Can fluctuate significantly year to year, especially in cyclical industries.",
        "Recommendation": "Buy" if isinstance(fcf, (int, float)) and fcf > 0 else "Sell"
    }
]

# Convert to DataFrame and display
recommendation_df = pd.DataFrame(recommendation_data)
st.table(recommendation_df)

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
