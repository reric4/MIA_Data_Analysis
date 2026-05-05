#Importing the needed libraries
import pandas as pd
import matplotlib.pyplot as plt
<<<<<<< Updated upstream
#import plotly.graph_objects as go
=======
import us
import geopandas
import re
#assign file path
file = "AZ-ALWY.xlsx"
usmapfile = "us-states.json"
worldmapfile = "countries.geojson"

#Note for purposes of this analysis Army Air Force and Air Force have been combined together 

#---------------------------------------------------------------------------------------

#IMPORTING EXCEL
>>>>>>> Stashed changes

#importing excel sheets as dataframes
byalph = pd.read_excel(file, "A-Z", index_col=None, na_values=["NA"]) 
bystate = pd.read_excel(file, "AL-WY", index_col=None, na_values=["NA"]) 

#print info (column names and numbers of the dataframes)
#az_info = byalph.info()
#alwy_info = bystate.info()

#---------------------------------------------------------------------------------------

#MERGING INTO ONE DF

#merge dfs on the columns Last_Name, First_Name, and Conflict as these are the only columns that are present in both dataframes and printing the df info
merged = byalph.merge(bystate, how='outer', on=["Last_Name","First_Name","Conflict"])
<<<<<<< Updated upstream
#joined_info = merged.info()
#drop duplicate rows based upon service number (using last name to counter nan issues) and print df info
cleaned = merged.drop_duplicates(subset=["Last_Name", "Service_Number"])
#dedupe_info = cleaned.info()
#remove all non-us records and print df info
cleaned = cleaned.drop(cleaned[(cleaned.Home_of_Record == "NON-US")].index)
#us_info = cleaned.info()
#remove all records that have null states and print info
cleaned = cleaned.dropna(subset = ["State", "Conflict"])
#states_info = cleaned.info()
=======

#print info
merged.info()

#---------------------------------------------------------------------------------------

#CLEANING

#drop duplicate rows based upon service number (using last name to counter nan issues) and print df info
cleaned = merged.drop_duplicates(subset=["Last_Name", "Service_Number"])
cleaned.info()

#remove all non-us records and print df info
cleaned = cleaned.drop(cleaned[(cleaned.Home_of_Record == "NON-US")].index)
cleaned.info()

#remove all records that have null states and print info
cleaned = cleaned.dropna(subset = ["State", "Conflict"])
cleaned.info()
>>>>>>> Stashed changes

#---------------------------------------------------------------------------------------

#ANONOMIZING

#drop names and service numbers in order to anonomize data, as well as Unit, since the unit data is not currently standardized and to do so would take massibe amounts of time, and Home of Record since it is duplicated by state to a degree and state is a more accurate identifier, and Rank since it s not standardized, nor currently in use in this analysis
todrop = ["Last_Name", "First_Name", "Service_Number", "Unit", "Home_of_Record", "Rank"]
anon = cleaned.drop(columns=todrop)
<<<<<<< Updated upstream
anon["Date_of_Loss"]=pd.to_datetime(anon["Date_of_Loss"])
anon["Year_of_Loss"]=anon["Date_of_Loss"].dt.year
anon["Date_of_Loss"]=anon["Date_of_Loss"].dt.date
#anon_info = anon.info()

#export anonomized data to an excel spreadsheet 
#anon.to_excel("mia_anon.xlsx")


conflictcount = anon.groupby("Conflict").agg(Count=("State","count"))
conflictcount["startyear"]=[1947,1950,1991,1986,2003,1955,1939]
conflictcount["endyear"]=[1991,1953,1991,1986,2011,1975,1945]

servicecount = anon.groupby("Service").agg(Count=("State","count"))
                                           
statecount = anon.groupby("State").agg(Count=("Conflict","count"))

yearcount = anon.groupby("Year_of_Loss").agg(Count=("State","count"))

datecount = anon.groupby("Date_of_Loss").agg(Count=("State","count"))

