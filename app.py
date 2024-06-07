import streamlit as st
import pandas as pd
import numpy as np
import streamlit_shadcn_ui as ui
from local_components import card_container

st.set_page_config(layout="wide")

st.sidebar.header("")

with st.sidebar.expander("Fractional Mandates"):
    num_mandates = st.number_input('Number of Mandates', min_value=1, value=3, step=1)
    hours_per_mandate = st.number_input('Average Hours Per Mandate', min_value=1, value=20, step=1)
    avg_hourly_rate = st.number_input('Average Hourly Rate', value=200, step=10)

with st.sidebar.expander("Referrals"):
    num_referrals_per_quarter = st.number_input('Number of Active Referrals per Quarter', min_value=1, value=3, step=1)
    avg_referral_value = st.number_input('Average Referral Contract Value', value=6500, step=500)
    referral_commission = st.number_input('Referral Commission (%)', value=6, step=1)

hours_worked = num_mandates * hours_per_mandate
net_income = hours_worked * avg_hourly_rate

# Calculate cumulative referrals per quarter
referrals_per_month = np.zeros(36)
for i in range(36):
    quarter = (i // 3)
    referrals_per_month[i] = quarter * num_referrals_per_quarter

referral_income = referrals_per_month * avg_referral_value * (referral_commission / 100)

total_income = net_income + referral_income[-1]  # Total income for the last month
effective_hourly_rate = total_income / hours_worked
annualized_revenue = total_income * 12  # Annualized revenue
annualized_referral_revenue = referral_income[-1] * 12  # Annualized referral revenue

# Calculate the percentage of revenue from referrals on an annual basis
percentage_annual_referral_revenue = (annualized_referral_revenue / annualized_revenue) * 100

st.title("Origination Credit Estimator :money_with_wings:")
st.write("This app is designed to estimate potential earnings for Goodlawyer's through FGC referrals.")

st.markdown("---")

cols1 = st.columns(3)
with cols1[0]:
    ui.metric_card(title="Total Compensation", content=f"${annualized_revenue:,.0f}", key="card0")
with cols1[1]:
    ui.metric_card(title="Annualized Origination Revenue", content=f"${annualized_referral_revenue:,.0f}", key="card9")
with cols1[2]:
    ui.metric_card(title="Origination Revenue (%)", content=f"{percentage_annual_referral_revenue:.2f}%", key="card10")

cols2 = st.columns(4)
with cols2[0]:
    ui.metric_card(title="Hours Worked", content=f"{hours_worked}", key="card1")
with cols2[1]:
    ui.metric_card(title="Monthly Earned Income", content=f"${net_income:,.0f}", key="card2")
with cols2[2]:
    ui.metric_card(title="Monthly Origination Income", content=f"${referral_income[-1]:,.0f}", key="card3")  # Last month's referral income
with cols2[3]:
    ui.metric_card(title="Effective Hourly", content=f"${effective_hourly_rate:,.0f}", key="card4")

# Create a stacked bar graph
dates = pd.date_range(start='1/1/2022', periods=36, freq='M')
months = dates.strftime('%m/%y')  # Convert dates to "MM/YY" format
mandate_income = np.full((36,), net_income)

df = pd.DataFrame({
    'Month': months,
    'Mandate Income': mandate_income,
    'Referral Income': referral_income
})

df['Month'] = pd.to_datetime(df['Month'], format='%m/%y')
df.sort_values('Month', inplace=True)
df.set_index('Month', inplace=True)

with card_container(key="chart1"):
    st.area_chart(df, use_container_width=True)
