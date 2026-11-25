# ====================
# ORDER INSIGHTS
# ====================

# Import Libraries

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Load the Dataset

df = pd.read_csv("data/orders_raw.csv")

# Display first five rows

print("First Five Rows: ")
print(df.head())

# Display the number of rows and columns

print("\nDataset Shape: ")
print(df.shape)

# Display all Column Names

print("\nColumn Names: ")
print(df.columns)

# Display the Data types of each column

print("\nData Types: ")
print(df.dtypes)

# Check the number of missing values in each column

print("\nMissingValues: ")
print(df.isna().sum())

# Count the duplicate rows in the dataset

print("\nDuplicate Rows: ")
print(df.duplicated().sum())


# Create a cleaning function

def clean_orders(df):

# Create a copy of the original dataset

    clean = df.copy()

# Remove extra spaces and standardize capitalization

    clean["region"] = clean["region"].str.strip().str.title()
    clean["category"] = clean["category"].str.strip().str.title()

# Convert order_date column into datetime format

    clean["order_date"] = pd.to_datetime(
        clean["order_date"], errors="coerce"
    )

# Convert quantity, unit_price and order_value into numeric values

    numeric_columns = ["quantity", "unit_price", "order_value"]

    for col in numeric_columns:
        clean[col] = pd.to_numeric(clean[col], errors="coerce")

# Remove duplicate rows

    clean = clean.drop_duplicates()

# Define essential columns required for an order

    essential_columns = [
        "order_id",
        "order_date",
        "region",
        "category",
        "quantity",
        "unit_price",
        "order_value",    
        "status",
    ]

# Remove records with missing values in essential columns

    clean = clean.dropna(subset=essential_columns)

# Keep only records with positive values

    clean = clean[
        (clean["quantity"] > 0) &
        (clean["unit_price"] > 0) &
        (clean["order_value"] > 0)
      ]


    return clean.reset_index(drop=True)

# Test the function using the original dataset

cleaned_df = clean_orders(df)

# Display unique regions after cleaning
print("\nUnique Regions: ")
print(cleaned_df["region"].unique())

# Display unique categories after cleaning
print("\nUnique Categories: ")
print(cleaned_df["category"].unique())


# Create a data quality report

# Create the output folder if it does not already exist

os.makedirs("output", exist_ok=True)

report = pd.DataFrame({
    "Metric": [
        "Rows Before Cleaning",
        "Rows After Cleaning",
        "Rows Removed"
    ],
    "Value": [
        len(df),
        len(cleaned_df),
        len(df) - len(cleaned_df)
    ]
})

# Save the data quality report as a CSV file

report.to_csv("output/data_quality_report.csv", index=False)

# Save the cleaned dataset as a CSV file

cleaned_df.to_csv("output/cleaned.csv", index = False)

print("\nData Quality Report: ")
print(report)


# Compare the shapes of raw and cleaned datasets

print("Raw Dataset Shape: ", df.shape)
print("Cleaned Dataset Shape: ", cleaned_df.shape)

# Check missing values after cleaning

print("\nMissing Values After Cleaning:")
print(cleaned_df.isna().sum())

# Check duplicate rows after cleaning

print("\nDuplicate Rows After Cleaning:")
print(cleaned_df.duplicated().sum())

# Calculate mean, median and standard deviation of order values

mean_value = cleaned_df["order_value"].mean()
median_value = cleaned_df["order_value"].median()
std_value = cleaned_df["order_value"].std()

# Display order value statistics

print("\nOrder Value Statistics: ")
print("Mean : ",mean_value)
print("Median : ", median_value)
print("Standard Deviation : ", std_value)


# Calculate order count, total sales and average sales for each region

sales_by_region = cleaned_df.groupby("region")["order_value"].agg(
    order_counts="count",
    total_sales="sum",
    avg_sales="mean"
)

# Display sales analysis by region

print("\nTotal Sales by Region: ")
print(sales_by_region)

# Count the number of orders in each category

category_counts = cleaned_df["category"].value_counts()

# Display category counts

print("\nOrders by Category: ")
print(category_counts)

# Create a cross-tabulation of region and category

region_category = pd.crosstab(
    cleaned_df["region"],
    cleaned_df["category"]
)

# Display region vs category analysis

print("\nRegion vs Category: ")
print(region_category)


# DATA VISUALIZATION

# HISTOGRAM - DISTRIBUTION OF ORDER VALUES

plt.figure(figsize=(8, 5))

sns.histplot(
    data=cleaned_df,
    x="order_value",
    bins=20,
    kde=True
)

plt.title("Distribution of Order Values")
plt.xlabel("Order Value")
plt.ylabel("Number of Orders")

plt.tight_layout()
plt.savefig("output/order_value_histogram.png")
plt.show()


# BAR CHART - TOTAL SALES BY REGION

sales_by_region = cleaned_df.groupby("region")["order_value"].sum()

plt.figure(figsize=(8, 5))

sns.barplot(
    x=sales_by_region.index,
    y=sales_by_region.values
)

plt.title("Total Sales by Region")
plt.xlabel("Region")
plt.ylabel("Total Sales")

plt.tight_layout()
plt.savefig("output/sales_by_region.png")
plt.show()


# SCATTER PLOT - ORDER VALUE VS DELIVERY DAYS

plt.figure(figsize=(8, 5))

sns.scatterplot(
    data=cleaned_df,
    x="delivery_days",
    y="order_value"
)

plt.title("Order Value vs Delivery Days")
plt.xlabel("Delivery Days")
plt.ylabel("Order Value")

plt.tight_layout()
plt.savefig("output/order_value_vs_delivery_days.png")
plt.show()





# DATA QUALITY ISSUES IDENTIFIED


# 1. Missing values in quantity, delivery_days and status columns.

# 2. Three duplicate rows found in the dataset.

# 3. Inconsistent capitalization and extra spaces
#    in region and category columns.