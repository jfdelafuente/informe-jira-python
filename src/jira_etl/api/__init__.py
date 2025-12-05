"""API client for Jira"""
from .client import JiraAPIHandler

# Alias para compatibilidad
JiraClient = JiraAPIHandler

__all__ = ['JiraAPIHandler', 'JiraClient']
