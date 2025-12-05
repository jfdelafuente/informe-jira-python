import json
import JiraAPIHandler as jiraAPIHandler


def mostrar_bugs(bug):
    contar = bug["total"]
    if contar > 0:
        for j in range(0, contar):
            print("%s - vIssueKey:  %s - vNumIncidencia:  %s - vListaBugs: %s / %s" %  (j,
                                                                        bug["issues"][j]["fields"]["customfield_11104"], 
                                                                        bug["issues"][j]["key"], 
                                                                        bug["issues"][j]["fields"]["status"]["name"],
                                                                        bug["issues"][j]["fields"]["resolution"]["name"]
                                                                           )
            )

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()

    # obtenemos los datos de un bug
    # response = jira.get_project("ORANGE MPVs")
    # response = jira.get_issues("BOREAL-1777")
    response = jira.get_bug("INC000002830586")
    if response.status_code == 200:
        issue = json.loads(response.text)
    
    print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    mostrar_bugs(issue)
    print("Fin")

if __name__ == '__main__':
    main()