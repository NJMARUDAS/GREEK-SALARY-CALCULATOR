import streamlit as st
import plotly.graph_objects as go

def calculate_contributions(gross_annual):
    MONTHLY_CAP = 7572.62  # 2025 cap
    ANNUAL_CAP = MONTHLY_CAP * 12
    capped_base = min(gross_annual, ANNUAL_CAP)
    total_contributions = capped_base * 0.1337  # 13.37%
    contributions = {
        'Social Security (13.37%)': total_contributions
    }
    return total_contributions, contributions

def calculate_income_tax(taxable_income, moving_residency=False):
    # Apply 50% exemption if moving residency
    if moving_residency:
        taxable_income_for_tax = taxable_income * 0.5
    else:
        taxable_income_for_tax = taxable_income

    brackets = [
        (10000, 0.09),
        (20000, 0.22),
        (30000, 0.28),
        (40000, 0.36),
        (float('inf'), 0.44)
    ]
    tax = 0
    previous_limit = 0
    for limit, rate in brackets:
        if taxable_income_for_tax > previous_limit:
            amount = min(taxable_income_for_tax, limit) - previous_limit
            tax += amount * rate
            previous_limit = limit
        else:
            break
    return tax, taxable_income_for_tax

st.title('Greek Salary Calculator (12 or 14 Payments)')

gross_annual = st.number_input('Annual Gross Salary (€):', min_value=0.0, step=1000.0)
payment_months = st.selectbox('Number of salary payments per year:', [12, 14], index=1)
moving_residency = st.checkbox(
    'Moving Tax Residency',
    help="50% income tax exemption on Greek-source employment income"
)

if gross_annual > 0:
    # Calculate contributions
    total_contributions, contributions = calculate_contributions(gross_annual)
    taxable_income = gross_annual - total_contributions

    # Calculate taxes
    income_tax, taxable_income_for_tax = calculate_income_tax(taxable_income, moving_residency)
    total_tax = income_tax

    # Net calculations
    net_annual = taxable_income - total_tax
    net_monthly = net_annual / payment_months
    total_contributions_monthly = total_contributions / payment_months

    # --- Summary at the top ---
    st.header("Summary")
    st.write(f"**Gross Annual Salary:** €{gross_annual:,.2f}")
    st.write(f"**Net Annual Salary:** €{net_annual:,.2f}")
    st.write(f"**Net Salary per Payment ({payment_months} payments):** €{net_monthly:,.2f}")

    # --- Taxes section ---
    st.subheader("Tax Details")
    if moving_residency:
        st.write("⚠️ **Tax Residency Mode:** 50% income tax exemption applied")
        st.write(f"**Taxable Income After Exemption:** €{taxable_income_for_tax:,.2f}")
    st.write(f"**Total Income Tax:** annual €{income_tax:,.2f} | per payment €{income_tax/payment_months:,.2f}")

    # --- Social Security section ---
    st.subheader("Social Security Deductions")
    for name, amount in contributions.items():
        st.write(f"- {name}: annual €{amount:,.2f}  |  per payment €{amount/payment_months:,.2f}")
    st.write(f"**Total Social Security:** annual €{total_contributions:,.2f}  |  per payment €{total_contributions_monthly:,.2f}")

    # --- Pie Chart ---
    st.subheader("Income Distribution")
    labels = ['Net Pay', 'Income Tax', 'Social Security']
    values = [net_annual, income_tax, total_contributions]
    if moving_residency:
        labels.insert(1, 'Exempted Income')
        values.insert(1, taxable_income * 0.5)
        colors = ['#4CAF50', '#FFC107', '#F44336', '#2196F3']
    else:
        colors = ['#4CAF50', '#F44336', '#2196F3']

    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        insidetextorientation='auto'
    )])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=350)
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("<hr style='border:1px solid #bbb;'>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:white; font-size:1.5em; margin-top:20px;'>"
    "NJM 2025"
    "</div>",
    unsafe_allow_html=True
)
