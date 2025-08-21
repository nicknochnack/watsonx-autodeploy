"""
Basic usage example for WatsonX AutoDeploy library
"""

import os
from dotenv import load_dotenv
from autodeploy import Deployer

# Load environment variables
load_dotenv()

def my_ai_service(context, space_id=os.environ['WATSONX_SPACEID'], url=os.environ['WATSONX_URL'], model_id=os.environ['MODEL_ID'], **kwargs):    
    """
    Example AI service function that can be deployed to WatsonX
    """
    from ibm_watsonx_ai import APIClient, Credentials
    from langchain_ibm import ChatWatsonx
    from langchain_core.tools import tool
    from langgraph.prebuilt import create_react_agent
    import yfinance as yf 

    # Initialize API client
    api_client = APIClient(
        credentials=Credentials(url=url, token=context.generate_token()),
        space_id=space_id
    )
    
    # Initialize chat model
    chat = ChatWatsonx(
        watsonx_client=api_client,
        model_id=model_id,
        params={"temperature": 0.1}
    )
    
    # Define tools
    @tool
    def add(a: float, b: float) -> float:
        """Add two numbers together."""
        return a + b
    
    @tool
    def get_stock_price(stock_ticker: str) -> float:
        """Get the latest stock price for a given ticker."""
        ticker = yf.Ticker(stock_ticker) 
        history = ticker.history(period='1mo')  
        return history['Close'].iloc[-1]

    tools = [add, get_stock_price]    
    graph = create_react_agent(chat, tools=tools)

    def generate(context) -> dict:        
        api_client.set_token(context.get_token())   
        payload = context.get_json()
        question = payload["question"]        
        response = graph.invoke({"messages": [("user", f"{question}")]})        
        json_messages = [msg.to_json() for msg in response['messages']]        
        response['messages'] = json_messages        
        return {"body": response}
    
    def generate_stream(context):
        # Streaming not implemented in this example
        pass
        
    return generate, generate_stream

if __name__ == '__main__':
    # Initialize the deployer
    deployer = Deployer()
    
    # Deploy the AI service automatically
    deployer.autodeploy(my_ai_service)
    
    print("Deployment completed successfully!")
    print(f"Deployment details: {deployer.deployment_details}") 