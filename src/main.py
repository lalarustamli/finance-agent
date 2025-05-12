from fastapi import FastAPI, Request
from twilio.twiml.messaging_response import MessagingResponse
from dotenv import load_dotenv
import os
import uvicorn
from expense_processor import ExpenseProcessor
from sheets_handler import SheetsHandler
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()


app = FastAPI()
expense_processor = ExpenseProcessor()
sheets_handler = SheetsHandler()

def create_response(message: str) -> str:
    """Create a Twilio response with the given message"""
    resp = MessagingResponse()
    resp.message(message)
    return str(resp)

async def process_and_log_expense(message_body: str) -> str:
    """Process expense message and log to Google Sheets"""
    expense_data = expense_processor.process_message(message_body)
    logger.info(f"Processed expense data: {expense_data}")
    
    if not expense_data:
        return create_response("❌ Error: No expense data found")
        
    if sheets_handler.log_expense(expense_data):
        logger.info("Successfully logged expense to Google Sheets")
        return create_response(
            f"✅ Expense logged: {expense_data['amount']}€ for "
            f"{expense_data['description']} ({expense_data['category']})"
        )
    
    logger.error("Failed to log expense to Google Sheets")
    return create_response("❌ Error: Could not log expense to Google Sheets")

@app.post("/webhook")
async def webhook(request: Request):
    form_data = await request.form()
    message_body = form_data.get('Body', '')
    sender = form_data.get('From', '')
    
    logger.info(f"Received message from {sender}: {message_body}")
    
    try:
        return await process_and_log_expense(message_body)
    except Exception as e:
        logger.error(f"Error processing message: {str(e)}")
        return create_response(f"❌ Error processing expense: {str(e)}")

if __name__ == "__main__":
    logger.info("Starting Finance Agent server...")
    uvicorn.run(app, host="0.0.0.0", port=8000)