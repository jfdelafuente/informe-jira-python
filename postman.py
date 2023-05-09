import json
import JiraAPIHandler as jiraAPIHandler

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()

    # obtenemos los datos de un bug
    # response = jira.get_project("ORANGE MPVs")
    # response = jira.get_issues("BOREAL-1777")
    response = jira.get_bug("INC000002783177")
    if response.status_code == 200:
        issue = json.loads(response.text)
    
    print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    print("Fin")

if __name__ == '__main__':
    main()