"""
Advanced usage example for WatsonX AutoDeploy library
Shows step-by-step deployment with custom parameters
"""

import os
from dotenv import load_dotenv
from autodeploy import Deployer

# Load environment variables
load_dotenv()

def custom_ai_service(context, **kwargs):
    """Custom AI service with different functionality"""
    # Your AI service implementation here
    def generate(context):
        return {"body": {"message": "Custom AI service response"}}
    
    def generate_stream(context):
        pass
        
    return generate, generate_stream

if __name__ == '__main__':
    # Initialize the deployer
    deployer = Deployer()
    
    # Step 1: Export custom configuration
    deployer.export_config(
        python_version="3.11",
        channels="conda-forge", 
        dependencies=[
            "ibm-watsonx-ai==1.3.34",
            "langchain==0.3.27",
            "langchain-ibm==0.3.15", 
            "langgraph==0.2.44",
            "python-dotenv==1.1.1",
            "pandas==2.0.0",  # Additional custom dependency
            "numpy==1.24.0"   # Additional custom dependency
        ],
        prefix="/opt/anaconda3/envs/custom_env"
    )
    
    # Step 2: Build environment with custom parameters
    deployer.build_environment(
        python_version="3.11",
        environment_name="my-custom-watsonx-env",
        base_runtime="runtime-24.1-py3.11"
    )
    
    # Step 3: Build software specification
    deployer.build_software_spec(
        spec_name="my-custom-software-spec",
        spec_description="Custom software specification for advanced AI service"
    )
    
    # Step 4: Store the AI service
    deployer.store_service(
        deployable_ai_service=custom_ai_service,
        service_name="my-advanced-ai-service"
    )
    
    # Step 5: Deploy the service
    deployer.deploy_service(
        deployment_name="my-production-deployment"
    )
    
    print("Advanced deployment completed successfully!")
    print(f"Service ID: {deployer.ai_service_id}")
    print(f"Deployment details: {deployer.deployment_details}") 