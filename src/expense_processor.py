from datetime import datetime
import json
import os
import logging
import openai
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure OpenAI
openai.api_key = os.getenv('OPENAI_API_KEY')

logger = logging.getLogger(__name__)

class ExpenseProcessor:
    def __init__(self):
        self.categories = self._load_categories()
        logger.info(f"Loaded categories: {self.categories}")
    
    def _load_categories(self):
        config_path = os.path.join(os.path.dirname(__file__), '../config/categories.json')
        try:
            with open(config_path, 'r') as f:
                return json.load(f)  # Now returns a list instead of a dict
        except Exception as e:
            logger.error(f"Error loading categories: {str(e)}")
            return []
    
    def process_message(self, message: str) -> dict:
        logger.info(f"Processing message: {message}")
        
        try:
            # Use GPT to parse the message with function calling
            response = openai.ChatCompletion.create(
                model="gpt-4o",
                messages=[
                    {"role": "user", "content": message}
                ],
                functions=[{
                    "name": "parse_expense",
                    "description": "Parse an expense message to extract amount, description, and category",
                    "parameters": {
                        "type": "object",
                        "properties": {
                            "amount": {
                                "type": "number",
                                "description": "The amount spent"
                            },
                            "description": {
                                "type": "string",
                                "description": "What the expense was for"
                            },
                            "category": {
                                "type": "string",
                                "description": "The category of the expense",
                                "enum": list(self.categories) + ["Other"]
                            }
                        },
                        "required": ["amount", "description", "category"]
                    }
                }],
                function_call={"name": "parse_expense"}
            )
            
            # Extract the function call result
            function_call = response.choices[0].message.function_call
            if not function_call:
                raise ValueError("No expense data could be extracted from the message")
            
            parsed_data = json.loads(function_call.arguments)
            amount = float(parsed_data['amount'])
            description = parsed_data['description']
            category = parsed_data['category']
            
            logger.info(f"GPT parsed amount: {amount}, description: {description}, category: {category}")
            
            return {
                'date': datetime.now().strftime('%Y-%m-%d'),
                'amount': amount,
                'description': description,
                'category': category
            }
            
        except Exception as e:
            logger.error(f"Error processing message with GPT: {str(e)}")
            raise ValueError(f"Could not process message: {str(e)}")
    