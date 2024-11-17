import streamlit as st

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

    Please enter a stock ticker and select the type of analysis to proceed.
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
        # Add your technical analysis code here
    elif analysis_type == "Fundamental Analysis":
        st.subheader(f"Fundamental Analysis for {ticker}")
        st.write("Performing fundamental analysis...")
        # Add your fundamental analysis code here
