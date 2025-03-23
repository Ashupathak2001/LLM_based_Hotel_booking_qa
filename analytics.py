import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = "C:\\Users\\Ashish\\Desktop\\hotel_booking\\cleaned_hotel_bookings.csv"
df = pd.read_csv(file_path)

# Display first few rows
print(df.head())

# Step 1: Data Cleaning
df.dropna(inplace=True)  # Remove missing values
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])  # Convert to datetime

# Step 2: Revenue Trends Over Time
df['revenue'] = df['adr'] * df['stays_in_week_nights'] + df['adr'] * df['stays_in_weekend_nights']
monthly_revenue = df.groupby(df['reservation_status_date'].dt.to_period("M"))['revenue'].sum()

plt.figure(figsize=(10, 5))
monthly_revenue.plot(kind='line', marker='o', color='b')
plt.title("Monthly Revenue Trends")
plt.xlabel("Month")
plt.ylabel("Total Revenue")
plt.grid()
# plt.show()

# Step 3: Cancellation Rate
cancellation_rate = (df['is_canceled'].sum() / len(df)) * 100
print(f"Cancellation Rate: {cancellation_rate:.2f}%")

# Step 4: Geographical Distribution
plt.figure(figsize=(12, 6))
sns.countplot(y=df['country'], order=df['country'].value_counts().index)
plt.title("Geographical Distribution of Bookings")
plt.xlabel("Number of Bookings")
plt.ylabel("Country")
# plt.show()

# Step 5: Booking Lead Time Distribution
plt.figure(figsize=(10, 5))
sns.histplot(df['lead_time'], bins=50, kde=True, color="purple")
plt.title("Booking Lead Time Distribution")
plt.xlabel("Days Before Check-in")
plt.ylabel("Frequency")
# plt.show()
