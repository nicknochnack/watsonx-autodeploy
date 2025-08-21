# WatsonX AutoDeploy

Automated deployment library for IBM WatsonX AI services with LangGraph support.

## Overview

WatsonX AutoDeploy simplifies the process of deploying AI services to IBM WatsonX by providing a clean, pythonic interface for:

- Creating custom environments with specified dependencies
- Building software specifications 
- Storing and deploying AI services
- Managing the entire deployment lifecycle

## Installation

### From PyPI (when published)
```bash
pip install watsonx-autodeploy
```

### From Source
```bash
git clone https://github.com/nicknochnack/watsonx-autodeploy.git
cd watsonx-autodeploy
pip install -e .
```

### Development Installation
```bash
git clone https://github.com/nicknochnack/watsonx-autodeploy.git
cd watsonx-autodeploy
pip install -e ".[dev]"
```

## Quick Start

### Environment Setup

First, set up your environment variables:

```bash
# .env file
WATSONX_URL=your_watsonx_url
WATSONX_APIKEY=your_api_key
WATSONX_SPACEID=your_space_id
MODEL_ID=your_model_id
```

### Basic Usage

```python
import os
from dotenv import load_dotenv
from autodeploy import Deployer

load_dotenv()

def my_ai_service(context, **kwargs):
    # Your AI service implementation
    def generate(context):
        return {"body": {"message": "Hello from WatsonX!"}}
    
    def generate_stream(context):
        pass
        
    return generate, generate_stream

# Deploy with one line
deployer = Deployer()
deployer.autodeploy(my_ai_service)
```

### Advanced Usage

```python
from autodeploy import Deployer

deployer = Deployer()

# Step-by-step deployment with custom parameters
deployer.export_config(
    python_version="3.11",
    channels="conda-forge",
    dependencies=["custom-package==1.0.0"],
    prefix="/opt/anaconda3/envs/custom"
)

deployer.build_environment(
    environment_name="my-custom-env",
    base_runtime="runtime-24.1-py3.11"
)

deployer.build_software_spec(
    spec_name="my-spec",
    spec_description="Custom specification"
)

deployer.store_service(
    deployable_ai_service=my_ai_service,
    service_name="my-service"
)

deployer.deploy_service(deployment_name="production-deployment")
```

## API Reference

### Deployer Class

The main class for managing WatsonX deployments.

#### `__init__()`
Initializes the deployer with WatsonX credentials from environment variables.

#### `autodeploy(deployable_function)`
One-step deployment method that handles the entire deployment pipeline.

**Parameters:**
- `deployable_function`: The AI service function to deploy

#### `export_config(python_version=None, channels=None, dependencies=None, prefix=None)`
Creates a conda environment configuration file.

**Parameters:**
- `python_version` (str, optional): Python version (default: "3.11")
- `channels` (str, optional): Conda channels (default: "empty") 
- `dependencies` (list, optional): List of pip dependencies
- `prefix` (str, optional): Environment prefix path

#### `build_environment(python_version=None, environment_name=None, base_runtime=None)`
Creates a package extension for the environment.

**Parameters:**
- `python_version` (str, optional): Python version
- `environment_name` (str, optional): Name for the environment
- `base_runtime` (str, optional): Base runtime specification

#### `build_software_spec(spec_name=None, spec_description=None)`
Creates a software specification.

**Parameters:**
- `spec_name` (str, optional): Name for the software specification
- `spec_description` (str, optional): Description of the specification

#### `store_service(deployable_ai_service, service_name=None)`
Stores the AI service in WatsonX repository.

**Parameters:**
- `deployable_ai_service`: The AI service function
- `service_name` (str, optional): Name for the service

#### `deploy_service(deployment_name=None)`
Deploys the stored AI service.

**Parameters:**
- `deployment_name` (str, optional): Name for the deployment

## Examples

See the `examples/` directory for complete usage examples:

- `examples/basic_usage.py` - Simple one-line deployment
- `examples/advanced_usage.py` - Step-by-step deployment with custom parameters

## Requirements

- Python 3.11+
- IBM WatsonX AI account and credentials
- Required dependencies (automatically installed):
  - ibm-watsonx-ai>=1.3.34
  - langchain>=0.3.27
  - langchain-ibm>=0.3.15
  - langgraph>=0.6.5
  - python-dotenv>=1.1.1

## Development

### Running Tests
```bash
pytest
```

### Code Formatting
```bash
black src/ examples/
```

### Type Checking
```bash
mypy src/
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Run the test suite
6. Submit a pull request

## License

MIT License. See LICENSE file for details.

## Support

For issues and questions:
- Open an issue on GitHub

## Changelog

### v0.1.0
- Initial release
- Basic deployment functionality
- Support for custom environments and dependencies
- One-step autodeploy feature
