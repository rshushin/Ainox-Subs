import os
import gspread
import requests
from oauth2client.service_account import ServiceAccountCredentials
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Google Sheets API setup
scope = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds_path = os.getenv("GOOGLE_CREDENTIALS_JSON")
spreadsheet_key = os.getenv("SPREADSHEET_KEY")

try:
    creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
    client = gspread.authorize(creds)
    spreadsheet = client.open_by_key(spreadsheet_key)
    sheet = spreadsheet.get_worksheet_by_id(0)  # GID=0
except Exception as e:
    print(f"Error setting up Google Sheets: {e}")
    exit()

# Ainox API setup
ainox_url = 'https://go.ainox.pro/api/'
headers = {
    'api-login': os.getenv("AINOX_API_LOGIN"),
    'api-key': os.getenv("AINOX_API_KEY")
}

STATUS_MAP = {1: "Active", 2: "Deactivated", 3: "Not Paid", 4: "Cancelled", 7: "Completed"}

clear_sheet = True  # Will clear the sheet each time the script runs

if clear_sheet:
    sheet.clear()
    print("Sheet cleared. Starting fresh.")

# Check/set headers
headers_list = ["ID", "Email", "Name", "Status", "Next Payment Date", "Next Payment Price", "Price", "Phone"]
existing_headers = sheet.row_values(1)
if not existing_headers:
    sheet.update(values=[headers_list], range_name='A1')

# Fetch subscribers
subscribers_data = {
    "request": "subscriber",
    "type": "output",
    "limit": 0,
    "offset": 0,
    "fields": ["id", "email", "status", "next_payment_date", "next_payment_price", "price", "first_invoice_id"]
}

response = requests.post(ainox_url, json=subscribers_data, headers=headers)

if response.status_code == 200 and 'data' in response.json():
    subscribers = response.json()['data']
    existing_data = sheet.get_all_values()[1:]  # Skip header row
    existing_ids = {row[0]: idx + 2 for idx, row in enumerate(existing_data)}
    
    updated_data = []
    for subscriber in subscribers:
        subscriber_id = str(subscriber.get('id', ''))
        email = subscriber.get('email', '')
        name = "Unknown"
        phone = "Unknown"
        first_invoice_id = subscriber.get('first_invoice_id')

        if first_invoice_id:
            parent_request_data = {
                "request": "request",
                "type": "output",
                "id": first_invoice_id
            }

            parent_response = requests.post(ainox_url, json=parent_request_data, headers=headers)
            
            if parent_response.status_code == 200:
                parent_data = parent_response.json().get('data', {})
                name = parent_data.get('name', name)
                phone = parent_data.get('phone', phone)

        next_payment_date = ''
        if subscriber.get('next_payment_date'):
            try:
                date_obj = datetime.strptime(subscriber['next_payment_date'], '%Y-%m-%d %H:%M:%S')
                next_payment_date = date_obj.strftime('%Y-%m-%d')
            except ValueError:
                pass

        subscriber_info = [
            subscriber_id,
            email,
            name,
            STATUS_MAP.get(subscriber.get('status', ''), 'Unknown'),
            next_payment_date,
            str(subscriber.get('next_payment_price', '')),
            str(subscriber.get('price', '')),
            phone
        ]
        
        if subscriber_id in existing_ids:
            row_index = existing_ids[subscriber_id]
            sheet.update(values=[subscriber_info], range_name=f"A{row_index}")
        else:
            updated_data.append(subscriber_info)
    
    if updated_data:
        sheet.append_rows(updated_data)
else:
    print(f"API Error: {response.status_code}\n{response.text}")
