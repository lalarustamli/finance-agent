from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json
import logging

logger = logging.getLogger(__name__)

class SheetsHandler:
    def __init__(self):
        self.SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
        self.SPREADSHEET_ID = os.getenv('GOOGLE_SHEET_ID')
        self.RANGE_NAME = "'Expenses'!A:D"
        logger.info(f"Initializing SheetsHandler with spreadsheet ID: {self.SPREADSHEET_ID}")
        self.creds = self._get_credentials()
    
    def _get_credentials(self):
        try:
            # Get credentials from environment variable
            credentials_json = os.getenv('GOOGLE_CREDENTIALS')
            if not credentials_json:
                raise ValueError("GOOGLE_CREDENTIALS environment variable not set")
            
            # Parse the JSON string from environment variable
            credentials_info = json.loads(credentials_json)
            
            # Create credentials from service account info
            credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=self.SCOPES
            )
            
            return credentials
            
        except Exception as e:
            logger.error(f"Error getting credentials: {str(e)}")
            raise
    
    def log_expense(self, expense_data: dict):
        logger.info(f"Attempting to log expense: {expense_data}")
        service = build('sheets', 'v4', credentials=self.creds)
        
        values = [[
            expense_data['date'],
            expense_data['amount'],
            expense_data['description'],
            expense_data['category']
        ]]
        
        body = {
            'values': values
        }
        
        try:
            logger.info(f"Appending to sheet: {self.SPREADSHEET_ID}, range: {self.RANGE_NAME}")
            result = service.spreadsheets().values().append(
                spreadsheetId=self.SPREADSHEET_ID,
                range=self.RANGE_NAME,
                valueInputOption='RAW',
                body=body
            ).execute()
            logger.info(f"Successfully appended to sheet. Result: {result}")
            return True
        except Exception as e:
            logger.error(f"Error logging expense: {str(e)}")
            return False 