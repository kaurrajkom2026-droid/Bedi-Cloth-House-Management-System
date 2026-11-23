import pandas as pd
import mysql.connector
from getpass import getpass
from datetime import date

print("BEDI CLOTH HOUSE - ONLINE DATABASE IMPORT")
print("------------------------------------------")

# Aiven database password
password = input("Enter your Aiven MySQL password: ")

try:

    # Connect to Aiven MySQL
    connection = mysql.connector.connect(
        host="mysql-304e532-kaurrajkom2026-cb83.d.aivencloud.com",
        port=22295,
        user="bedi_app",
        password=password,
        database="defaultdb",
        ssl_disabled=False
    )

    cursor = connection.cursor()

    print("\nConnected to Aiven successfully!")

    # Create database tables
    tables = [

        """
        CREATE TABLE IF NOT EXISTS categories (
            CategoryID INT AUTO_INCREMENT PRIMARY KEY,
            Category VARCHAR(100) NOT NULL UNIQUE
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS products (
            ProductID VARCHAR(20) PRIMARY KEY,
            ProductName VARCHAR(150) NOT NULL,
            Category VARCHAR(100),
            CostPrice DECIMAL(10,2),
            SellingPrice DECIMAL(10,2),
            MarginPct DECIMAL(5,2),
            FOREIGN KEY (Category) REFERENCES categories(Category)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS customers (
            CustomerID VARCHAR(20) PRIMARY KEY,
            CustomerName VARCHAR(100) NOT NULL,
            Phone VARCHAR(20),
            City VARCHAR(100),
            JoinDate DATE
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS suppliers (
            SupplierID VARCHAR(20) PRIMARY KEY,
            SupplierName VARCHAR(150) NOT NULL,
            CategorySupplied VARCHAR(100),
            City VARCHAR(100),
            ContactNo VARCHAR(20),
            FOREIGN KEY (CategorySupplied)
            REFERENCES categories(Category)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS sales_targets (
            SalesExecutive VARCHAR(100),
            Month VARCHAR(20),
            SalesTarget DECIMAL(12,2),
            AchievedSales DECIMAL(12,2),
            AchievementPct DECIMAL(5,2),
            PRIMARY KEY (SalesExecutive, Month)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS sales_transactions (
            BillNo VARCHAR(30) PRIMARY KEY,
            Date DATE,
            CustomerID VARCHAR(20),
            ProductID VARCHAR(20),
            Category VARCHAR(100),
            Qty INT,
            UnitPrice DECIMAL(10,2),
            DiscountPct DECIMAL(5,2),
            EffectivePrice DECIMAL(10,2),
            TotalAmount DECIMAL(12,2),
            TotalCost DECIMAL(12,2),
            Profit DECIMAL(12,2),
            SalesExecutive VARCHAR(100),
            PaymentMode VARCHAR(50),
            FOREIGN KEY (CustomerID) REFERENCES customers(CustomerID),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID),
            FOREIGN KEY (Category) REFERENCES categories(Category)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS inventory (
            ProductID VARCHAR(20) PRIMARY KEY,
            ProductName VARCHAR(150),
            Category VARCHAR(100),
            CurrentStock INT,
            ReorderLevel INT,
            Status VARCHAR(50),
            StockValue DECIMAL(12,2),
            PreferredSupplierID VARCHAR(20),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID),
            FOREIGN KEY (Category) REFERENCES categories(Category),
            FOREIGN KEY (PreferredSupplierID)
            REFERENCES suppliers(SupplierID)
        )
        """,

        """
        CREATE TABLE IF NOT EXISTS purchases (
            PONumber VARCHAR(30) PRIMARY KEY,
            Date DATE,
            SupplierID VARCHAR(20),
            ProductID VARCHAR(20),
            Category VARCHAR(100),
            Qty INT,
            UnitCost DECIMAL(10,2),
            TotalAmount DECIMAL(12,2),
            Status VARCHAR(50),
            FOREIGN KEY (SupplierID) REFERENCES suppliers(SupplierID),
            FOREIGN KEY (ProductID) REFERENCES products(ProductID),
            FOREIGN KEY (Category) REFERENCES categories(Category)
        )
        """
    ]

    for table in tables:
        cursor.execute(table)

    connection.commit()

    print("All 8 tables created or verified successfully!")

    # Check that tables are empty before importing
    table_names = [
        "categories",
        "products",
        "customers",
        "suppliers",
        "sales_targets",
        "sales_transactions",
        "inventory",
        "purchases"
    ]

    for table_name in table_names:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        if cursor.fetchone()[0] > 0:
            raise Exception(
                f"{table_name} already contains records. "
                "Import stopped to prevent duplicate data."
            )

    # Read Excel workbook
    file_path = "Bedi_Cloth_House_Dataset_Updated.xlsx"
    excel = pd.ExcelFile(file_path)

    print("\nExcel workbook loaded successfully!")

    # Clean Excel values
    def clean_value(value):

        if pd.isna(value):
            return None

        if isinstance(value, pd.Timestamp):
            return value.date()

        if hasattr(value, "item"):
            return value.item()

        return value

    # Insert Excel data into MySQL
    def insert_data(sheet_name, table_name, columns, rename=None):

        df = pd.read_excel(excel, sheet_name=sheet_name)

        if rename:
            df = df.rename(columns=rename)

        df = df[columns]

        placeholders = ", ".join(["%s"] * len(columns))
        column_names = ", ".join(columns)

        query = f"""
            INSERT INTO {table_name} ({column_names})
            VALUES ({placeholders})
        """

        records = [
            tuple(clean_value(value) for value in row)
            for row in df.itertuples(index=False, name=None)
        ]

        cursor.executemany(query, records)

        print(f"{table_name}: {len(records)} records imported")

    # Import in foreign-key order
    insert_data(
        "Categories",
        "categories",
        ["Category"]
    )

    insert_data(
        "Products",
        "products",
        ["ProductID", "ProductName", "Category",
         "CostPrice", "SellingPrice", "MarginPct"],
        {"Margin%": "MarginPct"}
    )

    insert_data(
        "Customers",
        "customers",
        ["CustomerID", "CustomerName", "Phone",
         "City", "JoinDate"]
    )

    insert_data(
        "Suppliers",
        "suppliers",
        ["SupplierID", "SupplierName", "CategorySupplied",
         "City", "ContactNo"]
    )

    insert_data(
        "Sales Targets",
        "sales_targets",
        ["SalesExecutive", "Month", "SalesTarget",
         "AchievedSales", "AchievementPct"]
    )

    insert_data(
        "Sales Transactions",
        "sales_transactions",
        ["BillNo", "Date", "CustomerID", "ProductID",
         "Category", "Qty", "UnitPrice", "DiscountPct",
         "EffectivePrice", "TotalAmount", "TotalCost",
         "Profit", "SalesExecutive", "PaymentMode"]
    )

    insert_data(
        "Inventory",
        "inventory",
        ["ProductID", "ProductName", "Category",
         "CurrentStock", "ReorderLevel", "Status",
         "StockValue", "PreferredSupplierID"]
    )

    insert_data(
        "Purchases",
        "purchases",
        ["PONumber", "Date", "SupplierID", "ProductID",
         "Category", "Qty", "UnitCost", "TotalAmount",
         "Status"]
    )

    connection.commit()

    print("\n------------------------------------------")
    print("DATA IMPORT COMPLETED SUCCESSFULLY!")
    print("------------------------------------------")

    # Verify imported records
    total_records = 0

    for table_name in table_names:

        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]

        total_records += count

        print(f"{table_name}: {count} records")

    print("------------------------------------------")
    print("TOTAL RECORDS:", total_records)
    print("------------------------------------------")

    cursor.close()
    connection.close()

    print("\nAiven database connection closed.")

except Exception as error:

    print("\nIMPORT FAILED!")
    print("Error:", error)

    try:
        connection.rollback()
        cursor.close()
        connection.close()
    except:
        pass