locationcount = anon.groupby("Location").agg(Count=("State","count"))

# cnfplt = conflictcount.sort_values("startyear",  ascending=False).plot(
#     title="Losses per Conflict",
#     kind="barh",
#     y="Count",
#     legend=False,
#     color="tan"
#     )
# for p in cnfplt.patches:
#     value = p.get_width()
#     cnfplt.annotate(
#         str(value),
#         (value, p.get_y() + p.get_height() / 2),
#         ha="left", va="center", xytext=(5, 0), textcoords="offset points")
# cnfplt.set_xlim( conflictcount["Count"].max() * 1.15, 0)
# cnfplt.invert_xaxis()
# plt.show()

def pielegpct(data, title):
    pcts = (data/data.sum()*100).round(1)
    leglab = [f"{label} ({pct}%)" for label, pct in zip(data.index, pcts)]
    
    plt.pie(data,labels=data.index, labeldistance=None)
    plt.legend(leglab, bbox_to_anchor=(1,1.1), loc="upper left")
    plt.title(title)
    
    plt.tight_layout(
        )

# pielegpct(servicecount["Count"], "Distribution of Loss by Services")
# plt.show
=======

#Additionally a year of loss column is added for further analysis after guarenteeing that date of loss is in date-time formate to be properly parsed and the state name is added to simplify mapping
anon["Date_of_Loss"]=pd.to_datetime(anon["Date_of_Loss"])
anon["Year_of_Loss"]=anon["Date_of_Loss"].dt.year
anon["Date_of_Loss"]=anon["Date_of_Loss"].dt.date
anon["State_Name"] = anon["State"].map(lambda x: us.states.lookup(x).name)
anon.info()

#export anonomized data to an excel spreadsheet (I keep it commented out because unless things have changed, it doesn't need to be updated)
#anon.to_excel("mia_anon.xlsx")

#---------------------------------------------------------------------------------------

#AGGREGATION

conflictcount = anon.groupby("Conflict").agg(Count=("State","count"))
conflictcount["Start_Year"]=[1947,1950,1991,1986,2003,1955,1939]
conflictcount["End_Year"]=[1991,1953,1991,1986,2011,1975,1945]

print(conflictcount)

servicecount = anon.groupby("Service").agg(Count=("State","count"))
             
print(servicecount)
                              
statecount = anon.groupby("State").agg(Count=("Conflict","count"))

statecount["State_Name"] = statecount.index.map(lambda x: us.states.lookup(x).name)

#showing first 10 numerically
print(statecount.sort_values("Count", ascending=False)[:10])

yearcount = anon.groupby("Year_of_Loss").agg(Count=("State","count"))

#showing first 10 numerically
print(yearcount.sort_values("Count", ascending=False)[:10])

datecount = anon.groupby("Date_of_Loss").agg(Count=("State","count"))

#showing first 10 numerically
print(datecount.sort_values("Count", ascending=False)[:10])

locationcount = anon.groupby("Location").agg(Count=("State","count"))

locationcount.index = locationcount.index.str.title()

#showing first 10 numerically
print(locationcount.sort_values("Count", ascending=False)[:10])

#---------------------------------------------------------------------------------------

#VISUALIZATION

cnfplt = conflictcount.sort_values("Start_Year",  ascending=False).plot(title="Missing per Conflict",
    kind="barh", y="Count", legend=False, color="grey")

for p in cnfplt.patches:
    value = p.get_width()
    cnfplt.annotate(str(value), (value, p.get_y() + p.get_height() / 2), ha="left", va="center", 
                    xytext=(5, 0), textcoords="offset points")
cnfplt.set_xlim(conflictcount["Count"].max() * 1.15, 0)
cnfplt.invert_xaxis()
plt.show()

#---

