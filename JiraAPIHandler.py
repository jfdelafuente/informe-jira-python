# Import the required libraries
import requests
from requests.auth import HTTPBasicAuth
import json
import pandas as pd
import os
from dotenv import load_dotenv

class JiraAPIHandler(object):
    """
    Adapter for JIRA web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'https://jira.si.orange.es'
    DEFAULT_BASE_PATH = ''

    # Endpoint for resources and rules
    JIRA_AUTH_ENDPOINT = '/rest/auth/1/session'
    JIRA_SEARCH_ENDPOINT = '/rest/api/latest/search'
    JIRA_ISSUE_SEARCH_ENDPOINT = '/rest/api/latest/issue'


    def __init__(self, host=None, port=None, base_path=None):
        load_dotenv()
        self._host = host or self.DEFAULT_HOST
        self._base_path = base_path or self.DEFAULT_BASE_PATH
        self.usuario = os.environ['USUARIO']
        self.password = os.environ['PASSWORD']

    def _get_url(self, endpoint):
        return '{}{}{}'.format(self._host, self._base_path, endpoint)

    def _make_call(self, endpoint, **query_args):
        # Get method and make the call
        url = self._get_url(endpoint)
        # print(url)
        
        headers = {
	        "Accept": "application/json"
        }
        
        auth = HTTPBasicAuth(self.usuario, 
                             self.password)
        
        response = requests.request(
	        "GET",
	        url,
	        headers=headers,
	        auth=auth,
	        params=query_args
        )
        return response
    

    def get_issues(self, issue):
        query_args = {
        }
        print(query_args)
        body = self._make_call(self.JIRA_ISSUE_SEARCH_ENDPOINT+ "/" +issue, **query_args)
        return body
    
    def get_project(self, proyecto):
        query_args = {
            'jql': 'project="' + proyecto + '"'
        }
        print(query_args)
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body
    
    def get_bug(self, epsilon):
        query_args = {
            'jql': 'Type = Bug AND ("Remedy HD" ~ ' +epsilon+ ')',
            'fields': 'customfield_11104, issuetype, status, resolution',
            'startAt' : '0',
            'maxResult': '500'
        }
        # print(json.dumps(query_args, sort_keys=True, indent=4, separators=(",", ": ")))
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body
    
    def get_bugs(self, lista_epsilons):
        sJQL = "Type = Bug AND ("
        tam = len(lista_epsilons) -1
        for index, row in lista_epsilons.iterrows():
            if index < tam:
                sJQL += f' "Remedy HD" ~ {row["Incidencia"]} OR'
            else:
                sJQL += f' "Remedy HD" ~ {row["Incidencia"]}'
        sJQL += f' ) ORDER BY cf[11104], status ASC '
        query_args = {
            'jql': '' + sJQL + '',
            'fields': 'customfield_11104, issuetype, status, resolution',
            'startAt' : '0',
            'maxResult': '500'
        }
        # print(json.dumps(query_args, sort_keys=True, indent=4, separators=(",", ": ")))
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body