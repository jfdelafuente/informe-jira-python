from utils.utils import log
import pandas as pd

def transform(data:pd.DataFrame) -> pd.DataFrame:
    df_filtrado = data[data["Status"]!= "Cancelled / Won't Do"]
    return df_filtrado

# Set of Data Quality Checks Needed to Perform Before Loading
def Data_Quality(load_df:pd.DataFrame):
    #Checking Whether the DataFrame is empty
    if load_df.empty:
        print('No Data Extracted')
        return False
    
    #Enforcing Primary keys since we don't need duplicates
    # if pd.Series(load_df['played_at']).is_unique:
    #    pass
    # else:
        #The Reason for using exception is to immediately terminate the program and avoid further processing
    #    raise Exception("Primary Key Exception,Data Might Contain duplicates")
    
    #Checking for Nulls in our data frame 
    if load_df.isnull().values.any():
        raise Exception("Null values found")
    return True