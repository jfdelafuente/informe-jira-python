import json
import configD
import JiraAPIHandler as jiraAPIHandler

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()
    
    sJQL = 'type = Delivery AND "Bug/s" in (TEI-5006)'

    response = jira.get_delivs(sJQL)
    if response.status_code == 200:
        issue = json.loads(response.text)
    
    print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    
    with open(configD.DIR_JIRA_OUT + "delivs_news.json", 'w') as file:
        json.dump(issue, file)
    print("Fin")

if __name__ == '__main__':
    main()