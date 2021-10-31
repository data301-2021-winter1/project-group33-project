import pandas as pd
import numpy as np

def raw(file):
    df = pd.read_csv(file)
    return df

def intial_process(df1,df2):
    """
    Merges two datasets and THEN drops all common un-needed columns,
    Renames ISO column to Location,
    Renames Area column to Area_hectares
    Drops values of areas where insignificant fires occured
    Drops all values of Prince Edward Island as these are insufficient for our analysis
    
    """
    df=(pd.concat([df1,df2['Number']],axis='columns')
    .drop(["AnnÈe","Jurisdiction","Juridiction","Data Qualifier","Qualificatifs de donnÈes","Superficie (en hectare)"],axis='columns')
    .rename(columns={'ISO':"Location"})
    .rename(columns={'Area (hectares)':"Area_hectares"})
    .query('Area_hectares >=0.02')
    .query('Location != "PE" ')    
        
        
       )
    
    return df

def drop_origine(df):
    """
    Drops rows where the Cause column has value Unspecified and Reburn, and then drops the column titled 'Origine'
    
    """
    df=df[ (df["Cause"]!="Unspecified") & (df["Cause"]!="Reburn") ].drop("Origine",axis='columns')
    return df


def percent_calc(x):
    """
    This function takes in combined dataset and for number of fires columns, calculates a new column showing percentage of fires for each fire observation
    
    """
    array = x['Location'].unique().tolist()
    # array = ['PC',"BC","AB","SK","MB",'ON','QC','NB','NS','PE','NL','NT','YT']
    
    sum_provinces = []
    for province in array:
        i=x[x['Location']==province]['Number'].sum()
        sum_provinces.append(i)
    print(array)
    print(sum_provinces)
    
    percentage_list=[]
    
    for i in range(len(array)):
        
        df2=x[x['Location']==array[i]]['Number']
        
        df2=df2.tolist() # this was originally a pandas series..had to use .type to convert to figure out the kind and then convert it to list

        for j in range(len(df2)):
            
           # print(df2[j])
            # print(sum_provinces[i])
            
            percentage = (df2[j]/sum_provinces[i])*100 
            
            percentage_list.append(percentage)  
            
    return percentage_list




def drop_french_firesize(df):
    # Drops rows where the Fire size class has value 'Unspecified' and drops the column titled 'Classe de superficie ‡ l'extinction '   
    df=df[df["Fire size class"]!="Unspecified"].drop("Classe de superficie ‡ l\'extinction ",axis='columns')
    return df
    

def drop_mois(df):
    # Drops rows where the Month column has value 'Unspecified' and drops the column titled 'Mois' 
    df=df[df['Month']!="Unspecified"].drop("Mois",axis='columns')
    return df

