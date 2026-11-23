import streamlit as st
import mysql.connector
import os
import pandas as pd
import plotly.express as px

# ==========================================
# PAGE SETTINGS
# ==========================================

st.set_page_config(
    page_title="Bedi Cloth House Management System",
    page_icon="🏬",
    layout="wide"
)

# ==========================================
# CUSTOM DESIGN - BEDI CLOTH HOUSE
# ==========================================

st.markdown("""
<style>

/* MAIN BACKGROUND */
.stApp {
    background: #F8F1E7 !important;
}

[data-testid="stAppViewContainer"] {
    background: #F8F1E7 !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
}

/* MAIN HEADINGS */
h1, h2, h3 {
    color: #800020 !important;
    font-weight: 800 !important;
}

h1 {
    font-size: 42px !important;
}

h2 {
    font-size: 30px !important;
}

h3 {
    font-size: 22px !important;
}

p, label, span {
    font-family: Arial, sans-serif;
}

/* SIDEBAR */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #800020, #4A0012) !important;
    min-width: 260px !important;
    max-width: 260px !important;
}

[data-testid="stSidebar"] > div:first-child {
    background: transparent !important;
}

/* SIDEBAR LOGO */
[data-testid="stSidebar"] img {
    max-width: 100% !important;
    border-radius: 8px;
}

/* SIDEBAR TEXT */
[data-testid="stSidebar"] h1,
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] label {
    color: #FFD700 !important;
    font-weight: 700 !important;
}

/* SIDEBAR SELECT BOX */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFF8E8 !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 10px !important;
}

[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #800020 !important;
    font-weight: 700 !important;
}

/* SIDEBAR INPUTS */
[data-testid="stSidebar"] input {
    background-color: #FFF8E8 !important;
    color: #800020 !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 9px !important;
}

/* KPI CARDS */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #800020, #4A0012) !important;
    padding: 22px 18px !important;
    border-radius: 16px !important;
    border: 1px solid #D4AF37 !important;
    box-shadow: 0 5px 14px rgba(70, 0, 20, 0.20) !important;
    text-align: center !important;
}

/* KPI LABEL */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #FFF1D0 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* KPI VALUES */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div {
    color: #FFD700 !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* KPI DELTA */
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #FFFFFF !important;
}

/* BUTTONS */
.stButton > button,
.stDownloadButton > button {
    background: #800020 !important;
    color: #FFFFFF !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 10px !important;
    font-weight: 700 !important;
    padding: 8px 18px !important;
    transition: 0.2s ease;
}

.stButton > button:hover,
.stDownloadButton > button:hover {
    background: #A00030 !important;
    color: #FFD700 !important;
    border: 1px solid #FFD700 !important;
}

/* INPUT FIELDS */
.stTextInput input,
.stNumberInput input,
.stDateInput input,
.stTimeInput input {
    background-color: #FFFDF8 !important;
    color: #4A0012 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 9px !important;
}

/* SELECT BOXES */
[data-baseweb="select"] > div {
    background-color: #FFFDF8 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 9px !important;
}

/* TEXT AREAS */
.stTextArea textarea {
    background-color: #FFFDF8 !important;
    color: #4A0012 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 9px !important;
}

/* TABLES */
[data-testid="stDataFrame"],
[data-testid="stTable"] {
    border: 1px solid #D4AF37 !important;
    border-radius: 10px !important;
    overflow: hidden;
}

/* EXPANDERS */
[data-testid="stExpander"] {
    background: #FFF8E8 !important;
    border: 1px solid #D4AF37 !important;
    border-radius: 12px !important;
}

/* TABS */
.stTabs [data-baseweb="tab"] {
    color: #800020 !important;
    font-weight: 700 !important;
}

.stTabs [aria-selected="true"] {
    color: #800020 !important;
    border-bottom-color: #D4AF37 !important;
}

/* DIVIDERS */
hr {
    border-color: #D4AF37 !important;
}

/* SUCCESS MESSAGE */
[data-testid="stAlert"] {
    border-radius: 12px !important;
}

/* CHART CONTAINERS */
[data-testid="stPlotlyChart"] {
    background: #FFFDF8;
    border: 1px solid #E4C77A;
    border-radius: 12px;
    padding: 8px;
}

/* HIDE DEFAULT FOOTER */
footer {
    visibility: hidden;
}

</style>
""", unsafe_allow_html=True)

# ==========================================
# SIDEBAR NAVIGATION
# ==========================================

logo_path = "bedi_logo.png"

# Store Logo
if os.path.exists(logo_path):
    st.sidebar.image(logo_path, width=220)

st.sidebar.markdown("---")

# Navigation
st.sidebar.subheader("▦ Navigation")

page = st.sidebar.selectbox(
    "Select Module",
    [
        "Dashboard",
        "Sales Management",
        "Customer Management",
        "Product Management",
        "Inventory Management",
        "Purchase Management",
        "Supplier Management",
        "Sales Targets Management"
    ]
)

st.sidebar.markdown("---")

# Database Connection
st.sidebar.subheader("Database Connection")

# ==========================================
# DATABASE CONFIGURATION
# ==========================================

db_config = st.secrets["mysql"]
password = db_config["password"]

# ==========================================
# MAIN HEADING
# ==========================================

st.title("Bedi Cloth House")
st.subheader("Management Information System")

st.markdown("---")

st.write(
    "Welcome to the Bedi Cloth House Management System. "
    "Manage sales, customers, products, inventory and purchases "
    "from one place."
)
# ==========================================
# DATABASE CONNECTION
# ==========================================

