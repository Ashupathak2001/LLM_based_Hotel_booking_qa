import pandas as pd
import numpy as np

# Load dataset
file_path = "hotel_bookings.csv"  # Change this if needed
df = pd.read_csv(file_path)

#  Handle Missing Values
df.drop(columns=['company'], inplace=True)  # Too many missing values
df['children'].fillna(0, inplace=True)  # Fill missing children count with 0
df['country'].fillna(df['country'].mode()[0], inplace=True)  # Fill missing country with mode
df['agent'].fillna(0, inplace=True)  # Fill missing agent with 0

#  Format Data Correctly
df['reservation_status_date'] = pd.to_datetime(df['reservation_status_date'])  # Convert to datetime

#  Remove Outliers
df = df[(df['adr'] > 0) & (df['adr'] < df['adr'].quantile(0.99))]  # Remove extreme ADR values
df = df[(df['lead_time'] < df['lead_time'].quantile(0.99))]  # Remove extreme lead times

#  Feature Engineering (Optional)
df['total_nights'] = df['stays_in_week_nights'] + df['stays_in_weekend_nights']  # Total nights stayed
df['booking_month'] = df['reservation_status_date'].dt.month  # Extract booking month

#  Save Preprocessed Data
df.to_csv("cleaned_hotel_bookings.csv", index=False)

print("✅ Data Preprocessing Complete! Cleaned data saved as 'cleaned_hotel_bookings.csv'.")
