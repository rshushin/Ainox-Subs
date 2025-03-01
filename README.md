# Ainox Subscription Sync

Ainox is a Russian payment system that provides subscription management and billing solutions. 
This script helps automate the retrieval and updating of subscriber data from Ainox into a Google Spreadsheet.

## Features
✅ Fetches subscriber data from Ainox API  
✅ Updates Google Sheets automatically  
✅ Stores credentials securely using environment variables  
✅ Handles existing and new subscribers efficiently  

## Prerequisites

Ensure you have the following installed:
- Python 3.x
- `pip` (Python package manager)

## Setup Instructions

### 1. Clone this repository
```bash
git clone https://github.com/your-username/ainox-subs-sync.git
cd ainox-subs-sync
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Set up environment variables
Create a `.env` file in the project directory and add the following:
```env
GOOGLE_CREDENTIALS_JSON=path/to/your/credentials.json
SPREADSHEET_KEY=your_google_sheet_key
AINOX_API_LOGIN=your_api_login
AINOX_API_KEY=your_api_key
```
⚠ **Never share or commit your `.env` file to GitHub!**

### 4. Run the script
```bash
python script.py
```

## License
This project is licensed under the MIT License. Feel free to use and modify it!

## Contributing
Pull requests are welcome! If you find any issues, feel free to open an issue.

## Contact
For any inquiries, contact [roman.shushin@gmail.com].


