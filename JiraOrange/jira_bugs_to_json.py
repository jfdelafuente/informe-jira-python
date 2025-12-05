import configD
import time
import api.JiraAPIHandler as jiraAPIHandler
from utils.utils import extract_from_csv, load_to_json, log
from etl.transform import Data_Quality

'''
    Proceso que consulta en Jira los Bugs asociadas a las 
    INCIDENCIAS EPSILON incluídas en el fichero 
    "incidencias_in.csv" y genera un fichero json en el 
    directorio "JSON/BUGS/INCxxxx.json"
'''

def main():
    print("Inicio consulta incidencias ...")
    start_time = time.time()
    ficheros = 0
    archivo = 'incidencias_in.csv'

    try:
        df_epsilons = extract_from_csv(configD.DIR_JIRA_IN + archivo)
        print(f'Leyendo ... {archivo}')

        if not Data_Quality(df_epsilons):
            print("Error: No se pudo validar la calidad de los datos")
            return

        print('Data Quality OK')

        try:
            jira = jiraAPIHandler.JiraAPIHandler()
        except ValueError as e:
            print(f"Error de configuración: {e}")
            return

        for index, row in df_epsilons.iterrows():
            row_inc = row['Incidencia']
            # Conectamos con Jira para obtener los bugs asociados a las incidencias
            try:
                estatus, texto = jira.get_bug_to_json(row_inc)
                if estatus == 200:
                    log("Tratado %s - %s - Estado: %s" % (index+1, row_inc, estatus))
                    nom_fichero = row_inc + "_bugs_new.json"
                    load_to_json(configD.DIR_JIRA_BUGS + nom_fichero, texto)
                    ficheros = ficheros + 1
                else:
                    log("Error %s - %s - Estado: %s" % (index+1, row_inc, estatus))
                    print(f"Error en incidencia {row_inc}: Status {estatus}")
            except Exception as e:
                log(f"Error procesando {row_inc}: {e}")
                print(f"Error procesando incidencia {row_inc}: {e}")
                continue

        print(f"Fin. Procesadas {ficheros} incidencias")
        print("COPY duration: {} seconds".format(time.time() - start_time))

    except FileNotFoundError:
        print(f"Error: No se encontró el archivo {archivo} en {configD.DIR_JIRA_IN}")
    except Exception as e:
        print(f"Error inesperado: {e}")
        import traceback
        traceback.print_exc()        
    
        
    
if __name__ == '__main__':
    main()