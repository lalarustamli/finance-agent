# WhatsApp Finance Agent

A WhatsApp-based AI agent for personal financial planning that automatically categorizes and logs expenses to Google Sheets.

## Features

- Receive expense messages via WhatsApp
- AI-powered expense parsing and categorization
- Automatic logging to Google Sheets
- Support for multiple currencies and formats
- Intelligent expense categorization

## Categories

The system uses the following expense categories:
- Food & Drink
- Transportation
- Shopping
- Entertainment
- Bills & Utilities
- Health & Medical
- Education
- Travel
- Housing
- Personal Care
- Gifts & Donations
- Investments & Savings
- Business Expenses
- Subscriptions & Memberships
- Insurance
- Taxes
- Other

## Setup Instructions

1. Install dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env`: 
```
GOOGLE_SHEET_ID=your_sheet_id
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
```

3. Set up Google Sheets API:
   - Go to Google Cloud Console
   - Create a new project
   - Enable Google Sheets API
   - Create credentials (OAuth 2.0)
   - Download credentials and save as `credentials.json`

4. Set up Twilio:
   - Create a Twilio account
   - Get a WhatsApp-enabled phone number
   - Configure webhook URL in Twilio console to point to your server's `/webhook` endpoint

5. Run the application:
```bash
python src/main.py
```

## Usage

Send a message to your WhatsApp number in the format:
"€12 coffee at Starbucks"

The agent will:
1. Parse the amount and description
2. Categorize the expense
3. Log it to your Google Sheet
4. Send a confirmation message back

## Google Sheet Structure

The Google Sheet should have the following columns:
- Date
- Amount
- Description
- Category