def pielegpct(data, title):
    pcts = (data/data.sum()*100).round(2)
    leglab = [f"{label} ({pct}%)" for label, pct in zip(data.index, pcts)]
    plt.pie(data,labels=data.index, labeldistance=None)
    plt.legend(leglab, bbox_to_anchor=(1,1.1), loc="upper left")
    plt.title(title)
    plt.tight_layout()
pielegpct(servicecount["Count"], "Distribution of Missing by Services")
plt.show()

#---

print("Missing by State")
usmap = geopandas.read_file(usmapfile)
usmaps = usmap.merge(statecount.reset_index(), left_on="name", right_on="State_Name", how="left")
usmaps.drop(columns={"density","State","State_Name", "id"}, inplace=True)
usmaps.rename(columns={"Count":"Missing"}, inplace=True)

usmaps.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

yearcount.plot(kind="line", y="Count", title="Missing by Year", legend=False)
plt.show()

#---

datecount.plot(kind="line", y="Count", title="Missing by Date", legend=False)
plt.show()

#---

locmatching = {
  'Baker Island': 'United States Minor Outlying Islands', 
  'Wake Island':'United States Minor Outlying Islands', 
  'Martinique': "France", #not technically, but I think on this map it is included 
  'Korea': "South Korea", 
  'Tokelau': "New Zealand", 
  'Johnston Atoll': 'United States Minor Outlying Islands', 
  'Serbia': 'Republic of Serbia', 
  'Czech Republic': 'Czechia', 
  'Federated States Of Micronesia':'Federated States of Micronesia',
  'Saint Helena, Ascension, And Tristan Da Cunha':'Saint Helena',  
  'Trinidad And Tobago':'Trinidad and Tobago', 
  'Bosnia And Herzegovina':'Bosnia and Herzegovina', 
  'United States':'United States of America', 
  'Curacao':'Curaçao', 
  'Wallis And Futuna':'Wallis and Futuna', 
  'French Guiana': "France",# this is not geographically part of France, but I am fairly certain that it is included geographically 
  'Hong Kong':'Hong Kong S.A.R.', 
  'Palmyra Atoll':'United States Minor Outlying Islands', 
  'U.S. Virgin Islands': 'United States Virgin Islands', 
  'Midway Islands': 'United States Minor Outlying Islands', 
  'Burma':'Myanmar', 
  'Christmas Island': "Australia"
  }
maplocationcount=locationcount
maplocationcount = maplocationcount.rename(index=locmatching)
maplocationcount = maplocationcount.groupby(level=0).sum()

worldmap = geopandas.read_file(worldmapfile)
worldmap = worldmap.merge(maplocationcount.reset_index(), left_on="name", right_on="Location", 
                          how="left")
fig, ax = plt.subplots(figsize=(15, 10))
worldmap.plot(column='Count', ax=ax, legend=True, cmap='YlOrRd', edgecolor='k')
ax.set_title('Missing by Location')
ax.set_axis_off()
plt.show()

locplt = locationcount.sort_values("Count",  ascending=False).plot( 
    title="Complete Missing per Location", kind="barh", y="Count", legend=False, color="gray", 
    figsize=(5,25))
for p in locplt.patches:
    value = p.get_width()
    locplt.annotate(str(value), (value, p.get_y() + p.get_height() / 2), ha="left", va="center",
                    xytext=(5, 0), textcoords="offset points")
locplt.set_xlim( locationcount["Count"].max() * 1.15, 0)
locplt.invert_xaxis()

#---------------------------------------------------------------------------------------

#ANALYSIS

analysis=anon
analysis["Service"]=analysis["Service"].str.replace("UNITED STATES ", "")
analysis["Service"]=analysis["Service"].str.replace(" RESERVE", "")

bysvc = analysis.groupby("Service")

ww2 = analysis[analysis["Conflict"]=="WORLD WAR II"]
kwar = analysis[analysis["Conflict"]=="KOREAN WAR"]
vwar = analysis[analysis["Conflict"]=="VIETNAM WAR"]
owar = analysis[analysis["Conflict"]!="WORLD WAR II"]
owar = owar[owar["Conflict"]!="KOREAN WAR"]
owar = owar[owar["Conflict"]!="VIETNAM WAR"]

