import streamlit as st
import mysql.connector
import os

# Page settings
st.set_page_config(
    page_title="Bedi Cloth House Management System",
    page_icon="🏬",
    layout="wide"
)

# Custom design
st.markdown("""
<style>

/* Main background */
.stApp {
    background-color: #F8F1E7;
}

/* Headings */
h1, h2, h3 {
    color: #800020 !important;
    font-weight: 700;
}

/* Normal text */
p, label {
    color: #4A2630;
}

/* KPI Cards */
[data-testid="stMetric"] {
    background: linear-gradient(135deg, #800020, #4A0012);
    padding: 22px 18px;
    border-radius: 16px;
    border: 1px solid #D4AF37;
    box-shadow: 0 5px 12px rgba(70, 0, 20, 0.18);
    text-align: center;
}

/* KPI Labels */
[data-testid="stMetricLabel"] {
    color: #F5DFA0 !important;
    font-size: 15px;
    font-weight: 600;
}

/* KPI Values */
[data-testid="stMetricValue"] {
    color: #FFD700 !important;
    font-size: 28px;
    font-weight: 800;
}

/* FORCE KPI TEXT VISIBILITY */

/* KPI Labels */
[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricLabel"] p {
    color: #FFF1D0 !important;
    font-size: 16px !important;
    font-weight: 700 !important;
}

/* KPI Numbers */
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] *,
[data-testid="stMetricValue"] div {
    color: #FFD700 !important;
    font-size: 30px !important;
    font-weight: 800 !important;
}

/* KPI Delta Text */
[data-testid="stMetricDelta"],
[data-testid="stMetricDelta"] * {
    color: #FFFFFF !important;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #4A0012;
}

/* SIDEBAR NAVIGATION AND INPUT VISIBILITY */

/* Sidebar headings and labels */
[data-testid="stSidebar"] h2,
[data-testid="stSidebar"] h3,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] p {
    color: #FFD700 !important;
    font-weight: 700 !important;
}

/* Navigation dropdown */
[data-testid="stSidebar"] [data-baseweb="select"] > div {
    background-color: #FFF8E8 !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 10px !important;
}

/* Selected dropdown text */
[data-testid="stSidebar"] [data-baseweb="select"] * {
    color: #800020 !important;
    font-weight: 700 !important;
}

/* Dropdown menu options */
[data-baseweb="popover"] ul {
    background-color: #FFF8E8 !important;
}

[data-baseweb="popover"] li {
    color: #800020 !important;
    font-weight: 600 !important;
}

/* Password and other input boxes */
[data-testid="stSidebar"] input {
    background-color: #FFF8E8 !important;
    color: #800020 !important;
    border: 2px solid #D4AF37 !important;
    border-radius: 9px !important;
    font-weight: 600 !important;
}

/* Password placeholder */
[data-testid="stSidebar"] input::placeholder {
    color: #987080 !important;
}

/* Database connection success message */
[data-testid="stSidebar"] [data-testid="stAlert"] {
    background-color: #FFF1D0 !important;
    border: 1px solid #D4AF37 !important;
}

[data-testid="stSidebar"] [data-testid="stAlert"] * {
    color: #800020 !important;
    font-weight: 700 !important;
}

[data-testid="stSidebar"] * {
    color: #FFF1D0 !important;
}

/* Buttons */
.stButton > button {
    background-color: #800020;
    color: white;
    border: 1px solid #D4AF37;
    border-radius: 9px;
    font-weight: 600;
}

.stButton > button:hover {
    background-color: #A00030;
    color: #FFD700;
    border: 1px solid #FFD700;
}

/* Input fields */
.stTextInput input,
.stNumberInput input,
.stSelectbox div[data-baseweb="select"] {
    border-radius: 8px;
}

/* Data tables */
[data-testid="stDataFrame"] {
    border: 1px solid #D4AF37;
    border-radius: 10px;
}

/* Horizontal divider */
hr {
    border-color: #D4AF37;
}

</style>
""", unsafe_allow_html=True)


# Sidebar
st.sidebar.title("🏬 Bedi Cloth House")
st.sidebar.caption("Tradition Meets Trend")
st.sidebar.markdown("---")

st.sidebar.subheader("Navigation")

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

st.sidebar.subheader("Database Connection")

password = st.sidebar.text_input(
    "MySQL Root Password",
    type="password"
)


# Main heading
logo_path = "bedi_logo.png"

if os.path.exists(logo_path):
    st.image(logo_path, width=130)

st.title("Bedi Cloth House")
st.subheader("Management Information System")

st.markdown("---")

st.write(
    "Welcome to the Bedi Cloth House Management System. "
    "Manage sales, customers, products, inventory and purchases "
    "from one place."
)


