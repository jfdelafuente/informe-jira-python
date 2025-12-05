from utils.utils import log
import pandas as pd

def transform(data:pd.DataFrame) -> pd.DataFrame:
    df_filtrado = data[data["Status"]!= "Cancelled / Won't Do"]
    return df_filtrado

# Set of Data Quality Checks Needed to Perform Before Loading
def Data_Quality(load_df:pd.DataFrame):
    """Valida la calidad de los datos antes de cargar"""
    # Checking Whether the DataFrame is empty
    if load_df.empty:
        print('No Data Extracted')
        return False

    # Checking for Nulls in our data frame
    if load_df.isnull().values.any():
        raise Exception("Null values found")
    return True

def eliminar_duplicados(df:pd.DataFrame) -> pd.DataFrame:
    """Elimina filas duplicadas del DataFrame"""
    return df.drop_duplicates()