usaf = analysis[analysis["Service"]=="AIR FORCE"]
usarmy = analysis[analysis["Service"]=="ARMY"]
usnavy = analysis[analysis["Service"]=="NAVY"]
usmc = analysis[analysis["Service"]=="MARINE CORPS"]
osvc = analysis[analysis["Service"]!="AIR FORCE"]
osvc = osvc[osvc["Service"]!="ARMY"]
osvc = osvc[osvc["Service"]!="NAVY"]
osvc = osvc[osvc["Service"]!="MARINE CORPS"]
osvc = osvc.dropna(subset=["Service"])

#---

srv_cnf = pd.crosstab(analysis["Conflict"], analysis["Service"],normalize="index").round(4)*100
print(srv_cnf)

#Pie charts showing the distributon of service missing per conflit
for name, group in bysvc:
    fig, ax = plt.subplots(figsize=(5,5))
    catcount=group["Conflict"].value_counts(normalize=True)*100
    catcount=catcount.round(2)
    leglab=[f"{cat} ({count}%)" for cat, count in catcount.items()]
    wedges, autotexts = ax.pie(catcount, startangle=90)
    ax.legend(wedges, leglab, loc="upper left", bbox_to_anchor=(1, 0, 0.5, 1))
    plt.title(f"{name}")
    plt.show()
    
#Interactive maps showing the missing quantities per conflict

ww2st=ww2.groupby("State").agg(Count=("State_Name","count"))
ww2st["State_Name"] = ww2st.index.map(lambda x: us.states.lookup(x).name)
ww2_stmap = usmap.merge(ww2st.reset_index(), left_on="name", right_on="State_Name", how="left")
ww2_stmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
ww2_stmap.rename(columns={"Count":"Missing"}, inplace=True)
ww2_stmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

kwarst=kwar.groupby("State").agg(Count=("State_Name","count"))
kwarst["State_Name"] = kwarst.index.map(lambda x: us.states.lookup(x).name)
kwar_stmap = usmap.merge(kwarst.reset_index(), left_on="name", right_on="State_Name", how="left")
kwar_stmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
kwar_stmap.rename(columns={"Count":"Missing"},inplace=True)
kwar_stmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

vwarst=vwar.groupby("State").agg(Count=("State_Name","count"))
vwarst["State_Name"] = vwarst.index.map(lambda x: us.states.lookup(x).name)
vwar_stmap = usmap.merge(vwarst.reset_index(), left_on="name", right_on="State_Name", how="left")
vwar_stmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
vwar_stmap.rename(columns={"Count":"Missing"},inplace=True)
vwar_stmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

owarst=owar.groupby("State").agg(Count=("State_Name","count"))
owarst["State_Name"] = owarst.index.map(lambda x: us.states.lookup(x).name)
owar_stmap = usmap.merge(owarst.reset_index(), left_on="name", right_on="State_Name", how="left")
owar_stmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
owar_stmap.rename(columns={"Count":"Missing"},inplace=True)
owar_stmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---


# Interactive maps showing the breakdown by service

afst=usaf.groupby("State").agg(Count=("State_Name","count"))
afst["State_Name"] = afst.index.map(lambda x: us.states.lookup(x).name)
afstmap = usmap.merge(afst.reset_index(), left_on="name", right_on="State_Name", how="left")
afstmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
afstmap.rename(columns={"Count":"Missing"},inplace=True)
afstmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

armyst=usarmy.groupby("State").agg(Count=("State_Name","count"))
armyst["State_Name"] = armyst.index.map(lambda x: us.states.lookup(x).name)
armystmap = usmap.merge(armyst.reset_index(), left_on="name", right_on="State_Name", how="left")
armystmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
armystmap.rename(columns={"Count":"Missing"},inplace=True)
armystmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

