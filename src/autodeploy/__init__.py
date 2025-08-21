"""
WatsonX AutoDeploy - Automated deployment library for IBM WatsonX AI services

This library provides a simple interface for deploying AI services to IBM WatsonX
with support for LangGraph and custom environments.
"""

from .deployer import Deployer

__version__ = "0.1.0"
__author__ = "Nicholas Renotte"
__email__ = "nicholas.renotte@ibm.com"

__all__ = ['Deployer']