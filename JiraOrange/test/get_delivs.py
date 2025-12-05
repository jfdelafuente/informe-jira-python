import json
import JiraAPIHandler as jiraAPIHandler


def mostrar_deliv(deliv):
    max = deliv["total"]
    for i in range(max):
        contar = len(deliv["issues"][i]["fields"]["customfield_16304"])
        if contar > 0:
            for j in range(0, contar):
                print("Bug:  %s - Deliv:  %s - Status: %s/%s " %  ( deliv["issues"][i]["fields"]["customfield_16304"][j]["key"],
                                                                    deliv["issues"][i]["key"],
                                                                    deliv["issues"][i]["fields"]["status"]["name"],
                                                                    deliv["issues"][i]["fields"]["customfield_16304"][j]["fields"]["status"]["name"]
                                                                    )
            )
    

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()
    
    sJQL = 'type = Delivery AND "Bug/s" in (FRONTAC-35453)'

    response = jira.get_delivs(sJQL)
    if response.status_code == 200:
        issue = json.loads(response.text)
    
    print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    mostrar_deliv(issue)
    
    print("Fin")

if __name__ == '__main__':
    main()