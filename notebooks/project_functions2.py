import pandas as pd
import numpy as np

def raw(file):
    df = pd.read_csv(file)
    return df

def intial_process(df1,df2):
    # Merges two datasets and THEN drops all common un-needed columns
    df=pd.concat([df1,df2['Number']],axis='columns').drop(["AnnÈe","ISO","Juridiction","Data Qualifier","Qualificatifs de donnÈes","Superficie (en hectare)"],axis='columns')
    
    # check = pd.concat([Area_by_cause,Number_by_cause['Number']],axis='columns')
    return df

def drop_origine(df):
    # Drops rows where the Cause column has value Unspecified and Reburn, and then drops the column titled 'Origine'
    df=df[ (df["Cause"]!="Unspecified") & (df["Cause"]!="Reburn") ].drop("Origine",axis='columns')
    return df

def drop_french_firesize(df):
    # Drops rows where the Fire size class has value 'Unspecified' and drops the column titled 'Classe de superficie ‡ l'extinction '   
    df=df[df["Fire size class"]!="Unspecified"].drop("Classe de superficie ‡ l\'extinction ",axis='columns')
    return df
    

def drop_mois(df):
    # Drops rows where the Month column has value 'Unspecified' and drops the column titled 'Mois' 
    df=df[df['Month']!="Unspecified"].drop("Mois",axis='columns')
    return df

