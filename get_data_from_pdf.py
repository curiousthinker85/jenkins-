import pandas as pd
import os
import re

def car_registrations_source_monthly():
    # Define the input file path and output directory directly in the function
    input_path = "table_3.csv"  # Specify input file path here

    # Read the CSV file
    df = pd.read_csv(input_path)

    # Step 1: Clean the DataFrame
    df_cleaned = df.dropna(how='all')  # Drop rows that are completely empty

    country_col_name = df_cleaned.columns[0]
    countries = df_cleaned[country_col_name].dropna().values  # Get all country names

    # Step 3: Extract month and year dynamically from the table
    # Month and year are extracted based on the position in the table
    month = df_cleaned.iloc[1, 2]  # Adjust as needed
    year = df_cleaned.iloc[2, 1]  # Adjust as needed

    # Step 5: Extract categories dynamically from the first row of the table
    categories = []
    for col_name in df_cleaned.columns:
        if 'Unnamed' in col_name:  # Dynamically identify category columns
            category_raw = df_cleaned.at[0, col_name]  # Get the category from the second row
            if pd.notna(category_raw):
                # Remove digits before or after the category name, and convert to uppercase
                category_cleaned = re.sub(r'\d+', '', str(category_raw)).strip().upper()
                categories.append(category_cleaned)

    # Step 6: Define countries to exclude from processing
    exclude_countries = ['EUROPEAN UNION', 'EFTA', 'EU + EFTA + UK']

    # Step 7: Initialize a list to store output rows
    output_rows = []

    # Step 8: Loop through the cleaned dataframe and extract relevant data
    for idx, row in df_cleaned.iterrows():
        country = row[country_col_name]  # Get the country name from the 'MONTHLY2' column
        
        # Ensure this row contains a valid country name and is not in the exclude list
        if pd.isna(country) or str(country).strip() == '' or country.upper() in exclude_countries:
            continue

        # Step 9: For each country, extract the corresponding category and registration values
        col_idx = 1  # Start at the second column (the first column is country names)
        for category_idx, category in enumerate(categories):
            try:
                # Extract the corresponding registration value
                month_year_value = row.iloc[col_idx]
                
                # Skip rows like '% CHANGE' or non-numeric registration data
                if pd.notna(month_year_value) and isinstance(month_year_value, str) and not month_year_value.endswith('%'):
                    # Remove commas and convert to numeric (if applicable)
                    month_year_value = month_year_value.replace(',', '')
                    
                    # Only append if we have a valid number
                    if month_year_value.isnumeric():
                        # Append year, month, category, country, and registration value
                        output_rows.append([year, month, category, country, month_year_value])
            except IndexError:
                pass  # Skip if column index is out of bounds
            
            # Move to the next category column (skip 3 columns: category name, current September value, next category name)
            col_idx += 3

    # Step 10: Create a DataFrame with the extracted data
    final_df = pd.DataFrame(output_rows, columns=['year', 'month', 'category', 'country', 'Registrations'])

    # Step 11: Remove rows with 'TOTAL' category
    final_df = final_df[final_df['category'] != 'TOTAL']  # Remove rows with the 'TOTAL' category

    # Step 9: Group the data by Category first, then by Country
    grouped_data = final_df.groupby(['category', 'country'], as_index=False).sum()

    # Step 10: Re-arrange the output so that each category is followed by all countries
    reversed_output_rows = []

    for category in categories:
        # Get the rows for this category
        category_data = final_df[final_df['category'] == category]
        
        for idx, row in category_data.iterrows():
            reversed_output_rows.append([row['year'], row['month'], row['category'], row['country'], row['Registrations']])

    # Step 11: Create a DataFrame from the reversed output
    reversed_df = pd.DataFrame(reversed_output_rows, columns=['year', 'month', 'category', 'country', 'Registrations'])

    # Step 7: Create the output file name dynamically
    output_path = f"{month}_{year}_car_registrations_monthly.csv".lower()

    # Step 12: Save the reversed DataFrame to a CSV
    reversed_df.to_csv(output_path, index=False)

    print(f"Data processed and saved to: {output_path}")

