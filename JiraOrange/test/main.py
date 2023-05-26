import pandas as pd
import configD

archivo = 'bugs.xlsx'
archivo_salida = 'bugs_out.csv'


def main():

    lista_inc = []
    lista_bug = []
    lista_status = []
    df_salida = pd.DataFrame()
    
    ''' Cargamos el ficheor de entrada en un DataFrame '''
    df = pd.read_excel(configD.DIR_JIRA_IN + archivo)
  
    ''' Recorremos el DataFrame para separar el campo Bugs en los campos Bugs y Status '''
    for index, row in df.iterrows():
        # print("Incidencia: %s  -  Bugs: %s " % (row['Incidencia'], row['Bug']))
        row_inc = row['Incidencia']
        row_string = row['Bug']
        bugs_list = row_string.split('\n')
        bugs_list.pop()
        bugs_list_escape = list(map(lambda x : x.strip(), bugs_list))

        for bug in bugs_list_escape:
            jira, status = bug.split(' [')
            status = ''.join( x for x in status if x not in ']')
            status_escape = status.strip()
            lista_inc.append(row_inc)
            lista_bug.append(jira)
            lista_status.append(status_escape)
            
       
    # imprimimos por pantalla los bugs en un string
    string_lista_bug = ""
    for i in lista_bug:
        string_lista_bug = string_lista_bug + ", " + i
    print(string_lista_bug)

  
    df_salida['Incidencias'] = lista_inc
    df_salida['Bugs'] = lista_bug
    df_salida['Status'] = lista_status
    print(df_salida)
    ''' Volcamos la informacion en el fichero de salida '''
    df_salida.to_csv(configD.DIR_JIRA_OUT + archivo_salida, sep=';', encoding='utf-8', index=False)

if __name__ == '__main__':
    main()