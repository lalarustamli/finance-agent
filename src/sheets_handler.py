from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import os
import pickle
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
        creds = None
        # The file token.pickle stores the user's access and refresh tokens
        if os.path.exists('token.pickle'):
            logger.info("Found existing token.pickle file")
            with open('token.pickle', 'rb') as token:
                creds = pickle.load(token)
        
        # If there are no (valid) credentials available, let the user log in.
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                logger.info("Refreshing expired credentials")
                creds.refresh(Request())
            else:
                logger.info("Getting new credentials")
                flow = InstalledAppFlow.from_client_secrets_file(
                    'credentials.json', self.SCOPES)
                # Add these parameters to handle the OAuth flow better
                creds = flow.run_local_server(
                    port=0,
                    prompt='consent',
                    authorization_prompt_message='Please authorize the application to access your Google Sheets.',
                    success_message='Authentication successful! You can close this window.'
                )
            
            # Save the credentials for the next run
            with open('token.pickle', 'wb') as token:
                logger.info("Saving new credentials to token.pickle")
                pickle.dump(creds, token)
        
        return creds
    
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