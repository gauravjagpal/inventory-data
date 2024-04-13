import gspread
from google.oauth2.service_account import Credentials
from pprint import pprint

SCOPE = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.file",
    "https://www.googleapis.com/auth/drive"
    ]

CREDS = Credentials.from_service_account_file('creds.json')
SCOPED_CREDS = CREDS.with_scopes(SCOPE)
GSPREAD_CLIENT = gspread.authorize(SCOPED_CREDS)
SHEET = GSPREAD_CLIENT.open('inventory-data')

sales = SHEET.worksheet('sales')
data=sales.get_all_values()
def get_sales_data():
    """
    Get sales figures
    """
    while True:
        print("Please enter sales data.")
        print("Data should be 3 numbers separated by commas.")
        print("Example: 1,2,3\n")

        data_str = input("Enter your data here:")

        sales_data = data_str.split(",")
        validate_data(sales_data)

        if validate_data(sales_data):
            print("Data is valid")
            break
    return sales_data
    
def validate_data(values):
    """
    Inside the try converts all string into integers.
    Raises a ValueError if string cannot be converted,
    or if there aren't exactly 6 values.
    """
    try:
        [int(value) for value in values]
        if len(values) != 3:
            raise ValueError(f'Exactly 3 values required, you provided {len(values)}')
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')

    return True

def update_sales_worksheet(data):
    """
    Update sales worksheet, add new row with the list of data provided
    """
    print("Updating sales worksheet... \n")
    sales_worksheet = SHEET.worksheet("sales")
    sales_worksheet.append_row(data)
    print("Sales worksheet update succesfully. \n")

def calculate_surplus_data(sales_row):
    """
    Compare sales and stock data
    
    The surplus is defined as the sales - stock:
    - Positive surplus indicates waste
    - Negative surplus indiactes extra made
    """
    print("Calculating surplus data... \n")
    stock = SHEET.worksheet("stock").get_all_values()
    stock_row = stock[-1]
    
    surplus_data = []
    for stock, sales in zip(stock_row, sales_row):
        surplus = int(stock)-int(sales)
        surplus_data.append(surplus)
    return surplus_data

def update_surplus_worksheet(data):
    """
    Update surplus worksheet, add new row with the list of data provided
    """
    print("Updating surplus worksheet... \n")
    surplus_worksheet = SHEET.worksheet("surplus")
    surplus_worksheet.append_row(data)
    print("Surplus worksheet update succesfully. \n")

def main():
    """
    run all functions
    """
    data = get_sales_data()
    sales_data = [int(num) for num in data]
    update_sales_worksheet(sales_data)
    new_surplus_data = calculate_surplus_data(sales_data)
    update_surplus_worksheet(new_surplus_data)

print("welcome to the data warehouse")
main()