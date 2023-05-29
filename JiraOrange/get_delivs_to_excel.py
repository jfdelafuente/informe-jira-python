import json
import configD
import api.JiraAPIHandler as jiraAPIHandler
from utils.utils import load_to_json

def main():
    # inicializamos Jira
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()
    

    sJQL = 'type = Delivery AND "Bug/s" in (KRATOS-10566, INTEPS-6933, TEI-5013, INTEPS-6934, FRONTAC-35452, \
            MICRO-40718, TEI-5023, FRONTCO-25641, FRONTAC-35453, WCS-8158, \
            MICRO-40696, INTEPS-6956, INTEPS-7191, FRONTAC-35573, FRONTRE-16982, \
            FRONTCO-25733, WEBMET-52, FRONTCO-25716, TEDTED-5145, INTEPS-7144, \
            INTEPS-7143, INTEPS-7261, FRONTAT-1135, INTEPS-7256, FCOM-20684, \
            FRONTAT-1109, MICRO-40896, TIAFOS-937, INTEPS-7255, CRM4TE-14159, \
            TIAFOS-943, KRATOS-10632, INTEPS-7224, KRATOS-10670, FRONTCO-25925, \
            FRONTOE-4319)'

    ficheros = 0
    response = jira.get_delivs(sJQL)
    if response.status_code == 200:
        issues = json.loads(response.text)
        
    for issue in issues["issues"]:
        # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
        nom_file = issue["key"] + "_delivs_news.json"
        load_to_json(configD.DIR_JIRA_DELIVS + nom_file, issue)
        print("Generando ... %s " % nom_file)  
        ficheros = ficheros + 1
        
    print("Fin. Se han generado %s ficheros" % ficheros)

if __name__ == '__main__':
    main()