def car_registrations_market_year_to_date():
    # Define the input file path here
    input_path = "table_4.csv"  # Input file path
    
    # Read the CSV file
    df = pd.read_csv(input_path)
    
    # Step 1: Clean the DataFrame
    df_cleaned = df.dropna(how='all')  # Drop rows that are completely empty

    # Step 2: Extract country names from 'Unnamed: 1' column
    countries = df_cleaned['Unnamed: 1'].dropna().values  # Get all country names

    # Step 3: Extract categories dynamically from the first row of the table
    categories = []
    for col_name in df_cleaned.columns:
        if 'Unnamed' in col_name:  # Dynamically identify category columns
            category_raw = df_cleaned.at[0, col_name]  # Get the category from the second row
            if pd.notna(category_raw):
                # Remove digits before or after the category name, and convert to uppercase
                category_cleaned = re.sub(r'\d+', '', str(category_raw)).strip().upper()
                categories.append(category_cleaned)

    # Define countries to exclude
    exclude_countries = ['EUROPEAN UNION', 'EFTA', 'EU + EFTA + UK']

    # Extract month and year from specific rows and columns
    month = df_cleaned.iloc[1, 2]  # Extract month (3rd column, 2nd row)
    year = df_cleaned.iloc[2, 2]  # Extract year (3rd column, 3rd row)

    # Create a list to store output rows
    output_rows = []

    # Step 4: Loop through the cleaned dataframe to extract the necessary data
    for idx, row in df_cleaned.iterrows():
        country = row['Unnamed: 1']  # Country name in 'Unnamed: 1'

        # Ensure this row contains a valid country name and is not in the exclude list
        if pd.isna(country) or str(country).strip() == '' or country in exclude_countries:
            continue

        # Step 5: For each country, extract the corresponding category and September 2024 values
        col_idx = 2  # Start at the second column, which holds Jan-Sep 2024 values
        for category_idx, category in enumerate(categories):
            category_column = row.iloc[col_idx + 1]  # Get category names from columns like 'Unnamed: 2', 'Unnamed: 5', etc.
            month_year_value = row.iloc[col_idx]  # Get Jan_Sep 2024 values from columns like 'Unnamed: 1', 'Unnamed: 4', etc.
            
            if pd.notna(month_year_value):
                # Append year, month, category, country, and registration value
                output_rows.append([year, month, category.upper(), country, month_year_value])
                
            # Move to the next category (skip 3 columns: September value, category name, next September value)
            col_idx += 3

    # Step 6: Create a DataFrame with the extracted data
    final_df = pd.DataFrame(output_rows, columns=['year', 'month', 'category', 'country', 'Registrations'])

    # Step 7: Remove rows with 'TOTAL' category
    final_df = final_df[final_df['category'] != 'TOTAL']  # Remove 'TOTAL' rows

    # Step 8: Group the data by Category first, then by Country
    grouped_data = final_df.groupby(['category', 'country'], as_index=False).sum()

    # Step 9: Re-arrange the output so that each category is followed by all countries
    reversed_output_rows = []

    for category in categories:
        # Get the rows for this category
        category_data = final_df[final_df['category'] == category]
        
        for idx, row in category_data.iterrows():
            reversed_output_rows.append([row['year'], row['month'], row['category'], row['country'], row['Registrations']])

    # Step 10: Create a DataFrame from the reversed output
    reversed_df = pd.DataFrame(reversed_output_rows, columns=['year', 'month', 'category', 'country', 'Registrations'])

    # Step 11: Save the reversed DataFrame to a CSV with dynamic filename
    output_path = f"{month}_{year}_car_registrations_market_year_to_date.csv".lower()  # Dynamic output path
    
    reversed_df.to_csv(output_path, index=False)
    
    print(f"Data processed and saved to: {output_path}")


