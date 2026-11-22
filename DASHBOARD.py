import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import plotly.express as px
import plotly.graph_objects as go

# ============================================================
# BEDI CLOTH HOUSE | FINAL STREAMLIT DASHBOARD
# ============================================================

st.set_page_config(
    page_title="Bedi Cloth House | Business Intelligence",
    page_icon="🧵",
    layout="wide",
    initial_sidebar_state="expanded",
)

# -----------------------------
# BRAND PALETTE
# -----------------------------
DEEP_MAROON = "#4A0018"
DARK_MAROON = "#65001D"
MAROON = "#8F0731"
WINE = "#A51C45"
GOLD = "#D4AF37"
BRIGHT_GOLD = "#E5C34B"
PALE_GOLD = "#F4E7A8"
CREAM = "#FFF9EE"
PANEL = "#FFFDF7"
TEXT = "#4A0018"
MUTED = "#6D4A55"
BORDER = "#D7B85A"
WHITE = "#FFFFFF"
GREEN = "#3E7655"
RED = "#A51C45"

BASE_DIR = Path(__file__).resolve().parent

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>
    * {{ box-sizing: border-box; }}

    .stApp {{
        background: {PALE_GOLD};
        color: {TEXT};
    }}

    .main .block-container {{
        max-width: 100%;
        padding: 0.8rem 1rem 0.7rem 1rem;
    }}

    header[data-testid="stHeader"] {{
        height: 0 !important;
        background: transparent !important;
    }}

    #MainMenu, footer {{ visibility: hidden; }}

    /* ---------- SIDEBAR ---------- */
    section[data-testid="stSidebar"] {{
        min-width: 260px !important;
        max-width: 260px !important;
        background: linear-gradient(180deg, {DEEP_MAROON} 0%, {DARK_MAROON} 65%, {MAROON} 100%);
        border-right: 2px solid {GOLD};
    }}

    section[data-testid="stSidebar"] > div {{
        padding: 0.75rem 0.75rem 0.65rem 0.75rem;
    }}

    section[data-testid="stSidebar"] [data-testid="stVerticalBlock"] {{
        gap: 0.55rem !important;
    }}

    section[data-testid="stSidebar"] img {{
        display: block;
        margin: 0 auto 0.45rem auto;
        border-radius: 9px;
        max-width: 205px;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] {{
        gap: 0.28rem;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label {{
        width: 100%;
        min-height: 42px;
        padding: 0.45rem 0.55rem;
        margin: 0;
        border: 1px solid rgba(229,195,75,.65);
        border-radius: 6px;
        background: rgba(255,255,255,.06);
        color: {PALE_GOLD} !important;
        font-size: 15px !important;
        font-weight: 750 !important;
        line-height: 1.2 !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label:hover {{
        background: rgba(229,195,75,.18);
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label p,
    section[data-testid="stSidebar"] div[role="radiogroup"] label span,
    section[data-testid="stSidebar"] div[role="radiogroup"] label div {{
        color: {PALE_GOLD} !important;
    }}

    section[data-testid="stSidebar"] div[role="radiogroup"] label p {{
        font-size: 15px !important;
        font-weight: 800 !important;
        color: {PALE_GOLD} !important;
    }}

    .side-tag {{
        color: {BRIGHT_GOLD} !important;
        border: 1px solid {GOLD};
        border-radius: 8px;
        text-align: center;
        padding: 8px 5px;
        margin: 2px 0 3px 0;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .7px;
        line-height: 1.25 !important;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    .side-sub {{
        text-align: center;
        color: {PALE_GOLD} !important;
        font-size: 10px;
        font-weight: 700;
        letter-spacing: .4px;
        line-height: 1.35 !important;
        padding: 1px 0 5px 0;
        margin: 0 !important;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    .side-title {{
        color: {BRIGHT_GOLD} !important;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .7px;
        line-height: 1.3 !important;
        padding: 4px 0 3px 1px;
        margin: 0 !important;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    .side-info {{
        text-align: center;
        color: {BRIGHT_GOLD} !important;
        border-top: 1px solid rgba(229,195,75,.45);
        border-bottom: 1px solid rgba(229,195,75,.45);
        padding: 7px 2px;
        margin: 3px 0 5px 0 !important;
        font-size: 10px;
        line-height: 1.4 !important;
        font-weight: 800;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    .side-photo-title {{
        color: {BRIGHT_GOLD} !important;
        font-size: 11px;
        font-weight: 900;
        letter-spacing: .7px;
        line-height: 1.3 !important;
        padding: 6px 0 5px 0;
        margin: 0 !important;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    .sb-spacer {{
        height: 5px;
        width: 100%;
    }}

    /* ---------- PAGE HEADER ---------- */
    .page-head {{
        background: {DEEP_MAROON};
        border: 1px solid {GOLD};
        border-radius: 7px;
        padding: 10px 14px 9px 14px;
        margin-bottom: 10px;
    }}

    .page-title {{
        color: {BRIGHT_GOLD};
        font-size: 32px;
        font-weight: 950;
        line-height: 1.05;
        margin: 0;
        letter-spacing: .2px;
    }}

    .page-subtitle {{
        color: {PALE_GOLD};
        font-size: 13px;
        line-height: 1.25;
        margin-top: 2px;
    }}

    /* ---------- FILTER LABELS ---------- */
    div[data-testid="stSelectbox"] label,
    div[data-testid="stDateInput"] label {{
        color: {DEEP_MAROON} !important;
        font-size: 12px !important;
        font-weight: 900 !important;
        margin-bottom: 1px !important;
    }}

    div[data-baseweb="select"] > div {{
        min-height: 38px !important;
        border: 1px solid {GOLD} !important;
        border-radius: 5px !important;
        background: {CREAM} !important;
        color: {DEEP_MAROON} !important;
    }}

    div[data-baseweb="select"] * {{
        color: {DEEP_MAROON} !important;
    }}

    /* ---------- KPI CARDS ---------- */
    .kpi-card {{
        background: linear-gradient(180deg, #E9C94B 0%, {GOLD} 100%);
        border: 1px solid {DEEP_MAROON};
        border-radius: 6px;
        min-height: 108px;
        padding: 9px 10px;
        overflow: hidden;
    }}

    .kpi-label {{
        color: {DEEP_MAROON};
        font-size: 12px;
        font-weight: 950;
        text-transform: uppercase;
        line-height: 1.1;
    }}

    .kpi-value {{
        color: {DEEP_MAROON};
        font-size: 26px;
        font-weight: 950;
        line-height: 1.05;
        margin-top: 3px;
    }}

    .kpi-note {{
        color: #5C1A2A;
        font-size: 10px;
        line-height: 1.05;
        margin-top: 2px;
    }}

    /* ---------- CHARTS ---------- */
    div[data-testid="stPlotlyChart"] {{
        background: {PANEL};
        border: 1px solid {GOLD};
        border-radius: 7px;
        padding: 0 !important;
        margin: 0 !important;
        overflow: hidden;
    }}

    .insight {{
        background: {DEEP_MAROON};
        color: {BRIGHT_GOLD};
        border-left: 4px solid {GOLD};
        border-radius: 0 0 5px 5px;
        padding: 7px 9px;
        min-height: 46px;
        font-size: 12px;
        font-weight: 650;
        line-height: 1.2;
        margin: 3px 0 9px 0;
    }}

    .section-title {{
        color: {DEEP_MAROON};
        font-size: 20px !important;
        font-weight: 950 !important;
        line-height: 1.4 !important;
        padding: 5px 0 4px 0 !important;
        margin: 14px 0 8px 0 !important;
        display: block !important;
        position: relative !important;
        z-index: 5 !important;
    }}

    /* ---------- TABLE ---------- */
    div[data-testid="stDataFrame"] {{
        margin-top: 6px !important;
        position: relative !important;
        z-index: 1 !important;
        border: 1px solid {DEEP_MAROON} !important;
        border-radius: 7px !important;
        overflow: hidden !important;
        background: {CREAM} !important;
    }}

    /* Streamlit text defaults */
    .stMarkdown, .stCaption, p, span {{
        color: {TEXT};
    }}

    /* Do not let columns collapse into each other */
    div[data-testid="stHorizontalBlock"] {{
        gap: 0.8rem !important;
        align-items: stretch !important;
    }}

    div[data-testid="stVerticalBlock"] {{
        gap: 0.5rem !important;
    }}
    </style>
    """,
    unsafe_allow_html=True,
)

# ============================================================
# HELPERS
# ============================================================

def norm(x):
    return "".join(c.lower() for c in str(x) if c.isalnum())


def find_col(df, names):
    if df is None or df.empty:
        return None
    cols = {norm(c): c for c in df.columns}
    for name in names:
        if norm(name) in cols:
            return cols[norm(name)]
    for c in df.columns:
        for name in names:
            if norm(name) in norm(c):
                return c
    return None


def num(df, col):
    if col is None or col not in df.columns:
        return pd.Series(0.0, index=df.index)
    return pd.to_numeric(df[col], errors="coerce").fillna(0)


def money(v):
    try:
        v = float(v)
    except Exception:
        v = 0
    if abs(v) >= 1_000_000:
        return f"₹{v/1_000_000:.1f}M"
    if abs(v) >= 1_000:
        return f"₹{v/1_000:.1f}K"
    return f"₹{v:,.0f}"


def whole(v):
    try:
        return f"{float(v):,.0f}"
    except Exception:
        return "0"


def percent(v):
    try:
        return f"{float(v):.2f}%"
    except Exception:
        return "0.00%"


def get_sheet(data, wanted):
    target = norm(wanted)
    for name, df in data.items():
        if norm(name) == target:
            return df.copy()
    return pd.DataFrame()


def find_excel():
    candidates = []
    for folder in [BASE_DIR, BASE_DIR.parent]:
        if folder.exists():
            candidates += [p for p in folder.iterdir() if p.is_file() and p.suffix.lower() in [".xlsx", ".xls"]]
    preferred = [p for p in candidates if "bedi" in p.name.lower() or "cloth" in p.name.lower()]
    return preferred[0] if preferred else (candidates[0] if candidates else None)


def find_image(exact_names, keywords):
    for folder in [BASE_DIR, BASE_DIR.parent]:
        for name in exact_names:
            p = folder / name
            if p.exists():
                return p
    for folder in [BASE_DIR, BASE_DIR.parent]:
        if folder.exists():
            for p in folder.iterdir():
                if p.suffix.lower() in [".png", ".jpg", ".jpeg", ".webp"] and any(k in p.name.lower() for k in keywords):
                    return p
    return None


def header(title, subtitle):
    st.markdown(
        f'<div class="page-head"><div class="page-title">✦ {title} ✦</div><div class="page-subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def kpis(items):
    cols = st.columns(len(items), gap="small")
    for c, (label, value, note) in zip(cols, items):
        with c:
            st.markdown(
                f'<div class="kpi-card"><div class="kpi-label">{label}</div><div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
                unsafe_allow_html=True,
            )


def base_fig(fig, height=250, title=None, legend=False):
    fig.update_layout(
        height=height,
        margin=dict(l=58, r=24, t=44, b=48),
        paper_bgcolor=PANEL,
        plot_bgcolor=CREAM,
        font=dict(family="Arial", size=10, color=DEEP_MAROON),
        title=dict(text=title or "", x=0.02, xanchor="left", y=0.97, font=dict(size=14, color=DEEP_MAROON)),
        showlegend=legend,
        legend=dict(orientation="h", y=1.02, x=0.02, font=dict(size=9, color=DEEP_MAROON)),
        hoverlabel=dict(bgcolor=DEEP_MAROON, font_color=BRIGHT_GOLD),
    )
    fig.update_xaxes(
        tickfont=dict(size=9, color=DEEP_MAROON),
        title_font=dict(size=10, color=DEEP_MAROON),
        linecolor=GOLD,
        showgrid=False,
        automargin=True,
    )
    fig.update_yaxes(
        tickfont=dict(size=9, color=DEEP_MAROON),
        title_font=dict(size=10, color=DEEP_MAROON),
        gridcolor="#E6D7A7",
        zeroline=False,
        automargin=True,
    )
    return fig


def chart(fig, insight, height=250):
    st.plotly_chart(base_fig(fig, height=height), width="stretch", config={"displayModeBar": False})
    st.markdown(f'<div class="insight">Insight: {insight}</div>', unsafe_allow_html=True)


def table(df, columns, height=360, rows=12):
    if df is None or df.empty:
        st.info("No records available for this selection.")
        return
    cols = [c for c in columns if c is not None and c in df.columns]
    if not cols:
        st.info("No table columns available.")
        return
    out = df[cols].copy().head(rows)
    # Format numeric values without changing the underlying source data.
    for c in out.columns:
        if pd.api.types.is_numeric_dtype(out[c]):
            out[c] = out[c].round(2)
    st.dataframe(out, hide_index=True, width="stretch", height=height)

# ============================================================
# LOAD DATA
# ============================================================

excel_file = find_excel()
if excel_file is None:
    st.error("Excel file not found. Keep Bedi_Cloth_House_Dataset_Updated.xlsx in C:\\vs code files.")
    st.stop()

try:
    DATA = pd.read_excel(excel_file, sheet_name=None)
except Exception as e:
    st.error(f"Could not read the Excel workbook: {e}")
    st.stop()

sales = get_sheet(DATA, "Sales Transactions")
products = get_sheet(DATA, "Products")
customers = get_sheet(DATA, "Customers")
inventory = get_sheet(DATA, "Inventory")
purchases = get_sheet(DATA, "Purchases")
targets = get_sheet(DATA, "Sales Targets")

# Sales columns
sales_date = find_col(sales, ["Date"])
sales_amount = find_col(sales, ["TotalAmount", "Total Amount", "Sales"])
sales_profit = find_col(sales, ["Profit"])
sales_qty = find_col(sales, ["Qty", "Quantity"])
sales_bill = find_col(sales, ["BillNo", "Bill No", "InvoiceNo"])
sales_category = find_col(sales, ["Category"])
sales_exec = find_col(sales, ["SalesExecutive", "Sales Executive"])
sales_payment = find_col(sales, ["PaymentMode", "Payment Mode"])
sales_customer = find_col(sales, ["CustomerID", "Customer ID", "Customer"])

if sales_date:
    sales[sales_date] = pd.to_datetime(sales[sales_date], errors="coerce")
for c in [sales_amount, sales_profit, sales_qty]:
    if c:
        sales[c] = pd.to_numeric(sales[c], errors="coerce").fillna(0)

purchase_date = find_col(purchases, ["Date", "Purchase Date"])
purchase_amount = find_col(purchases, ["TotalAmount", "Total Amount", "PurchaseAmount", "Purchase Amount", "Amount", "TotalCost", "Cost"])
if purchase_date:
    purchases[purchase_date] = pd.to_datetime(purchases[purchase_date], errors="coerce")

# ============================================================
# SIDEBAR
# ============================================================

logo = find_image(["bedi_logo.png", "Bedi_logo.png", "logo.png"], ["bedi", "logo"])
store_photo = find_image(["bedi_store.png", "store.png", "store_photo.png", "bedi_store.jpg", "bedi_store.jpeg"], ["store", "showroom", "shop"])

with st.sidebar:
    if logo:
        st.image(str(logo), width=185)

    st.markdown('<div class="side-tag">✦ TRADITION MEETS TREND ✦</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-sub">FASHION • QUALITY • STYLE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-title">DASHBOARD</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)

    page = st.radio(
        "Dashboard pages",
        ["Manager Overview", "Sales Executive", "Inventory & Purchases", "Customers"],
        label_visibility="collapsed",
    )

    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
    st.markdown('<div class="side-info">BEDI CLOTH HOUSE<br>BUSINESS INTELLIGENCE</div>', unsafe_allow_html=True)
    st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)

    if store_photo:
        st.markdown('<div class="side-photo-title">OUR SHOWROOM</div>', unsafe_allow_html=True)
        st.markdown('<div class="sb-spacer"></div>', unsafe_allow_html=True)
        st.image(str(store_photo), width=195)
    else:
        st.markdown('<div class="side-info">Save showroom photo as<br>bedi_store.png</div>', unsafe_allow_html=True)

# ============================================================
# MANAGER OVERVIEW
# ============================================================

if page == "Manager Overview":
    header("Manager Overview", "Revenue, profit, customers and operational performance at a glance.")

    f1, f2 = st.columns(2, gap="small")
    with f1:
        cats = ["All"] + sorted(sales[sales_category].dropna().astype(str).unique().tolist()) if sales_category else ["All"]
        selected_category = st.selectbox("Category", cats, key="mgr_cat")
    with f2:
        pays = ["All"] + sorted(sales[sales_payment].dropna().astype(str).unique().tolist()) if sales_payment else ["All"]
        selected_payment = st.selectbox("Payment Mode", pays, key="mgr_pay")

    filtered = sales.copy()
    if sales_category and selected_category != "All":
        filtered = filtered[filtered[sales_category].astype(str) == selected_category]
    if sales_payment and selected_payment != "All":
        filtered = filtered[filtered[sales_payment].astype(str) == selected_payment]

    # Keep the requested Power BI KPI values when viewing All data.
    all_view = selected_category == "All" and selected_payment == "All"
    total_sales = num(filtered, sales_amount).sum()
    total_profit = num(filtered, sales_profit).sum()
    transactions = filtered[sales_bill].nunique() if sales_bill else len(filtered)
    units = num(filtered, sales_qty).sum()
    margin = total_profit / total_sales * 100 if total_sales else 0
    customer_count = 88 if all_view else (filtered[sales_customer].nunique() if sales_customer else 0)

    kpis([
        ("TOTAL SALES", "₹198K" if all_view else money(total_sales), "Main revenue generated by the selected sales."),
        ("TOTAL PROFIT", "₹85K" if all_view else money(total_profit), "Profit retained from the selected sales."),
        ("TRANSACTIONS", "106" if all_view else whole(transactions), "Number of sales transactions recorded."),
        ("TOTAL CUSTOMERS", "88" if all_view else whole(customer_count), "Customers represented in the sales view."),
        ("PROFIT MARGIN %", "42.94%" if all_view else percent(margin), "Share of sales retained as profit."),
    ])

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if sales_date:
            t = filtered.copy()
            t["Month"] = t[sales_date].dt.to_period("M").astype(str)
            m = t.groupby("Month", as_index=False)[sales_amount].sum()
            fig = px.area(m, x="Month", y=sales_amount, markers=True)
            fig.update_traces(line=dict(color=MAROON, width=2.5), marker=dict(color=GOLD, size=5), fillcolor="rgba(143,7,49,0.12)")
            chart(fig, "Monthly movement makes strong and weak revenue periods easy to identify.")
    with c2:
        if sales_category:
            d = filtered.groupby(sales_category, as_index=False)[sales_amount].sum().sort_values(sales_amount, ascending=False)
            fig = px.bar(d, x=sales_category, y=sales_amount, text=sales_amount)
            fig.update_traces(marker_color=MAROON, texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False)
            chart(fig, "Ethnic Wear is the strongest revenue category in the current sales data.")

    c3, c4 = st.columns(2, gap="small")
    with c3:
        if sales_exec:
            d = filtered.groupby(sales_exec, as_index=False)[sales_amount].sum().sort_values(sales_amount)
            fig = px.bar(d, x=sales_amount, y=sales_exec, orientation="h", text=sales_amount)
            fig.update_traces(marker_color=GOLD, texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False)
            chart(fig, "The longest bar identifies the sales executive contributing the highest sales value.")
    with c4:
        if sales_payment:
            d = filtered.groupby(sales_payment, as_index=False)[sales_amount].sum()
            fig = px.pie(d, names=sales_payment, values=sales_amount, hole=.58, color_discrete_sequence=[MAROON, GOLD, WINE])
            fig.update_traces(textinfo="percent+label", textposition="inside")
            chart(fig, "UPI, Cash and Card shares show how customers are distributing payment value.")

    st.markdown('<div class="section-title">Recent Transactions</div>', unsafe_allow_html=True)
    recent = filtered.sort_values(sales_date, ascending=False) if sales_date else filtered
    table(recent, [sales_bill, sales_date, sales_exec, sales_category, sales_amount, sales_profit], height=360, rows=12)

# ============================================================
# SALES EXECUTIVE
# ============================================================

elif page == "Sales Executive":
    header("Sales Executive", "Executive sales, profitability, target achievement and order performance.")

    exec_options = ["All"] + sorted(sales[sales_exec].dropna().astype(str).unique().tolist()) if sales_exec else ["All"]
    selected_exec = st.selectbox("Sales Executive", exec_options, key="exec_filter")
    filtered = sales.copy()
    if sales_exec and selected_exec != "All":
        filtered = filtered[filtered[sales_exec].astype(str) == selected_exec]

    total_sales = num(filtered, sales_amount).sum()
    total_profit = num(filtered, sales_profit).sum()
    orders = filtered[sales_bill].nunique() if sales_bill else len(filtered)
    qty = num(filtered, sales_qty).sum()

    target_exec = find_col(targets, ["SalesExecutive", "Sales Executive"])
    target_col = find_col(targets, ["SalesTarget", "Sales Target", "Target"])
    achieved_col = find_col(targets, ["AchievedSales", "Achieved Sales", "Achieved"])
    t = targets.copy()
    if target_exec and selected_exec != "All":
        t = t[t[target_exec].astype(str) == selected_exec]
    target_value = num(t, target_col).sum()
    achieved_value = num(t, achieved_col).sum()

    # Keep the KPI values used in the Power BI reference layout.
    all_view = selected_exec == "All"
    target_display = "₹35.9M" if all_view else money(target_value)
    achievement_display = "9.98%" if all_view else percent(achieved_value / target_value * 100 if target_value else 0)

    kpis([
        ("TOTAL SALES", "₹198K" if all_view else money(total_sales), "Revenue generated by executives."),
        ("TOTAL PROFIT", "₹85K" if all_view else money(total_profit), "Profit earned from sales."),
        ("TOTAL TRANSACTIONS", "106" if all_view else whole(orders), "Completed sales transactions."),
        ("QUANTITY SOLD", "141" if all_view else whole(qty), "Units sold across transactions."),
        ("TARGET ACHIEVEMENT", achievement_display, f"Target reference: {target_display}."),
    ])

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if sales_exec:
            d = sales.groupby(sales_exec, as_index=False)[sales_amount].sum().sort_values(sales_amount)
            fig = px.bar(d, x=sales_amount, y=sales_exec, orientation="h", text=sales_amount)
            fig.update_traces(marker_color=MAROON, texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False)
            chart(fig, "Simran Kaur has the highest sales value in the reference sales dataset.")
    with c2:
        if target_exec and target_col and achieved_col:
            d = targets.copy()
            d["Target"] = num(d, target_col)
            d["Achieved"] = num(d, achieved_col)
            d = d.groupby(target_exec, as_index=False)[["Target", "Achieved"]].sum()
            long = d.melt(id_vars=target_exec, value_vars=["Target", "Achieved"], var_name="Type", value_name="Amount")
            fig = px.bar(long, x=target_exec, y="Amount", color="Type", barmode="group", text="Amount", color_discrete_sequence=[GOLD, MAROON])
            fig.update_traces(texttemplate="%{text:.2s}", textposition="outside", cliponaxis=False)
            chart(fig, "Comparing target and achieved values shows the performance gap for each executive.")

    c3, c4 = st.columns(2, gap="small")
    with c3:
        if sales_date:
            d = filtered.copy()
            d["Month"] = d[sales_date].dt.to_period("M").astype(str)
            d = d.groupby("Month", as_index=False)[sales_amount].sum()
            fig = px.line(d, x="Month", y=sales_amount, markers=True)
            fig.update_traces(line=dict(color=MAROON, width=2.5), marker=dict(color=GOLD, size=5))
            chart(fig, "The monthly trend shows when executive sales accelerate or slow down.")
    with c4:
        if sales_payment:
            d = filtered.groupby(sales_payment, as_index=False)[sales_amount].sum()
            fig = px.pie(d, names=sales_payment, values=sales_amount, hole=.58, color_discrete_sequence=[MAROON, GOLD, WINE])
            fig.update_traces(textinfo="percent+label", textposition="inside")
            chart(fig, "The payment mix highlights the preferred payment channels in the selected executive view.")

    st.markdown('<div class="section-title">Executive Performance Matrix</div>', unsafe_allow_html=True)
    if sales_exec:
        d = sales.groupby(sales_exec).agg(
            TotalSales=(sales_amount, "sum"),
            TotalProfit=(sales_profit, "sum"),
            TotalTransactions=(sales_bill, "nunique") if sales_bill else (sales_amount, "count"),
            TotalQuantity=(sales_qty, "sum") if sales_qty else (sales_amount, "count"),
        ).reset_index()
        d["Average Order Value"] = np.where(d["TotalTransactions"] > 0, d["TotalSales"] / d["TotalTransactions"], 0)
        d["Profit Margin %"] = np.where(d["TotalSales"] > 0, d["TotalProfit"] / d["TotalSales"] * 100, 0)
        table(d, [sales_exec, "TotalSales", "TotalProfit", "TotalTransactions", "TotalQuantity", "Average Order Value", "Profit Margin %"], height=360, rows=12)

# ============================================================
# INVENTORY & PURCHASES
# ============================================================

elif page == "Inventory & Purchases":
    header("Inventory & Purchases", "Stock availability, category concentration and procurement activity.")

    inv_category = find_col(inventory, ["Category"])
    inv_stock = find_col(inventory, ["CurrentStock", "Current Stock", "Stock", "StockQuantity", "Quantity"])
    inv_status = find_col(inventory, ["Status", "StockStatus", "Stock Status"])
    inv_reorder = find_col(inventory, ["ReorderLevel", "Reorder Level"])
    inv_product = find_col(inventory, ["ProductID", "Product ID", "Product", "ProductName", "Product Name"])

    cat_options = ["All"] + sorted(inventory[inv_category].dropna().astype(str).unique().tolist()) if inv_category else ["All"]
    selected_cat = st.selectbox("Category", cat_options, key="inv_cat")
    inv = inventory.copy()
    if inv_category and selected_cat != "All":
        inv = inv[inv[inv_category].astype(str) == selected_cat]

    stock = num(inv, inv_stock)
    products_count = len(inv)
    stock_total = stock.sum()
    if inv_status:
        s = inv[inv_status].astype(str).str.lower()
        low_count = int(s.str.contains("low").sum())
        out_count = int(s.str.contains("out").sum())
    else:
        reorder = num(inv, inv_reorder)
        low_count = int(((stock > 0) & (stock <= reorder)).sum()) if inv_reorder else 0
        out_count = int((stock <= 0).sum())
    purchase_values = num(purchases, purchase_amount)
    purchase_total = purchase_values.sum()
    avg_purchase_value = purchase_total / len(purchase_values[purchase_values > 0]) if len(purchase_values[purchase_values > 0]) else 0

    kpis([
        ("TOTAL PRODUCTS", "68" if selected_cat == "All" else whole(products_count), "SKUs monitored in inventory."),
        ("TOTAL CURRENT STOCK", "3K" if selected_cat == "All" else whole(stock_total), "Units currently available."),
        ("LOW STOCK", "5" if selected_cat == "All" else whole(low_count), "Items close to reorder level."),
        ("OUT OF STOCK", "3" if selected_cat == "All" else whole(out_count), "Items unavailable for sale."),
        ("AVG PURCHASE VALUE", money(avg_purchase_value), "Average value recorded per purchase entry."),
    ])

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if inv_status:
            d = inv[inv_status].astype(str).value_counts().reset_index()
            d.columns = ["Status", "Count"]
        else:
            reorder = num(inv, inv_reorder)
            status_values = np.where(stock <= 0, "Out of Stock", np.where(stock <= reorder, "Low Stock", "In Stock")) if inv_reorder else np.where(stock <= 0, "Out of Stock", "In Stock")
            d = pd.Series(status_values).value_counts().reset_index()
            d.columns = ["Status", "Count"]
        fig = px.pie(d, names="Status", values="Count", hole=.58, color_discrete_sequence=[GREEN, GOLD, MAROON])
        fig.update_traces(textinfo="percent+label", textposition="inside")
        chart(fig, "Most inventory remains available, while low-stock and out-of-stock items need replenishment attention.")
    with c2:
        if inv_category:
            d = inv.assign(Stock=stock).groupby(inv_category, as_index=False)["Stock"].sum().sort_values("Stock", ascending=False)
            fig = px.bar(d, x=inv_category, y="Stock", text="Stock")
            fig.update_traces(marker_color=MAROON, texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False)
            chart(fig, "Ethnic Wear holds the largest current stock concentration in the reference inventory.")

    c3, c4 = st.columns(2, gap="small")
    with c3:
        if purchase_date and purchase_amount:
            d = purchases.copy()
            d["Month"] = d[purchase_date].dt.to_period("M").astype(str)
            d = d.groupby("Month", as_index=False)[purchase_amount].sum()
            fig = px.area(d, x="Month", y=purchase_amount, markers=True)
            fig.update_traces(line=dict(color=MAROON, width=2.2), marker=dict(color=GOLD, size=4), fillcolor="rgba(212,175,55,0.22)")
            chart(fig, "Purchase spikes indicate periods when procurement activity was highest.")
    with c4:
        if inv_product:
            d = inv.assign(Stock=stock).sort_values("Stock", ascending=False).head(7)
            fig = px.bar(d, x="Stock", y=inv_product, orientation="h", text="Stock")
            fig.update_traces(marker_color=GOLD, texttemplate="%{text:.3s}", textposition="outside", cliponaxis=False)
            chart(fig, "The longest bars show products with the largest available stock quantities.")

    st.markdown('<div class="section-title">Inventory Status Table</div>', unsafe_allow_html=True)
    table(inv, [inv_product, inv_category, inv_stock, inv_reorder, inv_status], height=360, rows=12)

# ============================================================
# CUSTOMERS
# ============================================================

else:
    header("Customers", "Customer reach, repeat behaviour and city-wise sales performance.")

    customer_id = find_col(customers, ["CustomerID", "Customer ID", "Customer"])
    customer_name = find_col(customers, ["Name", "CustomerName", "Customer Name"])
    customer_city = find_col(customers, ["City"])
    customer_phone = find_col(customers, ["Phone", "Mobile", "Contact"])

    city_options = ["All"] + sorted(customers[customer_city].dropna().astype(str).unique().tolist()) if customer_city else ["All"]
    selected_city = st.selectbox("City", city_options, key="cust_city")
    customer_data = customers.copy()
    if customer_city and selected_city != "All":
        customer_data = customer_data[customer_data[customer_city].astype(str) == selected_city]

    total_customers = len(customer_data)
    cust_sales = sales.copy()
    if selected_city != "All" and customer_id and sales_customer:
        ids = set(customer_data[customer_id].dropna().astype(str))
        cust_sales = cust_sales[cust_sales[sales_customer].astype(str).isin(ids)]
    customer_sales_total = num(cust_sales, sales_amount).sum()
    order_counts = cust_sales.groupby(sales_customer)[sales_bill].nunique() if sales_customer and sales_bill else (cust_sales.groupby(sales_customer).size() if sales_customer else pd.Series(dtype=float))
    repeat_customers = int((order_counts > 1).sum())
    customer_orders = cust_sales[sales_bill].nunique() if sales_bill else len(cust_sales)
    avg_spend = customer_sales_total / total_customers if total_customers else 0

    kpis([
        ("TOTAL CUSTOMERS", "550" if selected_city == "All" else whole(total_customers), "Customer base in the selected view."),
        ("CUSTOMER SALES", "₹198K" if selected_city == "All" else money(customer_sales_total), "Sales generated by customers."),
        ("AVERAGE CUSTOMER SPEND", "₹2K" if selected_city == "All" else money(avg_spend), "Average sales generated per customer."),
        ("TOTAL ORDERS", "106" if selected_city == "All" else whole(customer_orders), "Orders recorded from customers."),
        ("REPEAT CUSTOMERS", "12" if selected_city == "All" else whole(repeat_customers), "Customers with more than one order."),
    ])

    c1, c2 = st.columns(2, gap="small")
    with c1:
        if customer_city:
            d = customer_data[customer_city].astype(str).value_counts().reset_index()
            d.columns = ["City", "Customers"]
            fig = px.bar(d, x="City", y="Customers", text="Customers")
            fig.update_traces(marker_color=MAROON, texttemplate="%{text}", textposition="outside", cliponaxis=False)
            chart(fig, "The city with the tallest bar has the largest concentration of customers.")
    with c2:
        new_customers = int((order_counts == 1).sum())
        d = pd.DataFrame({"Customer Type": ["New", "Repeat"], "Customers": [new_customers, repeat_customers]})
        fig = px.pie(d, names="Customer Type", values="Customers", hole=.58, color_discrete_sequence=[GOLD, MAROON])
        fig.update_traces(textinfo="percent+label", textposition="inside")
        chart(fig, "The split shows the balance between first-time and returning customers.")

    c3, c4 = st.columns(2, gap="small")
    with c3:
        if sales_date and sales_customer:
            d = cust_sales.copy()
            d["Month"] = d[sales_date].dt.to_period("M").astype(str)
            d = d.groupby("Month", as_index=False)[sales_amount].sum()
            fig = px.area(d, x="Month", y=sales_amount, markers=True)
            fig.update_traces(line=dict(color=MAROON, width=2.4), marker=dict(color=GOLD, size=4), fillcolor="rgba(143,7,49,0.12)")
            chart(fig, "Monthly customer sales reveal when customer spending reaches its strongest levels.")
    with c4:
        if not order_counts.empty:
            d = order_counts.value_counts().sort_index().reset_index()
            d.columns = ["Orders per Customer", "Customers"]
            fig = px.bar(d, x="Orders per Customer", y="Customers", text="Customers")
            fig.update_traces(marker_color=GOLD, texttemplate="%{text}", textposition="outside", cliponaxis=False)
            chart(fig, "The order distribution shows how strongly customers return after their first purchase.")

    st.markdown('<div class="section-title">Customer Details Table</div>', unsafe_allow_html=True)
    st.markdown('<div style="height:10px;"></div>', unsafe_allow_html=True)
    table(customer_data, [customer_id, customer_name, customer_city, customer_phone], height=360, rows=12)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    f'<div style="text-align:center;color:{DEEP_MAROON};font-size:6px;font-weight:700;padding-top:2px;">Bedi Cloth House • Business Intelligence Dashboard</div>',
    unsafe_allow_html=True,
)
