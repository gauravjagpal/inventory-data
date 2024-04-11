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
SHEET = GSPREAD_CLIENT.open('inventory-data')

sales = SHEET.worksheet('sales')

data=sales.get_all_values()

def get_sales_data():
    """
    Get sales figures
    """
    print("Please enter sales data.")
    print("Data should be 3 numbers separated by commas.")
    print("Example: 1,2,3,4,5,6\n")

    data_str = input("Enter your data here:")
    print(f"The data you provided is {data_str}")
    sales_data = data_str.split(",")
    validate_data (sales_data)


def validate_data(values):
    """
    Inside the try converts all string into integers. Raises a ValueError if string cannot be converted, or if there aren't exactly 6 values.
    """
    try:
        if len(values) != 3:
            raise ValueError (
                f'Exactly 3 values required, you provided {len(values)}'
            )
    except ValueError as e:
        print(f'Invalid data: {e}, please try again. \n')
get_sales_data()