def car_registrations_by_manufacturer_EU():
    # Step 1: Read the CSV file
    df = pd.read_csv("table_5.csv")  # Use the new input file path

    # Step 2: Clean the DataFrame - Drop rows that are completely empty
    df_cleaned = df.dropna(how='all')

    # Step 7: Extract the month and year dynamically
    month = df_cleaned.iloc[0, 3]  # Get the value from the first row, third column
    year = df_cleaned.iloc[2, 1]   # Get the value from the third row, second column

    # Step 3: Dynamically get the column names
    country_col_name = df_cleaned.columns[0]  # The first column name (e.g., 'EUROPEAN UNION4(EU)')
    share_col_name = df_cleaned.columns[1]  # The second column name (e.g., 'Unnamed: 1')
    units_col_name = df_cleaned.columns[3]  # The fourth column name (e.g., 'Unnamed: 3')

    # Step 4: Assign proper names to the columns
    df_cleaned = df_cleaned[[country_col_name, share_col_name, units_col_name]]
    df_cleaned.columns = ['Country', '%Share', 'Units']  # Rename columns for clarity

    # Step 5: Clean up the 'Country' column by removing any digits before or after the country name
    df_cleaned['Country'] = df_cleaned['Country'].apply(lambda x: re.sub(r'\d+', '', str(x)).strip() if isinstance(x, str) else x)

    # Step 6: Filter rows for valid data only (non-null values in 'Country' and 'Units')
    df_cleaned = df_cleaned.dropna(subset=['Country', 'Units'])  # Keep only rows with valid 'Country' and 'Units'

    # Step 8: Add fixed Year and Month columns
    df_cleaned['Month'] = month
    df_cleaned['Year'] = year

    # Step 9: Rearrange columns
    df_cleaned = df_cleaned[['Year', 'Month', 'Country', '%Share', 'Units']]

    # Step 10: Save the transformed data to a CSV file
    output_path = f"{month}_{year}_car_registrations_by_manufacturer_EU.csv"  # Dynamic output path
    df_cleaned.to_csv(output_path, index=False)

    print(f"Data processed and saved to: {output_path}")


def car_registrations_by_manufacturer_EU_EFTA_UK():
    # Read the CSV file
    df = pd.read_csv("table_6.csv")

    # Step 1: Clean the DataFrame
    df_cleaned = df.dropna(how='all')  # Drop rows that are completely empty

    month = df_cleaned.iloc[0, 3]  # Get the value from the first row, third column
    year = df_cleaned.iloc[2, 1]

    # Step 3: Dynamically get the column names
    country_col_name = df_cleaned.columns[0]  # The first column name (e.g., 'EUROPEAN UNION4(EU)')
    share_col_name = df_cleaned.columns[1]  # The second column name (e.g., 'Unnamed: 1')
    units_col_name = df_cleaned.columns[3]  # The fourth column name (e.g., 'Unnamed: 3')

    # Step 4: Assign proper names to the columns
    df_cleaned = df_cleaned[[country_col_name, share_col_name, units_col_name]]
    df_cleaned.columns = ['Country', '%Share', 'Units']  # Rename columns for clarity

    # Step 3: Clean up the 'Country' column by removing any digits before or after the company name
    df_cleaned['Country'] = df_cleaned['Country'].apply(lambda x: re.sub(r'\d+', '', str(x)).strip() if isinstance(x, str) else x)

    # Step 4: Filter rows for September data only (assumes relevant rows are non-null and numeric in 'Units')
    df_cleaned = df_cleaned.dropna(subset=['Country', 'Units'])  # Keep only rows with valid Country and Units

    # Step 5: Add fixed Year and Month columns
    df_cleaned['Year'] = year 
    df_cleaned['Month'] = month

    # Step 6: Rearrange columns
    df_cleaned = df_cleaned[['Year', 'Month', 'Country', '%Share', 'Units']]

    # Step 7: Save the transformed data to a CSV file
    output_path = f"{month}_{year}_car_registrations_by_manufacturer_EU_EFTA_UK.csv"  # Dynamic output path
    df_cleaned.to_csv(output_path, index=False)

    print(f"Data processed and saved to: {output_path}")

car_registrations_source_monthly()
car_registrations_market_year_to_date()
car_registrations_by_manufacturer_EU()
car_registrations_by_manufacturer_EU_EFTA_UK()
