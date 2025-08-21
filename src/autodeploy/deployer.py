from ibm_watsonx_ai import APIClient
from ibm_watsonx_ai import Credentials
from ibm_watsonx_ai.deployments import RuntimeContext
from dotenv import load_dotenv
import uuid
import os 
load_dotenv()

class Deployer():
    def __init__(self):  
        self.credentials = Credentials(url=os.environ['WATSONX_URL'], api_key=os.environ['WATSONX_APIKEY'])
        self.api_client = APIClient(self.credentials)
        self.api_client.set.default_space(os.environ['WATSONX_SPACEID'])
        self.uid = uuid.uuid1() 
    # Step 1
    def build_environment(self, python_version=None, environment_name=None, base_runtime=None):
        self.python_version = python_version or "3.11"    
        self.environment_name = environment_name or f"{self.uid}-watsonx.ai env with langgraph"
        self.base_runtime = base_runtime or "runtime-24.1-py3.11"
        
        self.base_sw_spec_id = self.api_client.software_specifications.get_id_by_name(self.base_runtime)
        meta_prop_pkg_extn = {
            self.api_client.package_extensions.ConfigurationMetaNames.NAME: self.environment_name,
            self.api_client.package_extensions.ConfigurationMetaNames.DESCRIPTION: "Environment with langgraph",
            self.api_client.package_extensions.ConfigurationMetaNames.TYPE: "conda_yml"
        }
        self.pkg_extn_details = self.api_client.package_extensions.store(meta_props=meta_prop_pkg_extn, file_path="config.yaml")
    # Step 2
    def build_software_spec(self, spec_name=None, spec_description=None): 
        self.spec_name = spec_name or f"{self.uid}-AI service watsonx.ai custom software specification with langgraph"
        self.spec_description = spec_description or "Software specification for AI service deployment"
        meta_prop_sw_spec = {
            self.api_client.software_specifications.ConfigurationMetaNames.NAME: self.spec_name,
            self.api_client.software_specifications.ConfigurationMetaNames.DESCRIPTION: self.spec_description,
            self.api_client.software_specifications.ConfigurationMetaNames.BASE_SOFTWARE_SPECIFICATION: {"guid": self.base_sw_spec_id}
        }
        self.sw_spec_details = self.api_client.software_specifications.store(meta_props=meta_prop_sw_spec)
    # Step 3 
    def store_service(self, deployable_ai_service, service_name=None): 
        self.service_name = service_name or f"{self.uid}-AI service SDK with langgraph"
        self.deployable_ai_service = deployable_ai_service or {}
        
        sw_spec_id = self.api_client.software_specifications.get_id(self.sw_spec_details)
        pkg_extn_id = self.api_client.package_extensions.get_id(self.pkg_extn_details)
        self.api_client.software_specifications.add_package_extension(sw_spec_id, pkg_extn_id)
        meta_props = {
            self.api_client.repository.AIServiceMetaNames.NAME: self.service_name,    
            self.api_client.repository.AIServiceMetaNames.SOFTWARE_SPEC_ID: sw_spec_id
        }
        self.stored_ai_service_details = self.api_client.repository.store_ai_service(self.deployable_ai_service, meta_props)
        self.ai_service_id = self.api_client.repository.get_ai_service_id(self.stored_ai_service_details)
    
    # Step 4
    def deploy_service(self, deployment_name=None): 
        self.deployment_name = deployment_name or f"{self.uid}-AI service with tools"
        
        meta_props = {
            self.api_client.deployments.ConfigurationMetaNames.NAME: self.deployment_name,
            self.api_client.deployments.ConfigurationMetaNames.ONLINE: {}
        }
        self.deployment_details = self.api_client.deployments.create(self.ai_service_id, meta_props)


    def autodeploy(self, deployable_function): 
        self.export_config()
        self.build_environment()
        self.build_software_spec()
        self.store_service(deployable_function)
        self.deploy_service() 

    
    def export_config(self, python_version:str = None, channels:str = None, dependencies:list = None, prefix:str = None):
        self.python_version = python_version or 3.11 
        self.channels = channels or "empty"
        self.dependencies = dependencies or ["ibm-watsonx-ai==1.3.34", "langchain==0.3.27", "langchain-ibm==0.3.15", "langgraph==0.2.44", "python-dotenv==1.1.1", "yfinance==0.2.65"]
        self.prefix = prefix or "/opt/anaconda3/envs/python311"

        # Build pip dependencies with proper indentation
        pip_deps = ''.join([f'      - {dependency}\n' for dependency in self.dependencies])
        
        self.config_yml = f"""name: python{''.join(str(self.python_version).split('.'))}
channels:
  - {self.channels}
dependencies:
  - pip:
{pip_deps}prefix: {self.prefix}"""
        
        with open("config.yaml", "w", encoding="utf-8") as f:
            f.write(self.config_yml)
        print(self.config_yml)


