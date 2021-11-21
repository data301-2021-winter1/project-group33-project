# Imports
import os
from os import listdir
import pandas as pd
import datetime

months = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

def addMissingMonths(df):
    count = 0
    for year in df["Year"].unique():
        for province in df["Jurisdiction"].unique():
            if len(df[(df["Year"] == year) & (df["Jurisdiction"] == province)].index) != 12:
                for month in months:
                    if df[(df["Year"] == year) & (df["Jurisdiction"] == province) & (df["Month"] == month)].empty:
                        df = df.append({"Year" : year, "Jurisdiction" : province, "Month" : month, "Area (hectares)" : 0, "Number" : 0}, ignore_index=True)
                        count = count + 1
    return df

# Import and process functions

def loadAndProcessFireData(pathToDataDir):
    fireData = {}
    for f in listdir(pathToDataDir):
        if(f.endswith(".csv")):
            fireData[f] = (
                pd.read_csv(pathToDataDir + "/" + f)
                .pipe(lambda x : x.drop(columns = x.columns[[1,2,4,6,8,9,10]]))
                .loc[lambda x : x["Year"] != 2020]
                .loc[lambda x : x["Jurisdiction"] != "Parks Canada"]
            )
    return fireData

def loadAndProcessONIData(pathToONIDataFile):
    ONIData = (
        pd.read_csv(pathToONIDataFile, sep='\s+', header=8)
        .pipe(lambda x : x.drop(columns = x.columns[[2, 3, 4]]))
        .rename(columns = {"YEAR" : "Year", "MON/MMM" : "MonthNum", "PHASE" : "Phase"})
        .loc[lambda x : x["Phase"] != "M"]
        .assign(Month = lambda x: x["MonthNum"].map({
            1 : "January",
            2 : "February",
            3 : "March",
            4 : "April",
            5 : "May",
            6 : "June",
            7 : "July",
            8 : "August",
            9 : "September",
            10 : "October",
            11 : "November",
            12 : "December"
        }))
        .loc[:, ["Year", "Month", "ONI", "Phase", "MonthNum"]]
    )
    return ONIData

def createONIByYear(ONIData):
    ONIByYear = pd.DataFrame(columns = {"Year", "AvgONI", "Phase"})
    for year in range(ONIData["Year"].min(), ONIData["Year"].max()):
        avgONI = ONIData[ONIData["Year"] == year]["ONI"].sum()/12
        phase = "N"
        if avgONI <= -0.5:
            phase = "L"
        if avgONI >= 0.5:
            phase = "E"
        ONIByYear = ONIByYear.append({"Year" : year, "AvgONI" : avgONI, "Phase" : phase}, ignore_index=True)
    return ONIByYear

# Data Merging functions

def createDataByMonth(fireData, ONIData):
    df = addMissingMonths(
        pd.merge(
            fireData["NFD-Area_burned_by_month-ENFR.csv"], 
            fireData["NFD-Number_of_fires_by_month-ENFR.csv"]
        )
    ).merge(
        ONIData,
        how = "left",
        on = ["Year", "Month"]
    )
    df["Month"] = pd.Categorical(df['Month'], categories=months, ordered=True)
    return (
        df.sort_values(["Year", "Jurisdiction", "Month"])
        .assign(DateTime = lambda x : pd.to_datetime(dict(year=x["Year"], month=x["MonthNum"], day=1)))
        .pipe(lambda x : x.drop(columns = ["MonthNum"]))
    )
    

def createDataByCause(fireData, ONIByYear):
    return (
        pd.merge(
            fireData["NFD-Area_burned_by_cause_class-ENFR.csv"],
            fireData["NFD-Number_of_fires_by_cause_class-ENFR.csv"]
        ).merge(
            ONIByYear,
            how = "left",
            on = ["Year"]
        )
    )

def createDataBySize(fireData, ONIByYear):
    return ( 
        pd.merge(
            fireData["NFD-Area_burned_by_fire_size_class-ENFR.csv"],
            fireData["NFD-Number_of_fires_by_fire_size_class-ENFR.csv"]
        ).merge(
            ONIByYear,
            how = "left",
            on = ["Year"]
        )
    )