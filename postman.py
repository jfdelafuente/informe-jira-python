import urllib.request, urllib.parse, urllib.error
import json
import ssl

class JiraAPIHandler(object):
    """
    Adapter for SonarQube's web service API.
    """
    # Default host is local
    DEFAULT_HOST = 'https://jira.si.orange.es/rest/api/2/search?jql'
    DEFAULT_BASE_PATH = ''

    # Endpoint for resources and rules
    JIRA_AUTH_ENDPOINT = '/rest/auth/1/session'
    JIRA_SEARCH_ENDPOINT = '/rest/api/2/search?jql'


    def __init__(self, host=None, port=None, base_path=None):
        self._host = host or self.DEFAULT_HOST
        self._base_path = base_path or self.DEFAULT_BASE_PATH

    def _get_url(self, endpoint):
        return '{}{}{}'.format(self._host, self._base_path, endpoint)

    def _make_call(self, endpoint, **query_args):
        # Get method and make the call
        url = self._get_url(endpoint)
        encoded_args = urllib.parse.urlencode(query_args)
        # print(url)
        full_url = url + '?' + encoded_args
        # print(full_url)

        # Ignorar errores de certificado SSL
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE

        try:
            uh = urllib.request.urlopen(full_url, context=ctx)    
        except URLError as e:
            if hasattr(e, 'reason'):
                print('We failed to reach a server.')
                print('Reason: ', e.reason)
            elif hasattr(e, 'code'):
                print('The server couldn\'t fulfill the request.')
                print('Error code: ', e.code)
        else:
            res = uh.read().decode()
            return res

    def get_auth(self, qualifiers):
        query_args = {
            'qualifiers' : qualifiers,
            'ps' : '200'
        }
        datos = self._make_call(self.JIRA_AUTH_ENDPOINT, **query_args)
        return datos

    def get_issues(self, component):
        query_args = {
            'component': component, 
            'metricKeys': 'complexity, duplicated_lines_density, code_smells, sqale_rating, sqale_index, bugs, reliability_rating, vulnerabilities, security_rating, ncloc, coverage'
        }
        body = self._make_call(self.JIRA_SEARCH_ENDPOINT, **query_args)
        return body


def main():
    # inicializamos Sonarqube
    print("Inicio")
    h = JiraAPIHandler()

    # obtenemos los proyectos de Sonarqube
    project = h.get_issues("BOREAL-1777")

    print("Fin")

if __name__ == '__main__':
    main()