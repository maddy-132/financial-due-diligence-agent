import streamlit as st
import yfinance as yf
import pandas as pd

# Page configuration
st.set_page_config(
    page_title="Financial Due Diligence Agent",
    page_icon="📊",
    layout="wide"
)

# Application title
st.title("📊 Financial Due Diligence Agent")
st.write(
    "Analyze company financial information and stock price history."
)

st.warning(
    "This tool provides automated screening indicators, "
    "not a complete financial risk assessment."
)

# User inputs
company = st.text_input(
    "Company Name",
    value="Reliance Industries"
)

ticker = st.text_input(
    "Stock Ticker",
    value="RELIANCE.NS"
)

# Helper function for displaying values
def format_number(value):
    if value is None or pd.isna(value):
        return "N/A"

    return f"{value:,.2f}"


# Analyze button
if st.button("Analyze Company", type="primary"):

    if not company.strip() or not ticker.strip():
        st.warning("Please enter both company name and ticker.")

    else:
        try:
            with st.spinner("Collecting financial data..."):

                stock = yf.Ticker(ticker.strip())
                info = stock.info
                history = stock.history(period="1y")

            # Company analysis
            st.header(f"Analysis: {company.strip()}")

            st.subheader("Financial Overview")

            revenue = info.get("totalRevenue")
            net_income = info.get("netIncomeToCommon")
            market_cap = info.get("marketCap")
            total_debt = info.get("totalDebt")
            total_cash = info.get("totalCash")
            profit_margin = info.get("profitMargins")
            current_ratio = info.get("currentRatio")
            sector = info.get("sector", "N/A")
            industry = info.get("industry", "N/A")

            # Display financial metrics
            col1, col2, col3 = st.columns(3)

            with col1:
                st.metric(
                    "Revenue",
                    format_number(revenue)
                )

            with col2:
                st.metric(
                    "Net Income",
                    format_number(net_income)
                )

            with col3:
                st.metric(
                    "Market Cap",
                    format_number(market_cap)
                )

            col4, col5, col6 = st.columns(3)

            with col4:
                st.metric(
                    "Total Debt",
                    format_number(total_debt)
                )

            with col5:
                st.metric(
                    "Cash",
                    format_number(total_cash)
                )

            with col6:
                margin_text = (
                    f"{profit_margin * 100:.2f}%"
                    if profit_margin is not None
                    and pd.notna(profit_margin)
                    else "N/A"
                )

                st.metric("Profit Margin", margin_text)

            st.subheader("Company Details")

            st.write("*Sector:*", sector)
            st.write("*Industry:*", industry)
            st.write(
                "*Current Ratio:*",
                format_number(current_ratio)
            )

            # Financial details table
            metrics = {
                "Revenue": format_number(revenue),
                "Net Income": format_number(net_income),
                "Market Cap": format_number(market_cap),
                "Total Debt": format_number(total_debt),
                "Cash": format_number(total_cash),
                "Profit Margin": margin_text,
                "Current Ratio": format_number(current_ratio)
            }

            st.subheader("Financial Details")

            financial_table = pd.DataFrame(
                list(metrics.items()),
                columns=["Metric", "Value"]
            )

            st.dataframe(
                financial_table,
                use_container_width="stretch",
                hide_index=True
            )

            # Financial Health Screening Score
            st.subheader("Financial Health Score")

            revenue = info.get("totalRevenue")
            net_income = info.get("netIncomeToCommon")
            profit_margin = info.get("profitMargins")
            current_ratio = info.get("currentRatio")
            total_debt = info.get("totalDebt")
            total_cash = info.get("totalCash")

            score = 0
            available_points = 0

            if profit_margin is not None:
                available_points += 30
                if profit_margin > 0.10:
                    score += 30
                elif profit_margin > 0:
                    score += 20

            if current_ratio is not None:
                available_points += 30
                if current_ratio >= 1.5:
                    score += 30
                elif current_ratio >= 1.0:
                    score += 20
                else:
                    score += 5

            if total_debt is not None and total_cash is not None:
                available_points += 20
                if total_cash >= total_debt:
                    score += 20
                else:
                    score += 10

            if revenue is not None and net_income is not None:
                available_points += 20
                if revenue > 0 and net_income > 0:
                    score += 20

            if available_points > 0:
                health_score = round(
                    score / available_points * 100
                )
                st.metric(
                   "Indicative Health Score",
                    f"{health_score}/100"
                )
                st.progress(health_score / 100)
            else:
                st.warning(
                    "Insufficient financial data to calculate score."
                )
            st.caption(
                "This is a simplified screening score, "
                "not a credit rating or investment recommendation."
            )
            # Company Financial Comparison
            st.subheader("Company Financial Comparison")

            compare_ticker = st.text_input(
                "Enter another company ticker",
                value="TCS.NS"
            )

            if st.button("Compare Companies"):
                if compare_ticker.strip():
                    try:
                        compare_stock = yf.Ticker(
                            compare_ticker.strip()
                        )
                        compare_info = compare_stock.info

                        comparison = pd.DataFrame({
                            "Metric": [
                                "Revenue",
                                "Net Income",
                                "Market Cap"
                            ],
                            company: [
                                info.get("totalRevenue"),
                                info.get("netIncomeToCommon"),
                                info.get("marketCap")
                            ],
                            compare_ticker: [
                                compare_info.get("totalRevenue"),
                                compare_info.get("netIncomeToCommon"),
                                compare_info.get("marketCap")
                            ]
                        })

                        st.dataframe(
                            comparison,
                            width="stretch"
                        )

                    except Exception as error:
                        st.error(
                            f"Comparison failed: {error}"
                        )
                else:
                    st.warning(
                        "Enter a valid stock ticker."
                    )
                    
            st.subheader("Stock Price History (1 Year)")

            if not history.empty and "Close" in history.columns:
                st.line_chart(history["Close"])
            else:
                st.info("Stock price history is unavailable.")

            st.caption(
                "Data availability depends on the selected ticker "
                "and the data provider."
            )

        except Exception as error:
            st.error(f"Unable to retrieve data: {error}")
            st.info(
                "Check your internet connection and ticker symbol."
            )