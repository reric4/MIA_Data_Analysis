#assign file path
file = "AZ-ALWY.xlsx"
#Importing the needed libraries
import pandas as pd

#importing excel sheets as dataframes
byalph = pd.read_excel(file, "A-Z", index_col=None, na_values=["NA"]) 
bystate = pd.read_excel(file, "AL-WY", index_col=None, na_values=["NA"]) 

#print info (column names and numbers of the dataframes)
az_info = byalph.info()
alwy_info = bystate.info()

#merge dfs on the columns Last_Name, First_Name, and Conflict as these are the only columns that are present in both dataframes and printing the df info
merged = byalph.merge(bystate, how='outer', on=["Last_Name","First_Name","Conflict"])
joined_info = merged.info()
#drop duplicate rows based upon service number (using last name to counter nan issues) and print df info
cleaned = merged.drop_duplicates(subset=["Last_Name", "Service_Number"])
dedupe_info = cleaned.info()
#remove all non-us records and print df info
cleaned = cleaned.drop(cleaned[(cleaned.Home_of_Record == "NON-US")].index)
us_info = cleaned.info()
#remove all records that have null states and print info
cleaned = cleaned.dropna(subset = ["State", "Conflict"])
states_info = cleaned.info()

#drop names and service numbers in order to anonomize data, as well as Unit, since the unit data is not currently standardized and to do so would take massibe amounts of time, and Home of Record since it is duplicated by state to a degree and state is a more accurate identifier, aand Rank since it s not standardized, nor currently in use in this analysis
todrop = ["Last_Name", "First_Name", "Service_Number", "Unit", "Home_of_Record", "Rank"]
anon = cleaned.drop(columns=todrop)
anon_info = anon.info()

#export anonomized data to an excel spreadsheet 
anon.to_excel("mia_anon.xlsx")

print([az_info,alwy_info, joined_info, dedupe_info, us_info, states_info, anon_info])