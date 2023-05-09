import pandas as pd
import json
import JiraAPIHandler as jiraAPIHandler

archivo = 'incidencias_in.xlsx'
archivo_salida = 'incidenicas_out.csv'

def funcionVariasConsultas(jira, df):
    error = 200
    for index, row in df.iterrows():
        row_inc = row['Incidencia']
        print(row_inc)
        response = jira.get_bug(row_inc)
        if response.status_code == 200:
            issue = json.loads(response.text)
            # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
        else:
            error = response.status_code
    return error, issue
    
def funcionUnaConsulta(jira, df):
    response = jira.get_bugs(df)
    if response.status_code == 200:
            issue = json.loads(response.text)
            # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    return response.status_code, issue

def funcionUnEpsilon(jira, epsilon):
    response = jira.get_bug(epsilon)
    if response.status_code == 200:
            issue = json.loads(response.text)
            # print(json.dumps(issue, sort_keys=True, indent=4, separators=(",", ": ")))
    return response.status_code, issue
  

def crear_fichero(texto):
    
    if texto["maxResults"] > texto["total"]:
        contar = texto["total"]
    else:
        contar = texto["maxResults"]
    print("contar : %s" % contar)
    
    lista_inc = []
    lista_bug = []
    lista_status = []
    lista_resolution = []
    
    if contar > 0:
        for j in range(0, contar):
            vNumIncidencia = texto["issues"][j]["fields"]["customfield_11104"]
            vIssueKey = texto["issues"][j]["key"]
            # print("%s - vIssueKey:  %s - vNumIncidencia:  %s" %  (j, vIssueKey, vNumIncidencia))
            if vIssueKey != "":
                if (texto["issues"][j]["fields"]["status"]) is not None:
                    vstatus = texto["issues"][j]["fields"]["status"]["name"]
                else:
                    vstatus = ""
                if (texto["issues"][j]["fields"]["resolution"]) is not None:
                    vresolution = texto["issues"][j]["fields"]["resolution"]["name"]
                else:
                    vresolution = ""
                vListaBugs = vIssueKey + " [ " + vstatus + " / " + vresolution + " ] "
                print("%s - vIssueKey:  %s - vNumIncidencia:  %s - vListaBugs: %s" %  (j, vIssueKey, vNumIncidencia, vListaBugs))
                lista_inc.append(vNumIncidencia)
                lista_bug.append(vIssueKey)
                lista_status.append(vstatus)
                lista_resolution.append(vresolution)
        
        return lista_inc, lista_bug, lista_status, lista_resolution 


def main():
    
    print("Inicio")
    jira = jiraAPIHandler.JiraAPIHandler()
    df_epsilons = pd.read_excel(archivo)
    # epsilons = { 'Incidencia' : ["INC000002785241", "INC000002783177", "INC000002785242", "INC000002783037"] }
    # df_epsilons = pd.DataFrame(epsilons)
    estatus, texto = funcionUnaConsulta(jira, df_epsilons)

    with open("orders_new.json", 'w') as file:
        json.dump(texto, file)
        
    if estatus == 200:
        df_salida = pd.DataFrame()
        lista_inc, lista_bug, lista_status, lista_resolution = crear_fichero(texto)
        df_salida['Incidencias'] = lista_inc
        df_salida['Bugs'] = lista_bug
        df_salida['Status'] = lista_status
        df_salida['Resolution'] = lista_resolution
        df_salida.to_csv(archivo_salida, sep=';', encoding='utf-8', index=False)         
    else:
        print("La consulta no devuelve datos.")
        
        

    
if __name__ == '__main__':
    main()