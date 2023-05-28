import api.JiraAPIHandler as jiraAPIHandler
import configD
from utils.utils import extract_from_csv, load_to_json, log
from etl.transform import Data_Quality

'''
    Proceso que consulta en Jira los Bugs asociadas a las INC 
    incluídas en el fichero "incidencias_in.csv" y genera un 
    fichero json en el directorio JSON/BUGS/INCxxxx.json
    
'''

def main():
    print("Inicio")
    ficheros = 0
    archivo = 'incidencias_in.csv'
    jira = jiraAPIHandler.JiraAPIHandler()
    df_epsilons = extract_from_csv(configD.DIR_JIRA_IN + archivo)
    if (Data_Quality(df_epsilons) == True):
        for index, row in df_epsilons.iterrows():
            row_inc = row['Incidencia']
            estatus, texto = jira.get_bug_to_json(row_inc)
            if estatus == 200:
                log("Trantado %s - %s - Estato : %s " % (index, row_inc, estatus))
                nom_fichero = row_inc+ "_bugs_new.json"
                load_to_json(configD.DIR_JIRA_BUGS + nom_fichero, texto)
                ficheros = ficheros + 1
        print("Fin. Procesadas %s incidencias" % ficheros)
    else:
        print("No se ha procesado ninguna incidencia.")
        
    
if __name__ == '__main__':
    main()