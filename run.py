# Your code goes here.
# You can delete these comments, but do not change the name of this file
# Write your code to expect a terminal of 80 characters wide and 24 rows high

import gspread
from google.oauth2.service_account import Credentials


SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('love_sandwiches')


def f1_get_sales_data():
    """
    Get sales figures input from the user.
    Run a while loop to collect a valid string of data from the user
    via the terminal, which must be a string of 6 numbers separated
    by commas. The loop will repeatedly request data, until it is valid.
    """
    while True:
        print("Please enter sales data from the last market.")
        print("Data should be six numbers, separated by commas.")
        print("Example: 10,20,30,40,50,60\n")

        data_str = input("Enter your data here:\n")
        
        sales_data = data_str.split(",")
        print(f"1. data_str (grabbed from user input) = {data_str}")
        print(f"2. sales_data (converted to a split string)= {sales_data}")
        if f2_validate_data(sales_data):
            print("Data is valid!")
            break

    return sales_data


def f2_validate_data(values):
    """
    Inside the try, converts all string values into integers.
    Raises ValueError if strings cannot be converted into int,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 6:
            raise ValueError(
                f"Exactly 6 values required, you provided {len(values)}"
            )
    except ValueError as e:
        print(f"Invalid data: {e}, please try again.\n")
        return False
    
    return True


# def update_sales_worksheet(data):
#     """
#     Update sales worksheet, add new row with the list data provided
#     """
#     print("Updating sales worksheet...\n")
#     sales_worksheet = SHEET.worksheet("sales")
#     sales_worksheet.append_row(data)
#     print("Sales worksheet updated successfully.\n")


# def update_surplus_worksheet(data):
#     """
#     Update surplus worksheet with surplus data
#     """
#     print("Updating surplus worksheet...\n")
#     surplus_worksheet = SHEET.worksheet("surplus")
#     surplus_worksheet.append_row(data)
#     print("Surplus worksheet updated successfully.\n")


def f3_update_worksheet(data, worksheet):
    """
    Receives a list of integers to be inserted into a worksheet
    Update the relevant worksheet with the data provided
    """
    print(f"Updating {worksheet} worKsHeet...\n")
    worksheet_to_update = SHEET.worksheet(worksheet)
    worksheet_to_update.append_row(data)
    print(f"{worksheet} worksheet updated successfully\n")


def f4_calculate_surplus_data(sales_row):
    """
    Compare sales with stock and calculate the surplus for each item type.
    The surplus is defined as the sales figure subtracted from the stock:
    - Positive surplus indicates waste
    - Negative surplus indicates extra made when stock was sold out.
    """
    print("Calculating surplus data...\n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = (stock[len(stock)-1])
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock) - sales
        surplus_data.append(surplus)

    return surplus_data


def f5_get_last_5_entries_sales():
    """
    Collects columns of data from sales worksheet, collecting
    the last 5 entries for each sandwich and returns the data
    as a list of lists.
    """
    sales = SHEET.worksheet("sales")

    columns = []
    for ind in range(1, 7):
        column = sales.col_values(ind)
        columns.append(column[-5:])

    return columns


def f6_calculate_stock_data(data):
    """
    Calculate the average stock for each item type, adding 10%
    """
    print("Calculating stock data...\n")
    new_stock_data = []

    for column in data:
        int_column = [int(num) for num in column]

        average = sum(int_column) / len(int_column)
        stock_num = average * 1.1
        new_stock_data.append(round(stock_num))

    return new_stock_data


# def f7_main():
#     """
#     Run all program functions
#     """
#     data = f1_get_sales_data()
#     sales_data = [int(num) for num in data]
#     f3_update_worksheet(sales_data, "sales")
    
#     new_surplus_data = f4_calculate_surplus_data(sales_data)
#     print(new_surplus_data)
#     f3_update_worksheet(new_surplus_data, "surplus")

#     sales_columns = f5_get_last_5_entries_sales()
#     stock_data = f6_calculate_stock_data(sales_columns)
#     f3_update_worksheet(stock_data, "stock")
#     return stock_data

# print("Welcome to Love Sandwiches Data Automation")
# stock_data = f7_main()

print("Test if can retrieve headings row")

full_data = SHEET.worksheet("stock")
spreadsheet_column_count = len(full_data.col_values(1))

keys = full_data.row_values(1)
dict_values = full_data.row_values(14)

print(f"spreadsheet length is: {spreadsheet_column_count} columns")

print(f"dictionary keys are: {keys}")
print(f"dictionary values are: {dict_values}")

output_dictionary = {}
for key in keys:
    for value in dict_values:
        output_dictionary[key] = value
        dict_values.remove(value)
        break

print(output_dictionary)