navyst=usnavy.groupby("State").agg(Count=("State_Name","count"))
navyst["State_Name"] = navyst.index.map(lambda x: us.states.lookup(x).name)
navystmap = usmap.merge(navyst.reset_index(), left_on="name", right_on="State_Name", how="left")
navystmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
navystmap.rename(columns={"Count":"Missing"},inplace=True)
navystmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

mcst=usmc.groupby("State").agg(Count=("State_Name","count"))
mcst["State_Name"] = mcst.index.map(lambda x: us.states.lookup(x).name)
mcstmap = usmap.merge(mcst.reset_index(), left_on="name", right_on="State_Name", how="left")
mcstmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
mcstmap.rename(columns={"Count":"Missing"},inplace=True)
mcstmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

otherst=osvc.groupby("State").agg(Count=("State_Name","count"))
otherst["State_Name"] = otherst.index.map(lambda x: us.states.lookup(x).name)
otherstmap = usmap.merge(otherst.reset_index(), left_on="name", right_on="State_Name", how="left")
otherstmap.drop(columns={"State_Name", "State", "id", "density"},inplace=True)
otherstmap.rename(columns={"Count":"Missing"},inplace=True)
otherstmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

#Interactive maps showing the missing quantities per location

ww2loc=ww2.groupby("Location").agg(Count=("State_Name","count"))
ww2_locmap =worldmap.merge(maplocationcount.reset_index(), left_on="name", right_on="Location",
    how="left")
ww2_locmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
ww2_locmap.rename(columns={"Count_y":"Missing"}, inplace=True)
ww2_locmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

kwarloc=kwar.groupby("Location").agg(Count=("State_Name","count"))

kwar_locmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

kwar_locmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
kwar_locmap.rename(columns={"Count_y":"Missing"},inplace=True)

kwar_locmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

vwarloc=vwar.groupby("Location").agg(Count=("State_Name","count"))

vwar_locmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

vwar_locmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
vwar_locmap.rename(columns={"Count_y":"Missing"},inplace=True)

vwar_locmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

owarloc=owar.groupby("Location").agg(Count=("State_Name","count"))


owar_locmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

owar_locmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
owar_locmap.rename(columns={"Count_y":"Missing"},inplace=True)

owar_locmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---


# Interactive maps showing the breakdown by service

afloc=usaf.groupby("Location").agg(Count=("State_Name","count"))


aflocmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

aflocmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
aflocmap.rename(columns={"Count_y":"Missing"},inplace=True)

aflocmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

armyloc=usarmy.groupby("Location").agg(Count=("State_Name","count"))


armylocmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

armylocmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
armylocmap.rename(columns={"Count_y":"Missing"},inplace=True)

armylocmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

navyloc=usnavy.groupby("Location").agg(Count=("State_Name","count"))


navylocmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

navylocmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
navylocmap.rename(columns={"Count_y":"Missing"},inplace=True)

navylocmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

mcloc=usmc.groupby("Location").agg(Count=("State_Name","count"))

mclocmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

mclocmap.drop(columns={"ISO3166-1-Alpha-2","ISO3166-1-Alpha-3", "Location_y", "Count_x", "Location_x"},inplace=True)
mclocmap.rename(columns={"Count_y":"Missing"},inplace=True)

mclocmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)

#---

otherloc=osvc.groupby("Location").agg(Count=("State_Name","count"))

otherlocmap = worldmap.merge(
    maplocationcount.reset_index(),
    left_on="name",
    right_on="Location",
    how="left"
    )

otherlocmap.drop(columns={"ISO3166-1-Alpha-2", "ISO3166-1-Alpha-3","Location_y", "Count_x", "Location_x"},inplace=True)
otherlocmap.rename(columns={"Count_y":"Missing"},inplace=True)

otherlocmap.explore(column="Missing", legend=True, cmap="YlOrRd", tiles="OpenStreetMap", tooltip=True)
>>>>>>> Stashed changes
