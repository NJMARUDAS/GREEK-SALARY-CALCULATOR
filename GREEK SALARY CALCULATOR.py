import streamlit as st
import plotly.graph_objects as go

# Language dictionaries
labels = {
    'en': {
        'flag': '🇬🇧',
        'title': 'Greek Salary Calculator (12 or 14 Payments)',
        'gross_annual': 'Annual Gross Salary (€):',
        'payments': 'Number of salary payments per year:',
        'moving_residency': 'Moving Tax Residency',
        'moving_help': "50% income tax exemption on Greek-source employment income",
        'summary': 'Summary',
        'gross': 'Gross Annual Salary',
        'net_annual': 'Net Annual Salary',
        'net_monthly': 'Net Salary per Payment',
        'tax_details': 'Tax Details',
        'tax_mode': '⚠️ Tax Residency Mode: 50% income tax exemption applied',
        'taxable_after_exemption': 'Taxable Income After Exemption',
        'income_tax': 'Total Income Tax',
        'social_security': 'Social Security Deduction',
        'total_social_security': 'Total Social Security',
        'income_distribution': 'Income Distribution',
        'net_pay': 'Net Pay',
        'income_tax_label': 'Income Tax',
        'social_security_label': 'Social Security',
        'exempted_income': 'Exempted Income',
        'footer': 'NJM 2025',
        'annual': 'annual',
        'per_payment': 'per payment'
    },
    'el': {
        'flag': '🇬🇷',
        'title': 'Υπολογιστής Μισθού Ελλάδας (12 ή 14 Πληρωμές)',
        'gross_annual': 'Ετήσιος Μικτός Μισθός (€):',
        'payments': 'Αριθμός πληρωμών ανά έτος:',
        'moving_residency': 'Μεταφορά Φορολογικής Κατοικίας',
        'moving_help': "Απαλλαγή 50% από το φόρο εισοδήματος για εισόδημα από εργασία στην Ελλάδα",
        'summary': 'Σύνοψη',
        'gross': 'Ετήσιος Μικτός Μισθός',
        'net_annual': 'Ετήσιος Καθαρός Μισθός',
        'net_monthly': 'Καθαρός Μισθός ανά Πληρωμή',
        'tax_details': 'Λεπτομέρειες Φορολογίας',
        'tax_mode': '⚠️ Καθεστώς Φορολογικής Κατοικίας: Εφαρμόστηκε απαλλαγή 50% από το φόρο εισοδήματος',
        'taxable_after_exemption': 'Φορολογητέο Εισόδημα μετά την Απαλλαγή',
        'income_tax': 'Συνολικός Φόρος Εισοδήματος',
        'social_security': 'Κρατήσεις Κοινωνικής Ασφάλισης',
        'total_social_security': 'Συνολικές Κρατήσεις Κοινωνικής Ασφάλισης',
        'income_distribution': 'Κατανομή Εισοδήματος',
        'net_pay': 'Καθαρές Αποδοχές',
        'income_tax_label': 'Φόρος Εισοδήματος',
        'social_security_label': 'Κοινωνική Ασφάλιση',
        'exempted_income': 'Απαλλασσόμενο Εισόδημα',
        'footer': 'NJM 2025',
        'annual': 'ετησίως',
        'per_payment': 'ανά πληρωμή'
    }
}

# Language selector with Greek as default
lang = st.radio(
    "Language / Γλώσσα",
    options=['el', 'en'],
    index=0,  # Greek is default
    format_func=lambda x: f"{labels[x]['flag']} {x.upper()}"
)
L = labels[lang]

def calculate_contributions(gross_annual):
    MONTHLY_CAP = 7572.62  # 2025 cap
    ANNUAL_CAP = MONTHLY_CAP * 12
    capped_base = min(gross_annual, ANNUAL_CAP)
    total_contributions = capped_base * 0.1337  # 13.37%
    contributions = {
        L['social_security_label'] + " (13.37%)": total_contributions
    }
    return total_contributions, contributions

def calculate_income_tax(taxable_income, moving_residency=False):
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

st.title(L['title'])

gross_annual = st.number_input(L['gross_annual'], min_value=0.0, step=1000.0)
payment_months = st.selectbox(L['payments'], [12, 14], index=1)
moving_residency = st.checkbox(
    L['moving_residency'],
    help=L['moving_help']
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
    st.header(L['summary'])
    st.write(f"**{L['gross']}:** €{gross_annual:,.2f}")
    st.write(f"**{L['net_annual']}:** €{net_annual:,.2f}")
    st.write(f"**{L['net_monthly']} ({payment_months}):** €{net_monthly:,.2f}")

    # --- Taxes section ---
    st.subheader(L['tax_details'])
    if moving_residency:
        st.write(f"{L['tax_mode']}")
        st.write(f"**{L['taxable_after_exemption']}:** €{taxable_income_for_tax:,.2f}")
    st.write(f"**{L['income_tax']}:** {L['annual']} €{income_tax:,.2f} | {L['per_payment']} €{income_tax/payment_months:,.2f}")

    # --- Social Security section ---
    st.subheader(L['social_security'])
    st.write(f"**{L['total_social_security']}:** {L['annual']} €{total_contributions:,.2f} | {L['per_payment']} €{total_contributions_monthly:,.2f}")

    # --- Pie Chart ---
    st.subheader(L['income_distribution'])
    labels_pie = [L['net_pay'], L['income_tax_label'], L['social_security_label']]
    values = [net_annual, income_tax, total_contributions]
    if moving_residency:
        labels_pie.insert(1, L['exempted_income'])
        values.insert(1, taxable_income * 0.5)
        colors = ['#4CAF50', '#FFC107', '#F44336', '#2196F3']
    else:
        colors = ['#4CAF50', '#F44336', '#2196F3']

    fig = go.Figure(data=[go.Pie(
        labels=labels_pie,
        values=values,
        marker=dict(colors=colors),
        textinfo='label+percent',
        textposition='outside',  # Labels outside the pie for readability
        insidetextorientation='auto',
        textfont_size=16
    )])
    fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=420)
    st.plotly_chart(fig, use_container_width=True)

# --- Footer ---
st.markdown("<hr style='border:1px solid #bbb;'>", unsafe_allow_html=True)
st.markdown(
    f"<div style='text-align:center; color:white; font-size:1.5em; margin-top:20px;'>{L['footer']}</div>",
    unsafe_allow_html=True
)
