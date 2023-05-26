import json
import configD
import JiraAPIHandler as jiraAPIHandler

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()
    

    sJQL = 'type = Delivery AND "Bug/s" in (KRATOS-10566, INTEPS-6933, TEI-5013, INTEPS-6934, FRONTAC-35452, \
MICRO-40718, TIAFOS-914, TEI-5023, FRONTCO-25641, FRONTAC-35453, \
WCS-8158, MICRO-40696, INTEPS-7174, INTEPS-6956, INTEPS-7191, \
FRONTAC-35573, FRONTRE-16982, FRONTCO-25733, FRONTCO-25716, TEDTED-5145, \
INTEPS-7144, INTEPS-7143, INTEPS-7182, FRONTMC-15305, FRONTAT-1109, \
INTEPS-7161, CRM4TE-14159, TIAFOS-943)'

    ficheros = 0
    response = jira.get_delivs(sJQL)
    if response.status_code == 200:
        issues = json.loads(response.text)
        
    for issue in issues["issues"]:
        # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
        nom_file = issue["key"] + "_delivs_news.json"
        with open(configD.DIR_JIRA_DELIVS + nom_file, 'w') as file:
            json.dump(issue, file)
            print("Generando ... %s " % nom_file)  
            ficheros = ficheros + 1
        
    print("Se han generado %s ficheros" % ficheros)
    print("Fin")

if __name__ == '__main__':
    main()