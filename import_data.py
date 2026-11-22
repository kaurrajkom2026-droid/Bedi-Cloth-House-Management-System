import pandas as pd
import mysql.connector

# Connect to MySQL
password = input("Enter your MySQL password: ")

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password=password,
    database="bedi_cloth_house"
)

cursor = connection.cursor()

# Excel file name
file_path = "Bedi_Cloth_House_Dataset_Updated.xlsx"

# Read Excel workbook
excel = pd.ExcelFile(file_path)


# Convert Excel values into MySQL-friendly values
def clean_value(value):
    if pd.isna(value):
        return None

    if isinstance(value, pd.Timestamp):
        return value.date()

    if hasattr(value, "item"):
        return value.item()

    return value


# Insert data into a MySQL table
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

    print(f"{table_name}: {len(records)} records inserted")


# Import data in foreign-key order
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

print("\nSUCCESS! All Excel data has been imported into MySQL.")

cursor.close()
connection.close()