# Database connection
if password:

    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password,
            database="bedi_cloth_house"
        )

        cursor = connection.cursor()

        st.sidebar.success("Database Connected Successfully!")

        # LIVE BUSINESS DASHBOARD

        st.markdown("### 📊 Business Overview")
                # MONTHLY SALES PERFORMANCE

        st.markdown("### 📈 Monthly Sales Performance")

        cursor.execute("""
            SELECT DATE_FORMAT(Date, '%Y-%m') AS SalesMonth,
                   SUM(TotalAmount) AS MonthlySales
            FROM sales_transactions
            GROUP BY DATE_FORMAT(Date, '%Y-%m')
            ORDER BY SalesMonth
        """)

        monthly_sales = cursor.fetchall()

        if monthly_sales:
            import pandas as pd

            sales_df = pd.DataFrame(
                monthly_sales,
                columns=["Month", "Sales"]
            )

            st.line_chart(
                sales_df.set_index("Month"),
                height=350,
                use_container_width=True
            )
        else:
            st.info("No monthly sales data available.")
                # CATEGORY-WISE SALES ANALYSIS

        st.markdown("---")
        st.markdown("### 👗 Category-wise Sales")

                # BUSINESS INSIGHTS

        st.markdown("---")
        st.markdown("### 💡 Business Insights")

        cursor.execute("""
            SELECT Category, SUM(TotalAmount) AS Sales
            FROM sales_transactions
            GROUP BY Category
            ORDER BY Sales DESC
            LIMIT 1
        """)

        top_category = cursor.fetchone()

        cursor.execute("""
            SELECT COUNT(*)
            FROM inventory
            WHERE CurrentStock <= ReorderLevel
        """)

        low_stock_count = cursor.fetchone()[0]

        cursor.execute("""
            SELECT SalesExecutive, SUM(Profit) AS TotalProfit
            FROM sales_transactions
            GROUP BY SalesExecutive
            ORDER BY TotalProfit DESC
            LIMIT 1
        """)

        top_executive = cursor.fetchone()

        col1, col2, col3 = st.columns(3)

        with col1:
            st.info(
                f"🏆 Best-Selling Category: {top_category[0]}"
                if top_category else "No sales data available"
            )

        with col2:
            st.warning(f"📦 Low Stock Products: {low_stock_count}")

        with col3:
            st.success(
                f"⭐ Top Profit Executive: {top_executive[0]}"
                if top_executive else "No sales data available"
            )

        cursor.execute("""
            SELECT Category, SUM(TotalAmount) AS CategorySales
            FROM sales_transactions
            GROUP BY Category
            ORDER BY CategorySales DESC
        """)

        category_sales = cursor.fetchall()

        if category_sales:
            category_df = pd.DataFrame(
                category_sales,
                columns=["Category", "Sales"]
            )

            category_df = category_df.set_index("Category")

            st.bar_chart(
                category_df,
                horizontal=True,
                height=300,
                use_container_width=True
            )
        else:
            st.info("No category sales data available.")


                # PAYMENT MODE ANALYSIS

        st.markdown("---")
        st.markdown("### 💳 Payment Mode Analysis")

        cursor.execute("""
            SELECT PaymentMode, COUNT(*) AS Transactions,
                   SUM(TotalAmount) AS Revenue
            FROM sales_transactions
            GROUP BY PaymentMode
            ORDER BY Revenue DESC
        """)

        payment_data = cursor.fetchall()

        if payment_data:
            payment_df = pd.DataFrame(
                payment_data,
                columns=["Payment Mode", "Transactions", "Revenue"]
            )

            col1, col2 = st.columns(2)

            with col1:
                st.bar_chart(
                    payment_df.set_index("Payment Mode")[["Transactions"]],
                    height=300,
                    use_container_width=True
                )

            with col2:
                st.bar_chart(
                    payment_df.set_index("Payment Mode")[["Revenue"]],
                    height=300,
                    use_container_width=True
                )
        else:
            st.info("No payment data available.")

                # TOP 5 BEST-SELLING PRODUCTS

        st.markdown("---")
        st.markdown("### 🏆 Top 5 Best-Selling Products")

        cursor.execute("""
            SELECT p.ProductName,
                   SUM(s.TotalAmount) AS TotalSales
            FROM sales_transactions s
            JOIN products p
                ON s.ProductID = p.ProductID
            GROUP BY p.ProductID, p.ProductName
            ORDER BY TotalSales DESC
            LIMIT 5
        """)

        top_products = cursor.fetchall()

        if top_products:
            products_df = pd.DataFrame(
                top_products,
                columns=["Product", "Sales"]
            )

            products_df = products_df.set_index("Product")

            st.bar_chart(
                products_df,
                horizontal=True,
                height=300,
                use_container_width=True
            )
        else:
            st.info("No product sales data available.")

        # Total Sales Revenue
        cursor.execute("""
            SELECT COALESCE(SUM(TotalAmount), 0)
            FROM sales_transactions
        """)
        total_revenue = cursor.fetchone()[0]

        # Total Profit
        cursor.execute("""
            SELECT COALESCE(SUM(Profit), 0)
            FROM sales_transactions
        """)
        total_profit = cursor.fetchone()[0]

        # Total Customers
        cursor.execute("SELECT COUNT(*) FROM customers")
        total_customers = cursor.fetchone()[0]

        # Total Products
        cursor.execute("SELECT COUNT(*) FROM products")
        total_products = cursor.fetchone()[0]

        # Total Inventory Stock
        cursor.execute("""
            SELECT COALESCE(SUM(CurrentStock), 0)
            FROM inventory
        """)
        total_stock = cursor.fetchone()[0]

        # Total Purchase Amount
        cursor.execute("""
            SELECT COALESCE(SUM(TotalAmount), 0)
            FROM purchases
        """)
        total_purchases = cursor.fetchone()[0]

        # First row of KPIs
        col1, col2, col3 = st.columns(3)

        col1.metric("💰 Total Sales", f"₹{total_revenue:,.2f}")
        col2.metric("📈 Total Profit", f"₹{total_profit:,.2f}")
        col3.metric("👥 Total Customers", total_customers)

        # Second row of KPIs
        col4, col5, col6 = st.columns(3)

        col4.metric("👗 Total Products", total_products)
        col5.metric("📦 Total Stock Units", total_stock)
        col6.metric("🛒 Total Purchases", f"₹{total_purchases:,.2f}")

                # CUSTOMER MANAGEMENT MODULE
        if page == "Customer Management":

            st.markdown("---")
            st.header("👥 Customer Management")

            # CREATE CUSTOMER
            st.subheader("➕ Add New Customer")

            with st.form("add_customer_form"):

                new_id = st.text_input("Customer ID")
                new_name = st.text_input("Customer Name")
                new_phone = st.text_input("Phone Number")
                new_city = st.text_input("City")
                new_date = st.date_input("Join Date")

                add_button = st.form_submit_button("Add Customer")

                if add_button:

                    if new_id and new_name:

                        try:
                            cursor.execute(
                                """
                                INSERT INTO customers
                                (CustomerID, CustomerName, Phone, City, JoinDate)
                                VALUES (%s, %s, %s, %s, %s)
                                """,
                                (new_id, new_name, new_phone, new_city, new_date)
                            )

                            connection.commit()
                            st.success("Customer added successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            st.error(f"Unable to add customer: {error}")

                    else:
                        st.warning("Customer ID and Name are required.")

            st.markdown("---")

            # READ CUSTOMERS
            st.subheader("📋 Customer Records")

            cursor.execute("""
                SELECT CustomerID, CustomerName, Phone, City, JoinDate
                FROM customers
            """)

            records = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in records],
                use_container_width=True
            )

            st.markdown("---")

            # UPDATE CUSTOMER
            st.subheader("✏️ Update Customer")

            cursor.execute("SELECT CustomerID FROM customers")
            customer_ids = [row[0] for row in cursor.fetchall()]

            if customer_ids:

                selected_id = st.selectbox(
                    "Select Customer ID to Update",
                    customer_ids
                )

                cursor.execute(
                    """
                    SELECT CustomerName, Phone, City
                    FROM customers
                    WHERE CustomerID = %s
                    """,
                    (selected_id,)
                )

                customer = cursor.fetchone()

                with st.form("update_customer_form"):

                    updated_name = st.text_input(
                        "Customer Name",
                        value=customer[0]
                    )

                    updated_phone = st.text_input(
                        "Phone Number",
                        value=customer[1] or ""
                    )

                    updated_city = st.text_input(
                        "City",
                        value=customer[2] or ""
                    )

                    update_button = st.form_submit_button("Update Customer")

                    if update_button:

                        cursor.execute(
                            """
                            UPDATE customers
                            SET CustomerName = %s, Phone = %s, City = %s
                            WHERE CustomerID = %s
                            """,
                            (updated_name, updated_phone, updated_city, selected_id)
                        )

                        connection.commit()
                        st.success("Customer updated successfully!")
                        st.rerun()

            st.markdown("---")

            # DELETE CUSTOMER
            st.subheader("🗑️ Delete Customer")

            delete_id = st.selectbox(
                "Select Customer ID to Delete",
                customer_ids,
                key="delete_customer"
            ) if customer_ids else None

            if delete_id:

                if st.button("Delete Customer", type="primary"):

                    try:
                        cursor.execute(
                            "DELETE FROM customers WHERE CustomerID = %s",
                            (delete_id,)
                        )

                        connection.commit()
                        st.success("Customer deleted successfully!")
                        st.rerun()

                    except mysql.connector.Error as error:
                        st.error(
                            f"Cannot delete this customer: {error}. "
                            "The customer may have existing sales records."
                        )
            # PRODUCT MANAGEMENT MODULE
        if page == "Product Management":

            st.markdown("---")
            st.header("👗 Product Management")

            cursor.execute("SELECT Category FROM categories")
            categories = [row[0] for row in cursor.fetchall()]

            # ADD PRODUCT
            st.subheader("➕ Add New Product")

            with st.form("add_product_form"):

                product_id = st.text_input("Product ID")
                product_name = st.text_input("Product Name")
                category = st.selectbox("Category", categories)

                cost_price = st.number_input("Cost Price", min_value=0.0)
                selling_price = st.number_input("Selling Price", min_value=0.0)
                margin = st.number_input("Margin Percentage", min_value=0.0)

                add_product = st.form_submit_button("Add Product")

                if add_product:

                    if product_id and product_name:

                        try:
                            cursor.execute("""
                                INSERT INTO products
                                (ProductID, ProductName, Category,
                                 CostPrice, SellingPrice, MarginPct)
                                VALUES (%s, %s, %s, %s, %s, %s)
                            """, (
                                product_id, product_name, category,
                                cost_price, selling_price, margin
                            ))

                            connection.commit()
                            st.success("Product added successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            st.error(f"Error: {error}")

                    else:
                        st.warning("Product ID and Product Name are required.")

            st.markdown("---")

            # VIEW PRODUCTS
            st.subheader("📋 Product Records")

            cursor.execute("SELECT * FROM products")
            records = cursor.fetchall()

            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in records],
                use_container_width=True
            )

            st.markdown("---")

            # UPDATE PRODUCT
            st.subheader("✏️ Update Product")

            cursor.execute("SELECT ProductID FROM products")
            product_ids = [row[0] for row in cursor.fetchall()]

            if product_ids:

                selected_product = st.selectbox(
                    "Select Product ID",
                    product_ids
                )

                cursor.execute("""
                    SELECT ProductName, Category, CostPrice,
                           SellingPrice, MarginPct
                    FROM products
                    WHERE ProductID = %s
                """, (selected_product,))

                product = cursor.fetchone()

                with st.form("update_product_form"):

                    updated_name = st.text_input(
                        "Product Name",
                        value=product[0]
                    )

                    updated_category = st.selectbox(
                        "Category",
                        categories,
                        index=categories.index(product[1])
                    )

                    updated_cost = st.number_input(
                        "Cost Price",
                        min_value=0.0,
                        value=float(product[2] or 0)
                    )

                    updated_selling = st.number_input(
                        "Selling Price",
                        min_value=0.0,
                        value=float(product[3] or 0)
                    )

                    updated_margin = st.number_input(
                        "Margin Percentage",
                        min_value=0.0,
                        value=float(product[4] or 0)
                    )

                    update_product = st.form_submit_button("Update Product")

                    if update_product:

                        cursor.execute("""
                            UPDATE products
                            SET ProductName=%s, Category=%s,
                                CostPrice=%s, SellingPrice=%s,
                                MarginPct=%s
                            WHERE ProductID=%s
                        """, (
                            updated_name, updated_category,
                            updated_cost, updated_selling,
                            updated_margin, selected_product
                        ))

                        connection.commit()
                        st.success("Product updated successfully!")
                        st.rerun()

            st.markdown("---")

            # DELETE PRODUCT
            st.subheader("🗑️ Delete Product")

            delete_product = st.selectbox(
                "Select Product to Delete",
                product_ids,
                key="delete_product"
            ) if product_ids else None

            if delete_product:

                if st.button("Delete Product", type="primary"):

                    try:
                        cursor.execute(
                            "DELETE FROM products WHERE ProductID=%s",
                            (delete_product,)
                        )

                        connection.commit()
                        st.success("Product deleted successfully!")
                        st.rerun()

                    except mysql.connector.Error as error:
                        st.error(f"Cannot delete product: {error}")
            # INVENTORY MANAGEMENT MODULE
        if page == "Inventory Management":

            st.markdown("---")
            st.header("📦 Inventory Management")

            # INVENTORY SUMMARY
            cursor.execute("""
                SELECT
                    COUNT(*) AS TotalProducts,
                    COALESCE(SUM(CurrentStock), 0) AS TotalStock,
                    COALESCE(SUM(StockValue), 0) AS TotalValue,
                    SUM(CASE WHEN CurrentStock <= ReorderLevel
                        AND CurrentStock > 0 THEN 1 ELSE 0 END) AS LowStock,
                    SUM(CASE WHEN CurrentStock = 0
                        THEN 1 ELSE 0 END) AS OutOfStock
                FROM inventory
            """)

            summary = cursor.fetchone()

            col1, col2, col3, col4, col5 = st.columns(5)

            col1.metric("Total Products", summary[0])
            col2.metric("Total Stock", summary[1])
            col3.metric("Stock Value", f"₹{summary[2]:,.0f}")
            col4.metric("Low Stock", summary[3] or 0)
            col5.metric("Out of Stock", summary[4] or 0)

            st.markdown("---")

            # VIEW INVENTORY
            st.subheader("📋 Inventory Records")

            cursor.execute("""
                SELECT ProductID, ProductName, Category,
                       CurrentStock, ReorderLevel, Status,
                       StockValue, PreferredSupplierID
                FROM inventory
            """)

            records = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in records],
                use_container_width=True
            )

            st.markdown("---")

            # LOW STOCK ALERT
            st.subheader("⚠️ Low Stock Alerts")

            cursor.execute("""
                SELECT ProductID, ProductName, CurrentStock, ReorderLevel
                FROM inventory
                WHERE CurrentStock <= ReorderLevel
                ORDER BY CurrentStock ASC
            """)

            low_stock = cursor.fetchall()

            if low_stock:
                st.warning(f"{len(low_stock)} products require stock attention.")
                st.dataframe(
                    low_stock,
                    column_config={
                        0: "Product ID",
                        1: "Product Name",
                        2: "Current Stock",
                        3: "Reorder Level"
                    },
                    use_container_width=True
                )
            else:
                st.success("All products have sufficient stock.")

            st.markdown("---")

            # UPDATE INVENTORY
            st.subheader("✏️ Update Stock")

            cursor.execute("SELECT ProductID FROM inventory")
            product_ids = [row[0] for row in cursor.fetchall()]

            if product_ids:

                selected_id = st.selectbox(
                    "Select Product ID",
                    product_ids
                )

                cursor.execute("""
                    SELECT CurrentStock, ReorderLevel
                    FROM inventory
                    WHERE ProductID = %s
                """, (selected_id,))

                stock = cursor.fetchone()

                with st.form("update_inventory_form"):

                    new_stock = st.number_input(
                        "New Stock Quantity",
                        min_value=0,
                        value=int(stock[0])
                    )

                    new_reorder = st.number_input(
                        "New Reorder Level",
                        min_value=0,
                        value=int(stock[1])
                    )

                    update_stock = st.form_submit_button("Update Inventory")

                    if update_stock:

                        status = (
                            "Out of Stock" if new_stock == 0
                            else "Low Stock" if new_stock <= new_reorder
                            else "In Stock"
                        )

                        cursor.execute("""
                            UPDATE inventory
                            SET CurrentStock = %s,
                                ReorderLevel = %s,
                                Status = %s
                            WHERE ProductID = %s
                        """, (
                            new_stock,
                            new_reorder,
                            status,
                            selected_id
                        ))

                        connection.commit()
                        st.success("Inventory updated successfully!")
                        st.rerun()

                # SALES MANAGEMENT MODULE
        if page == "Sales Management":

            st.markdown("---")
            st.header("💰 Sales Management")

            # SALES SUMMARY
            cursor.execute("""
                SELECT
                    COALESCE(SUM(TotalAmount), 0),
                    COALESCE(SUM(Profit), 0),
                    COUNT(*)
                FROM sales_transactions
            """)

            sales_summary = cursor.fetchone()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Sales Revenue", f"₹{sales_summary[0]:,.2f}")
            col2.metric("Total Profit", f"₹{sales_summary[1]:,.2f}")
            col3.metric("Total Transactions", sales_summary[2])

            st.markdown("---")

            # SALES FILTERS
            st.subheader("🔍 Filter Sales")

            filter_col1, filter_col2 = st.columns(2)

            filter_col1, filter_col2 = st.columns(2)

            with filter_col1:
                payment_mode = st.selectbox(
                    "Payment Mode",
                    ["All", "Cash", "UPI", "Card"]
                )

            with filter_col2:
                search_bill = st.text_input("Search Bill Number")

            query = """
                SELECT BillNo, Date, CustomerID, ProductID,
                       Category, Qty, TotalAmount, Profit,
                       SalesExecutive, PaymentMode
                FROM sales_transactions
                WHERE 1=1
            """

            parameters = []

            if payment_mode != "All":
                query += " AND PaymentMode = %s"
                parameters.append(payment_mode)

            if search_bill:
                query += " AND BillNo LIKE %s"
                parameters.append(f"%{search_bill}%")

            query += " ORDER BY Date DESC"

            cursor.execute(query, tuple(parameters))

            sales_records = cursor.fetchall()

            columns = [description[0] for description in cursor.description]

            st.subheader("📋 Sales Transactions")

            st.dataframe(
                [dict(zip(columns, row)) for row in sales_records],
                use_container_width=True
            )

            st.caption(f"Records displayed: {len(sales_records)}")
            st.markdown("---")
            st.subheader("➕ Add New Sales Transaction")

            with st.form("add_sales_form"):

                bill_no = st.text_input("Bill Number")

                cursor.execute("SELECT CustomerID FROM customers")
                customer_ids = [row[0] for row in cursor.fetchall()]

                cursor.execute("SELECT ProductID FROM products")
                product_ids = [row[0] for row in cursor.fetchall()]

                customer_id = st.selectbox("Customer", customer_ids)
                product_id = st.selectbox("Product", product_ids)

                quantity = st.number_input("Quantity", min_value=1, value=1)

                sales_date = st.date_input("Sales Date")

                sales_executive = st.text_input("Sales Executive")

                payment_mode = st.selectbox(
                    "Payment Mode",
                    ["Cash", "UPI", "Card"]
                )

                discount = st.number_input(
                    "Discount Percentage",
                    min_value=0.0,
                    max_value=100.0,
                    value=0.0
                )

                submit_sale = st.form_submit_button("Add Sale")

                if submit_sale:
                    cursor.execute(
                       "SELECT CurrentStock FROM inventory WHERE ProductID = %s",
                       (product_id,)
                    )              

                    stock_result = cursor.fetchone()

                    if stock_result is None:
                        st.error("This product was not found in inventory.")
                        st.stop()

                    available_stock = stock_result[0]

                    if quantity > available_stock:
                        st.error(f"Only {available_stock} units are available in stock.")
                        st.stop()


                    available_stock = cursor.fetchone()[0]

                    if quantity > available_stock:
                        st.error(
                            f"Only {available_stock} units are available in stock."
                        )
                        st.stop()

                    if bill_no and sales_executive:

                        cursor.execute("""
                            SELECT ProductName, Category,
                                   CostPrice, SellingPrice
                            FROM products
                            WHERE ProductID = %s
                        """, (product_id,))

                        product = cursor.fetchone()

                        product_name = product[0]
                        category = product[1]
                        cost_price = float(product[2])
                        selling_price = float(product[3])

                        effective_price = selling_price * (1 - discount / 100)

                        total_amount = effective_price * quantity
                        total_cost = cost_price * quantity
                        profit = total_amount - total_cost

                        cursor.execute("""
                            INSERT INTO sales_transactions
                            (BillNo, Date, CustomerID, ProductID,
                             Category, Qty, UnitPrice, DiscountPct,
                             EffectivePrice, TotalAmount, TotalCost,
                             Profit, SalesExecutive, PaymentMode)
                            VALUES (%s, %s, %s, %s, %s, %s, %s,
                                    %s, %s, %s, %s, %s, %s, %s)
                        """, (
                            bill_no, sales_date, customer_id,
                            product_id, category, quantity,
                            selling_price, discount, effective_price,
                            total_amount, total_cost, profit,
                            sales_executive, payment_mode
                        ))

                        # Reduce inventory after sale
                        cursor.execute("""
                            UPDATE inventory
                            SET CurrentStock = CurrentStock - %s
                            WHERE ProductID = %s
                        """, (quantity, product_id))

                        # Check updated stock
                        cursor.execute("""
                            SELECT CurrentStock, ReorderLevel
                            FROM inventory
                            WHERE ProductID = %s
                        """, (product_id,))

                        updated_stock = cursor.fetchone()

                        if updated_stock[0] == 0:
                            status = "Out of Stock"
                        elif updated_stock[0] <= updated_stock[1]:
                            status = "Low Stock"
                        else:
                            status = "In Stock"

                        cursor.execute("""
                            UPDATE inventory
                            SET Status = %s
                            WHERE ProductID = %s
                        """, (status, product_id))

                        connection.commit()

                        st.success("Sales transaction added successfully!")
                        st.rerun()

                else:
                        st.warning("Bill Number and Sales Executive are required.")

                
                            # PURCHASE MANAGEMENT MODULE
        if page == "Purchase Management":

            st.markdown("---")
            st.header("🛒 Purchase Management")

            # PURCHASE SUMMARY
            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(TotalAmount), 0)
                FROM purchases
            """)

            purchase_summary = cursor.fetchone()

            col1, col2 = st.columns(2)

            col1.metric("Total Purchase Orders", purchase_summary[0])
            col2.metric("Total Purchase Amount", f"₹{purchase_summary[1]:,.2f}")

            st.markdown("---")

            # PURCHASE RECORDS
            st.subheader("📋 Purchase Records")

            cursor.execute("""
                SELECT PONumber, Date, SupplierID, ProductID,
                       Category, Qty, UnitCost, TotalAmount, Status
                FROM purchases
                ORDER BY Date DESC
            """)

            records = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in records],
                use_container_width=True
            )

            st.markdown("---")

            # ADD PURCHASE
            st.subheader("➕ Add New Purchase")

            cursor.execute("SELECT SupplierID FROM suppliers")
            supplier_ids = [row[0] for row in cursor.fetchall()]

            cursor.execute("""
                SELECT ProductID, ProductName, Category, CostPrice
                FROM products
            """)
            products = cursor.fetchall()

            with st.form("add_purchase_form"):

                po_number = st.text_input("Purchase Order Number")

                supplier_id = st.selectbox("Supplier", supplier_ids)

                product_options = {
                    f"{p[0]} - {p[1]}": p for p in products
                }

                selected_product = st.selectbox(
                    "Product",
                    list(product_options.keys())
                )

                selected = product_options[selected_product]

                product_id = selected[0]
                category = selected[2]
                unit_cost = float(selected[3])

                purchase_qty = st.number_input(
                    "Quantity",
                    min_value=1,
                    value=1
                )

                purchase_date = st.date_input("Purchase Date")

                purchase_status = st.selectbox(
                    "Status",
                    ["Pending", "Received", "Cancelled"]
                )

                total_amount = unit_cost * purchase_qty

                st.write(f"Total Purchase Amount: ₹{total_amount:,.2f}")

                submit_purchase = st.form_submit_button("Add Purchase")

                if submit_purchase:

                    if po_number:

                        try:
                            cursor.execute("""
                                INSERT INTO purchases
                                (PONumber, Date, SupplierID, ProductID,
                                 Category, Qty, UnitCost, TotalAmount, Status)
                                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                            """, (
                                po_number, purchase_date, supplier_id,
                                product_id, category, purchase_qty,
                                unit_cost, total_amount, purchase_status
                            ))

                                                        # Update inventory when purchase is received
                            if purchase_status == "Received":

                                cursor.execute("""
                                    SELECT CurrentStock, ReorderLevel
                                    FROM inventory
                                    WHERE ProductID = %s
                                """, (product_id,))

                                inventory_result = cursor.fetchone()

                                if inventory_result is None:
                                    raise Exception("Product not found in inventory.")

                                new_stock = inventory_result[0] + purchase_qty
                                reorder_level = inventory_result[1]

                                if new_stock == 0:
                                    new_status = "Out of Stock"
                                elif new_stock <= reorder_level:
                                    new_status = "Low Stock"
                                else:
                                    new_status = "In Stock"

                                cursor.execute("""
                                    UPDATE inventory
                                    SET CurrentStock = %s,
                                        Status = %s
                                    WHERE ProductID = %s
                                """, (new_stock, new_status, product_id))

                            connection.commit()

                            st.success("Purchase order added successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            connection.rollback()
                            st.error(f"Unable to add purchase: {error}")

                    else:
                        st.warning("Purchase Order Number is required.")

                            # SUPPLIER MANAGEMENT MODULE
        if page == "Supplier Management":

            st.markdown("---")
            st.header("🏭 Supplier Management")
            st.caption("Manage your Bedi Cloth House suppliers.")

            # SUPPLIER SUMMARY
            cursor.execute("""
                SELECT COUNT(*) FROM suppliers
            """)

            total_suppliers = cursor.fetchone()[0]

            col1, col2 = st.columns(2)

            col1.metric("Total Suppliers", total_suppliers)

            cursor.execute("""
                SELECT COUNT(DISTINCT City) FROM suppliers
            """)

            total_cities = cursor.fetchone()[0]

            col2.metric("Supplier Cities", total_cities)

            st.markdown("---")

            # VIEW SUPPLIERS
            st.subheader("📋 All Supplier Records")

            cursor.execute("""
                SELECT SupplierID, SupplierName,
                       CategorySupplied, City, ContactNo
                FROM suppliers
                ORDER BY SupplierName
            """)

            supplier_records = cursor.fetchall()

            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in supplier_records],
                use_container_width=True
            )

            st.markdown("---")

            # ADD SUPPLIER
            st.subheader("➕ Add New Supplier")

            cursor.execute("""
                SELECT Category FROM categories
            """)

            categories = [row[0] for row in cursor.fetchall()]

            with st.form("add_supplier_form"):

                supplier_id = st.text_input("Supplier ID")

                supplier_name = st.text_input("Supplier Name")

                category_supplied = st.selectbox(
                    "Category Supplied",
                    categories
                )

                city = st.text_input("City")

                contact_no = st.text_input("Contact Number")

                add_supplier = st.form_submit_button("Add Supplier")

                if add_supplier:

                    if supplier_id and supplier_name and city:

                        try:
                            cursor.execute("""
                                INSERT INTO suppliers
                                (SupplierID, SupplierName,
                                 CategorySupplied, City, ContactNo)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                supplier_id,
                                supplier_name,
                                category_supplied,
                                city,
                                contact_no
                            ))

                            connection.commit()

                            st.success("Supplier added successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            connection.rollback()
                            st.error(f"Unable to add supplier: {error}")

                    else:
                        st.warning("Please enter Supplier ID, Supplier Name and City.")

            st.markdown("---")

            # UPDATE SUPPLIER
            st.subheader("✏️ Update Supplier Details")

            cursor.execute("""
                SELECT SupplierID FROM suppliers
            """)

            supplier_list = [row[0] for row in cursor.fetchall()]

            if supplier_list:

                selected_supplier = st.selectbox(
                    "Select Supplier ID to Update",
                    supplier_list
                )

                cursor.execute("""
                    SELECT SupplierName, CategorySupplied, City, ContactNo
                    FROM suppliers
                    WHERE SupplierID = %s
                """, (selected_supplier,))

                supplier_details = cursor.fetchone()

                with st.form("update_supplier_form"):

                    updated_name = st.text_input(
                        "Supplier Name",
                        value=supplier_details[0] or ""
                    )

                    updated_category = st.selectbox(
                        "Category Supplied",
                        categories,
                        index=categories.index(supplier_details[1])
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
                                SET SupplierName = %s,
                                    CategorySupplied = %s,
                                    City = %s,
                                    ContactNo = %s
                                WHERE SupplierID = %s
                            """, (
                                updated_name,
                                updated_category,
                                updated_city,
                                updated_contact,
                                selected_supplier
                            ))

                            connection.commit()

                            st.success("Supplier updated successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            connection.rollback()
                            st.error(f"Unable to update supplier: {error}")

            st.markdown("---")

            # DELETE SUPPLIER
            st.subheader("🗑️ Delete Supplier")

            if supplier_list:

                delete_supplier_id = st.selectbox(
                    "Select Supplier ID to Delete",
                    supplier_list,
                    key="delete_supplier"
                )

                if st.button("Delete Supplier"):

                    try:
                        cursor.execute("""
                            DELETE FROM suppliers
                            WHERE SupplierID = %s
                        """, (delete_supplier_id,))

                        connection.commit()

                        st.success("Supplier deleted successfully!")
                        st.rerun()

                    except mysql.connector.Error as error:
                        connection.rollback()
                        st.error(
                            "This supplier cannot be deleted because "
                            "it is linked to existing inventory or purchase records."
                        )
                        # SALES TARGETS MANAGEMENT MODULE
        if page == "Sales Targets Management":

            st.markdown("---")
            st.header("🎯 Sales Targets Management")

            # SUMMARY
            cursor.execute("""
                SELECT
                    COUNT(*),
                    COALESCE(SUM(SalesTarget), 0),
                    COALESCE(SUM(AchievedSales), 0)
                FROM sales_targets
            """)

            target_summary = cursor.fetchone()

            col1, col2, col3 = st.columns(3)

            col1.metric("Total Target Records", target_summary[0])
            col2.metric("Total Sales Target", f"₹{target_summary[1]:,.2f}")
            col3.metric("Total Achieved Sales", f"₹{target_summary[2]:,.2f}")

            st.markdown("---")

            # VIEW RECORDS
            st.subheader("📋 Sales Target Records")

            cursor.execute("""
                SELECT SalesExecutive, Month, SalesTarget,
                       AchievedSales, AchievementPct
                FROM sales_targets
                ORDER BY Month DESC, SalesExecutive
            """)

            target_records = cursor.fetchall()
            columns = [description[0] for description in cursor.description]

            st.dataframe(
                [dict(zip(columns, row)) for row in target_records],
                use_container_width=True
            )

            st.markdown("---")

            # ADD TARGET
            st.subheader("➕ Add New Sales Target")

            cursor.execute("""
                SELECT DISTINCT SalesExecutive
                FROM sales_transactions
                ORDER BY SalesExecutive
            """)

            executives = [row[0] for row in cursor.fetchall()]

            with st.form("add_target_form"):

                executive = st.selectbox(
                    "Sales Executive",
                    executives
                )

                month = st.text_input(
                    "Month",
                    placeholder="Example: Jan-2027"
                )

                target_amount = st.number_input(
                    "Sales Target (₹)",
                    min_value=1.0,
                    value=10000.0
                )

                achieved_amount = st.number_input(
                    "Achieved Sales (₹)",
                    min_value=0.0,
                    value=0.0
                )

                add_target = st.form_submit_button("Add Sales Target")

                if add_target:

                    if month.strip():

                        achievement = (
                            achieved_amount / target_amount
                        ) * 100

                        try:
                            cursor.execute("""
                                INSERT INTO sales_targets
                                (SalesExecutive, Month, SalesTarget,
                                 AchievedSales, AchievementPct)
                                VALUES (%s, %s, %s, %s, %s)
                            """, (
                                executive,
                                month.strip(),
                                target_amount,
                                achieved_amount,
                                achievement
                            ))

                            connection.commit()

                            st.success("Sales target added successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            connection.rollback()
                            st.error(f"Unable to add target: {error}")

                    else:
                        st.warning("Please enter the month.")

            st.markdown("---")

            # UPDATE TARGET
            st.subheader("✏️ Update Sales Target")

            cursor.execute("""
                SELECT SalesExecutive, Month
                FROM sales_targets
                ORDER BY Month DESC
            """)

            target_options = cursor.fetchall()

            if target_options:

                selected_target = st.selectbox(
                    "Select Target Record",
                    target_options,
                    format_func=lambda x: f"{x[0]} - {x[1]}"
                )

                cursor.execute("""
                    SELECT SalesTarget, AchievedSales
                    FROM sales_targets
                    WHERE SalesExecutive = %s AND Month = %s
                """, selected_target)

                existing_target = cursor.fetchone()

                with st.form("update_target_form"):

                    updated_target = st.number_input(
                        "Updated Sales Target (₹)",
                        min_value=1.0,
                        value=float(existing_target[0])
                    )

                    updated_achieved = st.number_input(
                        "Updated Achieved Sales (₹)",
                        min_value=0.0,
                        value=float(existing_target[1])
                    )

                    update_target = st.form_submit_button(
                        "Update Sales Target"
                    )

                    if update_target:

                        achievement = (
                            updated_achieved / updated_target
                        ) * 100

                        try:
                            cursor.execute("""
                                UPDATE sales_targets
                                SET SalesTarget = %s,
                                    AchievedSales = %s,
                                    AchievementPct = %s
                                WHERE SalesExecutive = %s
                                AND Month = %s
                            """, (
                                updated_target,
                                updated_achieved,
                                achievement,
                                selected_target[0],
                                selected_target[1]
                            ))

                            connection.commit()

                            st.success("Sales target updated successfully!")
                            st.rerun()

                        except mysql.connector.Error as error:
                            connection.rollback()
                            st.error(f"Unable to update target: {error}")

            st.markdown("---")

            # DELETE TARGET
            st.subheader("🗑️ Delete Sales Target")

            if target_options:

                delete_target = st.selectbox(
                    "Select Target to Delete",
                    target_options,
                    format_func=lambda x: f"{x[0]} - {x[1]}",
                    key="delete_target"
                )

                if st.button("Delete Sales Target"):

                    try:
                        cursor.execute("""
                            DELETE FROM sales_targets
                            WHERE SalesExecutive = %s AND Month = %s
                        """, delete_target)

                        connection.commit()

                        st.success("Sales target deleted successfully!")
                        st.rerun()

                    except mysql.connector.Error as error:
                        connection.rollback()
                        st.error(f"Unable to delete target: {error}")

        cursor.close()
        connection.close()

    except mysql.connector.Error as error:
        st.sidebar.error("Database Connection Failed")
        st.error(f"Error: {error}")

else:
    st.info("Enter your MySQL password in the left sidebar to connect.")

st.markdown("---")

st.caption("© 2026 Bedi Cloth House | Management System")