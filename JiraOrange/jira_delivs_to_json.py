import json
import configD
import api.JiraAPIHandler as jiraAPIHandler
from utils.utils import load_to_json

'''
    Proceso que consulta en JIRA las DELIVs asociados a los BUGs de entrada y
    genera un fichero pra cada DELIV en el directorio "JSON/DELIVS/DELIV-XXXXX.json
'''

def main():
    print("Inicio")
    ficheros = 0

    try:
        # Inicializamos Jira
        jira = jiraAPIHandler.JiraAPIHandler()
    except ValueError as e:
        print(f"Error de configuración: {e}")
        return

    # JQL para buscar deliveries asociadas a bugs
    sJQL = 'type = Delivery AND "Bug/s" in (WCS-9489, INTEPS-14777, CRM4TE-22756, INTEPS-14788, MIDOSS-6575, \
INTEPS-14844, KRATOS-13746, TMCSDS-715, MICRO-49163, INTEPS-14774, \
INTEPS-14791, INTEPS-14846, ARCLMU-39101, INTEPS-14968, INTEPS-14794, \
ARCLMU-39135, INTEPS-14877, FRONTCO-33732, INTEPS-14849, INTEPS-14865, \
INTEPS-14790, WCS-9487, INTEPS-14847, INTEPS-14879, INTEPS-14862, \
FRONTMC-18773, TEI-7939, FRONTCO-33908, FRONTMC-18775, FDCOSP-1083, \
INTEPS-14913, MICRO-49228, INTEPS-15059, FRONTAT-2263, PAEOSP-20558, \
PAEOSP-20552, TEDTED-8012, FCOM-25211, TEI-7951, FRONTRE-25415)'

    try:
        response = jira.get_delivs(sJQL)
        if response.status_code == 200:
            try:
                issues = response.json()
                for issue in issues["issues"]:
                    nom_file = issue["key"] + "_delivs_news.json"
                    load_to_json(configD.DIR_JIRA_DELIVS + nom_file, issue)
                    print("Generando ... %s " % nom_file)
                    ficheros = ficheros + 1
            except (json.JSONDecodeError, KeyError) as e:
                print(f"Error procesando respuesta de Jira: {e}")
        else:
            print(f"Error en la consulta a Jira: Status {response.status_code}")
            print(f"Respuesta: {response.text}")

        print("Fin. Se han generado %s ficheros" % ficheros)

    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    main()