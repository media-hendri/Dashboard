import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

# Function to create top 10 product categories based on unique orders
def create_top_category(df):
    # Group by product_category_name and count unique orders
    top_product_category = df.groupby(by="product_category_name").order_id.nunique().sort_values(ascending=False).reset_index()
    top_product_category.columns = ['product_category_name', 'total_orders']  # Rename columns
    return top_product_category

# Load the datasets
merged_df = pd.read_csv("merged_df.csv")
products_order_item_df = pd.read_csv("products_order_item_df.csv")

# Streamlit App Title
st.title('E-Commerce Customer Reviews and Delivery Time Dashboard')

# Sidebar filters
st.sidebar.header('Filter Data')

# Create a list of product categories with "Semua" as the first option
categories = ["Semua"] + list(merged_df['product_category_name'].unique())
selected_category = st.sidebar.selectbox('Select Product Category', categories)

# Slider for delivery time filter
min_delivery_time = st.sidebar.slider('Minimum Delivery Time (Days)', int(merged_df['delivery_time_days'].min()), int(merged_df['delivery_time_days'].max()), 0)
max_delivery_time = st.sidebar.slider('Maximum Delivery Time (Days)', int(merged_df['delivery_time_days'].min()), int(merged_df['delivery_time_days'].max()), int(merged_df['delivery_time_days'].max()))

# Filter dataset based on sidebar inputs
if selected_category == "Semua":
    filtered_df = merged_df[(merged_df['delivery_time_days'] >= min_delivery_time) &
                            (merged_df['delivery_time_days'] <= max_delivery_time)]
else:
    filtered_df = merged_df[(merged_df['product_category_name'] == selected_category) &
                            (merged_df['delivery_time_days'] >= min_delivery_time) &
                            (merged_df['delivery_time_days'] <= max_delivery_time)]

# Display filtered data
st.write(f"Displaying data for category: {selected_category}")
st.dataframe(filtered_df[['order_id', 'delivery_time_days', 'review_score', 'product_category_name']])

# Delivery Time vs Review Score
st.subheader('Delivery Time vs Review Score')
plt.figure(figsize=(10, 6))
sns.scatterplot(x='delivery_time_days', y='review_score', data=filtered_df)
plt.title('Delivery Time vs Review Score')
plt.xlabel('Delivery Time (Days)')
plt.ylabel('Review Score')
st.pyplot(plt)

# Correlation analysis
st.subheader('Correlation Analysis')
corr_matrix = filtered_df[['delivery_time_days', 'review_score']].corr()
st.write(corr_matrix)

# Most Purchased Product Categories
st.subheader('Most Purchased Product Categories')

# Create top categories DataFrame
top_category = create_top_category(products_order_item_df)

# Display the top categories in a table
st.write('Top 5 most purchased product categories:')
st.dataframe(top_category.head())

# Bar plot to visualize top categories
plt.figure(figsize=(10, 6))
sns.barplot(x='total_orders', y='product_category_name', data=top_category.head(10), palette='Blues_d')
plt.xlabel('Kategori Produk')   # Label for x-axis
plt.ylabel('Jumlah Penjualan')  # Label for y-axis
plt.title('Grafik Penjualan Kategori Produk')  # Title for the chart
plt.grid(axis='y', linestyle='--', alpha=0.7)  # Adding gridlines for better readability
st.pyplot(plt)  # Use st.pyplot to display the plot in Streamlit