if password:

    try:

        connection = mysql.connector.connect(
            host=db_config["host"],
            port=int(db_config["port"]),
            user=db_config["user"],
            password=db_config["password"],
            database=db_config["database"],
            ssl_disabled=False
        )

        cursor = connection.cursor()

       st.sidebar.markdown("""
<div style="
    background-color: #DDF5DF;
    color: #176B2C;
    padding: 16px 12px;
    border-radius: 12px;
    display: flex;
    align-items: center;
    gap: 12px;
    font-size: 15px;
    font-weight: 700;
    border: 1px solid #A5D6A7;
">
    <span style="
        background-color: #16852D;
        color: white;
        border-radius: 50%;
        width: 27px;
        height: 27px;
        min-width: 27px;
        display: inline-flex;
        align-items: center;
        justify-content: center;
        font-size: 18px;
    ">✓</span>
    <span>Database Connected<br>Successfully!</span>
</div>
""", unsafe_allow_html=True)

        # PART 2 CONTINUES HERE
                # ==========================================
        # HELPER FUNCTIONS
        # ==========================================

        def show_table(query, params=None):

            cursor.execute(query, params or ())
            rows = cursor.fetchall()

            columns = [item[0] for item in cursor.description]

            if rows:
                df = pd.DataFrame(rows, columns=columns)
                st.dataframe(
                    df,
                    use_container_width=True,
                    hide_index=True
                )
            else:
                st.info("No records found.")

        def get_values(query, params=None):

            cursor.execute(query, params or ())
            return [row[0] for row in cursor.fetchall()]

        def safe_commit(message):

            connection.commit()
            st.success(message)
            st.rerun()

        # ==========================================
        # DASHBOARD
        # ==========================================

        if page == "Dashboard":

            st.header("📊 Business Dashboard")

            # FETCH SALES INFORMATION
            cursor.execute("""
                SELECT
                    COALESCE(SUM(TotalAmount), 0),
                    COALESCE(SUM(Profit), 0),
                    COUNT(*)
                FROM sales_transactions
            """)

            sales_summary = cursor.fetchone()

            total_sales = float(sales_summary[0] or 0)
            total_profit = float(sales_summary[1] or 0)
            total_transactions = sales_summary[2]

            # FETCH CUSTOMER COUNT
            cursor.execute("""
                SELECT COUNT(*)
                FROM customers
            """)

            total_customers = cursor.fetchone()[0]

            # FETCH PRODUCT COUNT
            cursor.execute("""
                SELECT COUNT(*)
                FROM products
            """)

            total_products = cursor.fetchone()[0]

            # FETCH STOCK
            cursor.execute("""
                SELECT COALESCE(SUM(CurrentStock), 0)
                FROM inventory
            """)

            total_stock = cursor.fetchone()[0]

            # FETCH PURCHASE AMOUNT
            cursor.execute("""
                SELECT COALESCE(SUM(TotalAmount), 0)
                FROM purchases
            """)

            total_purchases = float(cursor.fetchone()[0] or 0)

            # ======================================
            # KPI CARDS
            # ======================================

            col1, col2, col3 = st.columns(3)

            col1.metric(
                "💰 Total Sales",
                f"₹{total_sales:,.0f}"
            )

            col2.metric(
                "📈 Total Profit",
                f"₹{total_profit:,.0f}"
            )

            col3.metric(
                "🧾 Transactions",
                total_transactions
            )

            col4, col5, col6 = st.columns(3)

            col4.metric(
                "👥 Total Customers",
                total_customers
            )

            col5.metric(
                "👗 Total Products",
                total_products
            )

            col6.metric(
                "📦 Stock Units",
                total_stock
            )

            st.markdown("---")

            # ======================================
            # BUSINESS INSIGHTS
            # ======================================

            st.subheader("💡 Business Highlights")

            cursor.execute("""
                SELECT
                    Category,
                    SUM(TotalAmount) AS TotalSales
                FROM sales_transactions
                GROUP BY Category
                ORDER BY TotalSales DESC
                LIMIT 1
            """)

            top_category = cursor.fetchone()

            cursor.execute("""
                SELECT COUNT(*)
                FROM inventory
                WHERE CurrentStock <= ReorderLevel
            """)

            low_stock = cursor.fetchone()[0]

            cursor.execute("""
                SELECT
                    SalesExecutive,
                    SUM(Profit) AS TotalProfit
                FROM sales_transactions
                GROUP BY SalesExecutive
                ORDER BY TotalProfit DESC
                LIMIT 1
            """)

            top_executive = cursor.fetchone()

            h1, h2, h3 = st.columns(3)

            with h1:
                if top_category:
                    st.info(
                        f"🏆 Best-Selling Category\n\n"
                        f"**{top_category[0]}**"
                    )
                else:
                    st.info("No category information available.")

            with h2:
                st.warning(
                    f"📦 Low Stock Products\n\n"
                    f"**{low_stock} products need attention**"
                )

            with h3:
                if top_executive:
                    st.success(
                        f"⭐ Top Profit Executive\n\n"
                        f"**{top_executive[0]}**"
                    )
                else:
                    st.success("No executive information available.")

            st.markdown("---")

            # ======================================
            # CHART COLOURS
            # ======================================

            chart_colors = [
                "#800020",
                "#D4AF37",
                "#A00030",
                "#E6C875",
                "#4A0012",
                "#B76E79"
            ]

            # ======================================
            # CATEGORY-WISE SALES CHART
            # ======================================

            st.subheader("👗 Category-wise Sales Distribution")

            cursor.execute("""
                SELECT
                    Category,
                    SUM(TotalAmount) AS CategorySales
                FROM sales_transactions
                GROUP BY Category
                ORDER BY CategorySales DESC
            """)

            category_data = cursor.fetchall()

            if category_data:

                category_df = pd.DataFrame(
                    category_data,
                    columns=["Category", "Sales"]
                )

                fig_category = px.pie(
                    category_df,
                    names="Category",
                    values="Sales",
                    hole=0.55,
                    color_discrete_sequence=chart_colors,
                    title="Sales Contribution by Category"
                )

                fig_category.update_traces(
                    textposition="inside",
                    textinfo="percent+label"
                )

                fig_category.update_layout(
                    height=430,
                    font=dict(color="#4A0012"),
                    title_font=dict(
                        size=20,
                        color="#800020"
                    )
                )

                st.plotly_chart(
                    fig_category,
                    use_container_width=True
                )

            else:
                st.info("No category sales data available.")

            st.markdown("---")

            # ======================================
            # PAYMENT MODE ANALYSIS
            # ======================================

            st.subheader("💳 Payment Mode Analysis")

            cursor.execute("""
                SELECT
                    PaymentMode,
                    COUNT(*) AS Transactions,
                    SUM(TotalAmount) AS Revenue
                FROM sales_transactions
                GROUP BY PaymentMode
                ORDER BY Revenue DESC
            """)

            payment_data = cursor.fetchall()

            if payment_data:

                payment_df = pd.DataFrame(
                    payment_data,
                    columns=[
                        "Payment Mode",
                        "Transactions",
                        "Revenue"
                    ]
                )

                pc1, pc2 = st.columns(2)

                with pc1:

                    fig_payment = px.pie(
                        payment_df,
                        names="Payment Mode",
                        values="Transactions",
                        hole=0.55,
                        color_discrete_sequence=chart_colors,
                        title="Transactions by Payment Mode"
                    )

                    fig_payment.update_traces(
                        textposition="inside",
                        textinfo="percent+label"
                    )

                    fig_payment.update_layout(
                        height=380,
                        font=dict(color="#4A0012")
                    )

                    st.plotly_chart(
                        fig_payment,
                        use_container_width=True
                    )

                with pc2:

                    fig_revenue = px.bar(
                        payment_df,
                        x="Payment Mode",
                        y="Revenue",
                        text="Revenue",
                        color="Payment Mode",
                        color_discrete_sequence=chart_colors,
                        title="Revenue by Payment Mode"
                    )

                    fig_revenue.update_traces(
                        texttemplate="₹%{y:,.0f}",
                        textposition="outside"
                    )

                    fig_revenue.update_layout(
                        height=380,
                        showlegend=False,
                        yaxis_title="Revenue (₹)",
                        font=dict(color="#4A0012")
                    )

                    st.plotly_chart(
                        fig_revenue,
                        use_container_width=True
                    )

            else:
                st.info("No payment information available.")

            st.markdown("---")

            # ======================================
            # TOP 5 BEST-SELLING PRODUCTS
            # ======================================

            st.subheader("🏆 Top 5 Best-Selling Products")

            cursor.execute("""
                SELECT
                    p.ProductName,
                    SUM(s.TotalAmount) AS TotalSales
                FROM sales_transactions s
                JOIN products p
                    ON s.ProductID = p.ProductID
                GROUP BY p.ProductID, p.ProductName
                ORDER BY TotalSales DESC
                LIMIT 5
            """)

            product_data = cursor.fetchall()

            if product_data:

                product_df = pd.DataFrame(
                    product_data,
                    columns=["Product", "Sales"]
                )

                product_df = product_df.sort_values(
                    "Sales",
                    ascending=True
                )

                fig_products = px.bar(
                    product_df,
                    x="Sales",
                    y="Product",
                    orientation="h",
                    text="Sales",
                    color="Sales",
                    color_continuous_scale=[
                        "#E6C875",
                        "#A00030",
                        "#800020"
                    ],
                    title="Top Performing Products"
                )

                fig_products.update_traces(
                    texttemplate="₹%{x:,.0f}",
                    textposition="outside"
                )

                fig_products.update_layout(
                    height=430,
                    coloraxis_showscale=False,
                    xaxis_title="Total Sales (₹)",
                    yaxis_title="Product",
                    font=dict(color="#4A0012")
                )

                st.plotly_chart(
                    fig_products,
                    use_container_width=True
                )

            else:
                st.info("No product sales data available.")

            st.markdown("---")

            # ======================================
            # PURCHASE SUMMARY
            # ======================================

            st.subheader("🛒 Purchase Overview")

            st.metric(
                "Total Purchase Amount",
                f"₹{total_purchases:,.0f}"
            )
                    # ==========================================
        # CUSTOMER MANAGEMENT
        # ==========================================

        elif page == "Customer Management":

            st.header("👥 Customer Management")

            st.write(
                "Add, view, update and manage customer information."
            )

            # ADD CUSTOMER
            with st.expander("➕ Add New Customer", expanded=True):

                with st.form("add_customer_form"):

                    new_id = st.text_input("Customer ID")
                    new_name = st.text_input("Customer Name")
                    new_phone = st.text_input("Phone Number")
                    new_city = st.text_input("City")
                    new_date = st.date_input("Join Date")

                    submitted = st.form_submit_button(
                        "Add Customer"
                    )

                    if submitted:

                        if new_id.strip() and new_name.strip():

                            try:

                                cursor.execute("""
                                    INSERT INTO customers
                                    (
                                        CustomerID,
                                        CustomerName,
                                        Phone,
                                        City,
                                        JoinDate
                                    )
                                    VALUES (%s, %s, %s, %s, %s)
                                """, (
                                    new_id.strip(),
                                    new_name.strip(),
                                    new_phone.strip(),
                                    new_city.strip(),
                                    new_date
                                ))

                                safe_commit(
                                    "Customer added successfully!"
                                )

                            except mysql.connector.Error as error:

                                connection.rollback()

                                st.error(
                                    f"Unable to add customer: {error}"
                                )

                        else:

                            st.warning(
                                "Customer ID and Customer Name are required."
                            )

            # CUSTOMER RECORDS
            st.markdown("---")
            st.subheader("📋 Customer Records")

            show_table("""
                SELECT
                    CustomerID,
                    CustomerName,
                    Phone,
                    City,
                    JoinDate
                FROM customers
                ORDER BY CustomerName
            """)

            customer_ids = get_values("""
                SELECT CustomerID
                FROM customers
                ORDER BY CustomerID
            """)

            # UPDATE CUSTOMER
            if customer_ids:

                st.markdown("---")
                st.subheader("✏️ Update Customer")

                selected_id = st.selectbox(
                    "Select Customer ID to Update",
                    customer_ids
                )

                cursor.execute("""
                    SELECT
                        CustomerName,
                        Phone,
                        City
                    FROM customers
                    WHERE CustomerID=%s
                """, (selected_id,))

                customer = cursor.fetchone()

                with st.form("update_customer_form"):

                    updated_name = st.text_input(
                        "Customer Name",
                        value=customer[0] or ""
                    )

                    updated_phone = st.text_input(
                        "Phone Number",
                        value=customer[1] or ""
                    )

                    updated_city = st.text_input(
                        "City",
                        value=customer[2] or ""
                    )

                    update_btn = st.form_submit_button(
                        "Update Customer"
                    )

                    if update_btn:

                        if updated_name.strip():

                            try:

                                cursor.execute("""
                                    UPDATE customers
                                    SET
                                        CustomerName=%s,
                                        Phone=%s,
                                        City=%s
                                    WHERE CustomerID=%s
                                """, (
                                    updated_name.strip(),
                                    updated_phone.strip(),
                                    updated_city.strip(),
                                    selected_id
                                ))

                                safe_commit(
                                    "Customer updated successfully!"
                                )

                            except mysql.connector.Error as error:

                                connection.rollback()

                                st.error(
                                    f"Unable to update customer: {error}"
                                )

                        else:

                            st.warning(
                                "Customer name cannot be empty."
                            )

                # DELETE CUSTOMER
                st.markdown("---")
                st.subheader("🗑️ Delete Customer")

                delete_id = st.selectbox(
                    "Select Customer ID to Delete",
                    customer_ids,
                    key="delete_customer"
                )

                if st.button(
                    "Delete Customer",
                    key="delete_customer_button"
                ):

                    try:

                        cursor.execute("""
                            DELETE FROM customers
                            WHERE CustomerID=%s
                        """, (delete_id,))

                        safe_commit(
                            "Customer deleted successfully!"
                        )

                    except mysql.connector.Error as error:

                        connection.rollback()

                        st.error(
                            "This customer cannot be deleted because "
                            "they may have linked sales records."
                        )

            else:

                st.info("No customer records are available.")

        # ==========================================
        # PRODUCT MANAGEMENT
        # ==========================================

        elif page == "Product Management":

            st.header("👗 Product Management")

            st.write(
                "Manage product details, prices and categories."
            )

            categories = get_values("""
                SELECT Category
                FROM categories
                ORDER BY Category
            """)

            # ADD PRODUCT
            if categories:

                with st.expander(
                    "➕ Add New Product",
                    expanded=True
                ):

                    with st.form("add_product_form"):

                        product_id = st.text_input("Product ID")

                        product_name = st.text_input(
                            "Product Name"
                        )

                        category = st.selectbox(
                            "Category",
                            categories
                        )

                        cost_price = st.number_input(
                            "Cost Price (₹)",
                            min_value=0.0,
                            value=0.0
                        )

                        selling_price = st.number_input(
                            "Selling Price (₹)",
                            min_value=0.0,
                            value=0.0
                        )

                        margin = st.number_input(
                            "Margin Percentage",
                            min_value=0.0,
                            value=0.0
                        )

                        add_product = st.form_submit_button(
                            "Add Product"
                        )

                        if add_product:

                            if (
                                product_id.strip()
                                and product_name.strip()
                            ):

                                try:

                                    cursor.execute("""
                                        INSERT INTO products
                                        (
                                            ProductID,
                                            ProductName,
                                            Category,
                                            CostPrice,
                                            SellingPrice,
                                            MarginPct
                                        )
                                        VALUES (%s, %s, %s, %s, %s, %s)
                                    """, (
                                        product_id.strip(),
                                        product_name.strip(),
                                        category,
                                        cost_price,
                                        selling_price,
                                        margin
                                    ))

                                    safe_commit(
                                        "Product added successfully!"
                                    )

                                except mysql.connector.Error as error:

                                    connection.rollback()

                                    st.error(
                                        f"Unable to add product: {error}"
                                    )

                            else:

                                st.warning(
                                    "Product ID and Product Name are required."
                                )

            else:

                st.warning(
                    "No categories found in the database."
                )

            # PRODUCT RECORDS
            st.markdown("---")
            st.subheader("📋 Product Records")

            show_table("""
                SELECT
                    ProductID,
                    ProductName,
                    Category,
                    CostPrice,
                    SellingPrice,
                    MarginPct
                FROM products
                ORDER BY ProductName
            """)

            product_ids = get_values("""
                SELECT ProductID
                FROM products
                ORDER BY ProductID
            """)

            # UPDATE AND DELETE PRODUCT
            if product_ids and categories:

                st.markdown("---")
                st.subheader("✏️ Update Product")

                selected_product = st.selectbox(
                    "Select Product ID to Update",
                    product_ids
                )

                cursor.execute("""
                    SELECT
                        ProductName,
                        Category,
                        CostPrice,
                        SellingPrice,
                        MarginPct
                    FROM products
                    WHERE ProductID=%s
                """, (selected_product,))

                product = cursor.fetchone()

                with st.form("update_product_form"):

                    updated_name = st.text_input(
                        "Product Name",
                        value=product[0] or ""
                    )

                    category_index = (
                        categories.index(product[1])
                        if product[1] in categories
                        else 0
                    )

                    updated_category = st.selectbox(
                        "Category",
                        categories,
                        index=category_index
                    )

                    updated_cost = st.number_input(
                        "Cost Price (₹)",
                        min_value=0.0,
                        value=float(product[2] or 0)
                    )

                    updated_selling = st.number_input(
                        "Selling Price (₹)",
                        min_value=0.0,
                        value=float(product[3] or 0)
                    )

                    updated_margin = st.number_input(
                        "Margin Percentage",
                        min_value=0.0,
                        value=float(product[4] or 0)
                    )

                    update_product = st.form_submit_button(
                        "Update Product"
                    )

                    if update_product:

                        if updated_name.strip():

                            try:

                                cursor.execute("""
                                    UPDATE products
                                    SET
                                        ProductName=%s,
                                        Category=%s,
                                        CostPrice=%s,
                                        SellingPrice=%s,
                                        MarginPct=%s
                                    WHERE ProductID=%s
                                """, (
                                    updated_name.strip(),
                                    updated_category,
                                    updated_cost,
                                    updated_selling,
                                    updated_margin,
                                    selected_product
                                ))

                                safe_commit(
                                    "Product updated successfully!"
                                )

                            except mysql.connector.Error as error:

                                connection.rollback()

                                st.error(
                                    f"Unable to update product: {error}"
                                )

                        else:

                            st.warning(
                                "Product name cannot be empty."
                            )

                # DELETE PRODUCT
                st.markdown("---")
                st.subheader("🗑️ Delete Product")

                delete_product = st.selectbox(
                    "Select Product ID to Delete",
                    product_ids,
                    key="delete_product"
                )

                if st.button(
                    "Delete Product",
                    key="delete_product_button"
                ):

                    try:

                        cursor.execute("""
                            DELETE FROM products
                            WHERE ProductID=%s
                        """, (delete_product,))

                        safe_commit(
                            "Product deleted successfully!"
                        )

                    except mysql.connector.Error as error:

                        connection.rollback()

                        st.error(
                            "This product cannot be deleted because "
                            "it may be linked to sales, inventory "
                            "or purchase records."
                        )

            elif not product_ids:

                st.info("No product records are available.")

                    # ==========================================
        # INVENTORY MANAGEMENT
        # ==========================================

        elif page == "Inventory Management":

            st.header("📦 Inventory Management")

            st.write(
                "Monitor stock levels, stock value and low-stock products."
            )

            # INVENTORY SUMMARY
            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(CurrentStock), 0),
                    COALESCE(SUM(StockValue), 0),
                    SUM(
                        CASE
                            WHEN CurrentStock <= ReorderLevel
                            AND CurrentStock > 0
                            THEN 1 ELSE 0
                        END
                    ),
                    SUM(
                        CASE
                            WHEN CurrentStock = 0
                            THEN 1 ELSE 0
                        END
                    )
                FROM inventory
            """)

            inventory_summary = cursor.fetchone()

            c1, c2, c3, c4, c5 = st.columns(5)

            c1.metric(
                "Total SKUs",
                inventory_summary[0]
            )

            c2.metric(
                "Stock Units",
                inventory_summary[1]
            )

            c3.metric(
                "Stock Value",
                f"₹{float(inventory_summary[2] or 0):,.0f}"
            )

            c4.metric(
                "Low Stock",
                inventory_summary[3] or 0
            )

            c5.metric(
                "Out of Stock",
                inventory_summary[4] or 0
            )

            st.markdown("---")

            # INVENTORY RECORDS
            st.subheader("📋 Inventory Records")

            show_table("""
                SELECT
                    ProductID,
                    ProductName,
                    Category,
                    CurrentStock,
                    ReorderLevel,
                    Status,
                    StockValue,
                    PreferredSupplierID
                FROM inventory
                ORDER BY ProductName
            """)

            st.markdown("---")

            # LOW STOCK ALERTS
            st.subheader("⚠️ Low Stock Alerts")

            show_table("""
                SELECT
                    ProductID,
                    ProductName,
                    CurrentStock,
                    ReorderLevel,
                    Status
                FROM inventory
                WHERE CurrentStock <= ReorderLevel
                ORDER BY CurrentStock ASC
            """)

            # UPDATE INVENTORY
            inventory_ids = get_values("""
                SELECT ProductID
                FROM inventory
                ORDER BY ProductID
            """)

            if inventory_ids:

                st.markdown("---")
                st.subheader("✏️ Update Stock")

                selected_inventory = st.selectbox(
                    "Select Product ID",
                    inventory_ids
                )

                cursor.execute("""
                    SELECT
                        CurrentStock,
                        ReorderLevel
                    FROM inventory
                    WHERE ProductID=%s
                """, (selected_inventory,))

                stock_details = cursor.fetchone()

                with st.form("update_inventory_form"):

                    new_stock = st.number_input(
                        "Current Stock Quantity",
                        min_value=0,
                        value=int(stock_details[0] or 0)
                    )

                    new_reorder = st.number_input(
                        "Reorder Level",
                        min_value=0,
                        value=int(stock_details[1] or 0)
                    )

                    update_inventory = st.form_submit_button(
                        "Update Inventory"
                    )

                    if update_inventory:

                        if new_stock == 0:
                            new_status = "Out of Stock"

                        elif new_stock <= new_reorder:
                            new_status = "Low Stock"

                        else:
                            new_status = "In Stock"

                        try:

                            cursor.execute("""
                                UPDATE inventory
                                SET
                                    CurrentStock=%s,
                                    ReorderLevel=%s,
                                    Status=%s
                                WHERE ProductID=%s
                            """, (
                                new_stock,
                                new_reorder,
                                new_status,
                                selected_inventory
                            ))

                            safe_commit(
                                "Inventory updated successfully!"
                            )

                        except mysql.connector.Error as error:

                            connection.rollback()

                            st.error(
                                f"Unable to update inventory: {error}"
                            )

            # ==========================================
            # SALES MANAGEMENT
            # ==========================================

        elif page == "Sales Management":

            st.header("💰 Sales Management")

            st.write(
                "View sales transactions and record new sales."
            )

            # SALES SUMMARY
            cursor.execute("""
                SELECT
                    COALESCE(SUM(TotalAmount), 0),
                    COALESCE(SUM(Profit), 0),
                    COUNT(*)
                FROM sales_transactions
            """)

            sales_summary = cursor.fetchone()

            s1, s2, s3 = st.columns(3)

            s1.metric(
                "Total Revenue",
                f"₹{float(sales_summary[0]):,.0f}"
            )

            s2.metric(
                "Total Profit",
                f"₹{float(sales_summary[1]):,.0f}"
            )

            s3.metric(
                "Total Transactions",
                sales_summary[2]
            )

            st.markdown("---")

            # SALES FILTERS
            st.subheader("🔍 Search and Filter Sales")

            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:

                payment_filter = st.selectbox(
                    "Payment Mode",
                    ["All", "Cash", "UPI", "Card"]
                )

            with filter_col2:

                search_bill = st.text_input(
                    "Search Bill Number"
                )

            sales_query = """
                SELECT
                    BillNo,
                    Date,
                    CustomerID,
                    ProductID,
                    Category,
                    Qty,
                    TotalAmount,
                    Profit,
                    SalesExecutive,
                    PaymentMode
                FROM sales_transactions
                WHERE 1=1
            """

            sales_params = []

            if payment_filter != "All":

                sales_query += " AND PaymentMode=%s"
                sales_params.append(payment_filter)

            if search_bill.strip():

                sales_query += " AND BillNo LIKE %s"
                sales_params.append(
                    "%" + search_bill.strip() + "%"
                )

            sales_query += " ORDER BY Date DESC"

            st.subheader("📋 Sales Transactions")

            show_table(
                sales_query,
                tuple(sales_params)
            )

            st.markdown("---")

            # ADD NEW SALE
            st.subheader("➕ Add New Sales Transaction")

            customer_ids = get_values("""
                SELECT CustomerID
                FROM customers
                ORDER BY CustomerID
            """)

            product_ids = get_values("""
                SELECT ProductID
                FROM products
                ORDER BY ProductID
            """)

            if not customer_ids or not product_ids:

                st.warning(
                    "Please add customers and products before "
                    "recording a sale."
                )

            else:

                with st.form("add_sales_form"):

                    bill_no = st.text_input("Bill Number")

                    customer_id = st.selectbox(
                        "Customer",
                        customer_ids
                    )

                    product_id = st.selectbox(
                        "Product",
                        product_ids
                    )

                    quantity = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=1
                    )

                    sales_date = st.date_input(
                        "Sales Date"
                    )

                    sales_executive = st.text_input(
                        "Sales Executive"
                    )

                    sale_payment_mode = st.selectbox(
                        "Payment Mode",
                        ["Cash", "UPI", "Card"]
                    )

                    discount = st.number_input(
                        "Discount Percentage",
                        min_value=0.0,
                        max_value=100.0,
                        value=0.0
                    )

                    submit_sale = st.form_submit_button(
                        "Add Sale"
                    )

                    if submit_sale:

                        if (
                            not bill_no.strip()
                            or not sales_executive.strip()
                        ):

                            st.warning(
                                "Bill Number and Sales Executive are required."
                            )

                        else:

                            try:

                                # CHECK AVAILABLE STOCK
                                cursor.execute("""
                                    SELECT CurrentStock
                                    FROM inventory
                                    WHERE ProductID=%s
                                """, (product_id,))

                                stock_result = cursor.fetchone()

                                if stock_result is None:

                                    st.error(
                                        "Product inventory record not found."
                                    )

                                elif quantity > int(stock_result[0]):

                                    st.error(
                                        f"Only {stock_result[0]} units "
                                        "are available."
                                    )

                                else:

                                    # FETCH PRODUCT DETAILS
                                    cursor.execute("""
                                        SELECT
                                            Category,
                                            CostPrice,
                                            SellingPrice
                                        FROM products
                                        WHERE ProductID=%s
                                    """, (product_id,))

                                    product = cursor.fetchone()

                                    if product is None:

                                        st.error(
                                            "Product not found."
                                        )

                                    else:

                                        category = product[0]

                                        cost_price = float(
                                            product[1] or 0
                                        )

                                        selling_price = float(
                                            product[2] or 0
                                        )

                                        effective_price = (
                                            selling_price *
                                            (1 - discount / 100)
                                        )

                                        total_amount = (
                                            effective_price * quantity
                                        )

                                        total_cost = (
                                            cost_price * quantity
                                        )

                                        profit = (
                                            total_amount - total_cost
                                        )

                                        # INSERT SALE
                                        cursor.execute("""
                                            INSERT INTO sales_transactions
                                            (
                                                BillNo,
                                                Date,
                                                CustomerID,
                                                ProductID,
                                                Category,
                                                Qty,
                                                UnitPrice,
                                                DiscountPct,
                                                EffectivePrice,
                                                TotalAmount,
                                                TotalCost,
                                                Profit,
                                                SalesExecutive,
                                                PaymentMode
                                            )
                                            VALUES (
                                                %s,%s,%s,%s,%s,%s,%s,
                                                %s,%s,%s,%s,%s,%s,%s
                                            )
                                        """, (
                                            bill_no.strip(),
                                            sales_date,
                                            customer_id,
                                            product_id,
                                            category,
                                            quantity,
                                            selling_price,
                                            discount,
                                            effective_price,
                                            total_amount,
                                            total_cost,
                                            profit,
                                            sales_executive.strip(),
                                            sale_payment_mode
                                        ))

                                        # REDUCE INVENTORY
                                        cursor.execute("""
                                            UPDATE inventory
                                            SET CurrentStock = CurrentStock - %s
                                            WHERE ProductID=%s
                                        """, (
                                            quantity,
                                            product_id
                                        ))

                                        # UPDATE STOCK STATUS
                                        cursor.execute("""
                                            SELECT
                                                CurrentStock,
                                                ReorderLevel
                                            FROM inventory
                                            WHERE ProductID=%s
                                        """, (product_id,))

                                        updated_stock = cursor.fetchone()

                                        if updated_stock[0] == 0:

                                            new_status = "Out of Stock"

                                        elif updated_stock[0] <= updated_stock[1]:

                                            new_status = "Low Stock"

                                        else:

                                            new_status = "In Stock"

                                        cursor.execute("""
                                            UPDATE inventory
                                            SET Status=%s
                                            WHERE ProductID=%s
                                        """, (
                                            new_status,
                                            product_id
                                        ))

                                        safe_commit(
                                            "Sales transaction added successfully!"
                                        )

                            except mysql.connector.Error as error:

                                connection.rollback()

                                st.error(
                                    f"Unable to add sale: {error}"
                                )

                        # ==========================================
        # PURCHASE MANAGEMENT
        # ==========================================

        elif page == "Purchase Management":

            st.header("🛒 Purchase Management")

            st.write(
                "Manage purchase orders and track purchases from suppliers."
            )

            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(TotalAmount), 0)
                FROM purchases
            """)

            purchase_summary = cursor.fetchone()

            p1, p2 = st.columns(2)

            p1.metric(
                "Total Purchase Orders",
                purchase_summary[0]
            )

            p2.metric(
                "Total Purchase Amount",
                f"₹{float(purchase_summary[1]):,.0f}"
            )

            st.markdown("---")

            st.subheader("📋 Purchase Records")

            show_table("""
                SELECT
                    PONumber,
                    Date,
                    SupplierID,
                    ProductID,
                    Category,
                    Qty,
                    UnitCost,
                    TotalAmount,
                    Status
                FROM purchases
                ORDER BY Date DESC
            """)

            st.markdown("---")

            st.subheader("➕ Add New Purchase")

            supplier_ids = get_values("""
                SELECT SupplierID
                FROM suppliers
                ORDER BY SupplierID
            """)

            product_ids = get_values("""
                SELECT ProductID
                FROM products
                ORDER BY ProductID
            """)

            if not supplier_ids or not product_ids:

                st.warning(
                    "Please add suppliers and products first."
                )

            else:

                with st.form("add_purchase_form"):

                    po_number = st.text_input("Purchase Order Number")

                    supplier_id = st.selectbox(
                        "Supplier",
                        supplier_ids
                    )

                    product_id = st.selectbox(
                        "Product",
                        product_ids
                    )

                    purchase_date = st.date_input(
                        "Purchase Date"
                    )

                    purchase_qty = st.number_input(
                        "Quantity",
                        min_value=1,
                        value=1
                    )

                    unit_cost = st.number_input(
                        "Unit Cost",
                        min_value=0.0,
                        value=100.0
                    )

                    purchase_status = st.selectbox(
                        "Purchase Status",
                        ["Pending", "Completed", "Cancelled"]
                    )

                    submit_purchase = st.form_submit_button(
                        "Add Purchase"
                    )

                    if submit_purchase:

                        if not po_number.strip():

                            st.warning(
                                "Please enter a Purchase Order Number."
                            )

                        else:

                            try:

                                cursor.execute("""
                                    SELECT Category
                                    FROM products
                                    WHERE ProductID=%s
                                """, (product_id,))

                                product_result = cursor.fetchone()

                                if product_result is None:

                                    st.error("Product not found.")

                                else:

                                    category = product_result[0]

                                    total_amount = (
                                        purchase_qty * unit_cost
                                    )

                                    cursor.execute("""
                                        INSERT INTO purchases
                                        (
                                            PONumber,
                                            Date,
                                            SupplierID,
                                            ProductID,
                                            Category,
                                            Qty,
                                            UnitCost,
                                            TotalAmount,
                                            Status
                                        )
                                        VALUES (
                                            %s,%s,%s,%s,%s,%s,%s,%s,%s
                                        )
                                    """, (
                                        po_number.strip(),
                                        purchase_date,
                                        supplier_id,
                                        product_id,
                                        category,
                                        purchase_qty,
                                        unit_cost,
                                        total_amount,
                                        purchase_status
                                    ))

                                    # Increase stock only for completed purchases
                                    if purchase_status == "Completed":

                                        cursor.execute("""
                                            UPDATE inventory
                                            SET CurrentStock = CurrentStock + %s
                                            WHERE ProductID=%s
                                        """, (
                                            purchase_qty,
                                            product_id
                                        ))

                                        cursor.execute("""
                                            SELECT
                                                CurrentStock,
                                                ReorderLevel
                                            FROM inventory
                                            WHERE ProductID=%s
                                        """, (product_id,))

                                        stock = cursor.fetchone()

                                        if stock:

                                            if stock[0] == 0:
                                                new_status = "Out of Stock"

                                            elif stock[0] <= stock[1]:
                                                new_status = "Low Stock"

                                            else:
                                                new_status = "In Stock"

                                            cursor.execute("""
                                                UPDATE inventory
                                                SET Status=%s
                                                WHERE ProductID=%s
                                            """, (
                                                new_status,
                                                product_id
                                            ))

                                    safe_commit(
                                        "Purchase record added successfully!"
                                    )

                            except mysql.connector.Error as error:

                                connection.rollback()

                                st.error(
                                    f"Unable to add purchase: {error}"
                                )

        # ==========================================
        # SUPPLIER MANAGEMENT
        # ==========================================

        elif page == "Supplier Management":

            st.header("🚚 Supplier Management")

            st.write(
                "Maintain supplier information and contact details."
            )

            cursor.execute("""
                SELECT COUNT(*)
                FROM suppliers
            """)

            total_suppliers = cursor.fetchone()[0]

            st.metric(
                "Total Suppliers",
                total_suppliers
            )

            st.markdown("---")

            st.subheader("📋 Supplier Records")

            show_table("""
                SELECT
                    SupplierID,
                    SupplierName,
                    CategorySupplied,
                    City,
                    ContactNo
                FROM suppliers
                ORDER BY SupplierName
            """)

            st.markdown("---")

            # ADD SUPPLIER
            st.subheader("➕ Add New Supplier")

            with st.form("add_supplier_form"):

                supplier_name = st.text_input(
                    "Supplier Name"
                )

                category_supplied = st.text_input(
                    "Category Supplied"
                )

                supplier_city = st.text_input(
                    "City"
                )

                supplier_contact = st.text_input(
                    "Contact Number"
                )

                submit_supplier = st.form_submit_button(
                    "Add Supplier"
                )

                if submit_supplier:

                    if not supplier_name.strip():

                        st.warning(
                            "Supplier name is required."
                        )

                    else:

                        try:

                            cursor.execute("""
                                SELECT COALESCE(MAX(SupplierID), 0) + 1
                                FROM suppliers
                            """)

                            new_supplier_id = cursor.fetchone()[0]

                            cursor.execute("""
                                INSERT INTO suppliers
                                (
                                    SupplierID,
                                    SupplierName,
                                    CategorySupplied,
                                    City,
                                    ContactNo
                                )
                                VALUES (%s,%s,%s,%s,%s)
                            """, (
                                new_supplier_id,
                                supplier_name.strip(),
                                category_supplied,
                                supplier_city,
                                supplier_contact
                            ))

                            safe_commit(
                                "Supplier added successfully!"
                            )

                        except mysql.connector.Error as error:

                            connection.rollback()

                            st.error(
                                f"Unable to add supplier: {error}"
                            )

            st.markdown("---")

            # UPDATE SUPPLIER
            st.subheader("✏️ Update Supplier")

            supplier_ids = get_values("""
                SELECT SupplierID
                FROM suppliers
                ORDER BY SupplierID
            """)

            if supplier_ids:

                selected_supplier = st.selectbox(
                    "Select Supplier ID",
                    supplier_ids,
                    key="update_supplier_id"
                )

                cursor.execute("""
                    SELECT
                        SupplierName,
                        CategorySupplied,
                        City,
                        ContactNo
                    FROM suppliers
                    WHERE SupplierID=%s
                """, (selected_supplier,))

                supplier_details = cursor.fetchone()

                with st.form("update_supplier_form"):

                    updated_supplier_name = st.text_input(
                        "Supplier Name",
                        value=supplier_details[0] or ""
                    )

                    updated_category = st.text_input(
                        "Category Supplied",
                        value=supplier_details[1] or ""
                    )

                    updated_city = st.text_input(
                        "City",
                        value=supplier_details[2] or ""
                    )

                    updated_contact = st.text_input(
                        "Contact Number",
                        value=supplier_details[3] or ""
                    )

                    update_supplier = st.form_submit_button(
                        "Update Supplier"
                    )

                    if update_supplier:

                        try:

                            cursor.execute("""
                                UPDATE suppliers
                                SET
                                    SupplierName=%s,
                                    CategorySupplied=%s,
                                    City=%s,
                                    ContactNo=%s
                                WHERE SupplierID=%s
                            """, (
                                updated_supplier_name,
                                updated_category,
                                updated_city,
                                updated_contact,
                                selected_supplier
                            ))

                            safe_commit(
                                "Supplier details updated successfully!"
                            )

                        except mysql.connector.Error as error:

                            connection.rollback()

                            st.error(
                                f"Unable to update supplier: {error}"
                            )

        # ==========================================
        # SALES TARGETS MANAGEMENT
        # ==========================================

        elif page == "Sales Targets Management":

            st.header("🎯 Sales Targets Management")

            st.write(
                "Monitor sales executive targets and their performance."
            )

            st.markdown("---")

            st.subheader("📋 Sales Target Records")

            show_table("""
                SELECT *
                FROM sales_targets
            """)

            st.markdown("---")

            st.subheader("📊 Target Performance Summary")

            cursor.execute("""
                SELECT COUNT(*)
                FROM sales_targets
            """)

            total_targets = cursor.fetchone()[0]

            st.metric(
                "Total Target Records",
                total_targets
            )

            cursor.execute("""
                SHOW COLUMNS FROM sales_targets
            """)

            target_columns = [
                row[0] for row in cursor.fetchall()
            ]

            st.caption(
                "Target table columns: " +
                ", ".join(target_columns)
            )

        # ==========================================
        # APPLICATION FOOTER
        # ==========================================
        st.markdown("---")

        st.markdown(
            """
<div style="
    background-color: #800020;
    padding: 25px;
    border-radius: 12px;
    text-align: center;
">
    <h2 style="color: #FFD700;">BEDI CLOTH HOUSE</h2>
    <h4 style="color: white;">Tradition Meets Trend</h4>
    <p style="color: white;">Business Management System</p>
    <p style="color: white;">Developed using Python, Streamlit and MySQL</p>
</div>
            """,
            unsafe_allow_html=True
        )

    except mysql.connector.Error as error:

        st.error(f"Database Error: {error}")

    except Exception as error:

        st.error(f"Application Error: {error}")

else:

    st.warning(
        "Please enter your database password in Streamlit Secrets."
    )