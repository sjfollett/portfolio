import pandas as pd
import pandas_datareader as web
import matplotlib.pyplot as plt
import seaborn as sb
import pybaseball
from pybaseball import playerid_lookup
from pybaseball import statcast_pitcher
from pybaseball import statcast
pybaseball.cache.enable()

# #Lookup-player id
# df_player = playerid_lookup('Loup','Aaron')
#
# #Write to CSV file so you can read player id
# df_player.to_csv("AaronLoup.csv")
#
# #put player id into statcast to get data
# loup_stats = statcast_pitcher(start_dt="2022-01-01", end_dt="2022-06-27", player_id=571901)
#
# #write stats to CSV
# loup_stats.to_csv("Loup2021.csv")

# read csv file to manipulate it in pandas
dfOne = pd.read_csv("Mayers2022.csv")

# convert statcast data into movement in inches
dfOne["Horizontal Movement"] = dfOne["pfx_x"]*-12
dfOne["Vertical Movement"] = dfOne["pfx_z"]*12

# take only the columns you want
dfTwo = dfOne[["pitch_name", "Horizontal Movement", "Vertical Movement"]]

# write conditions by pitch type
Cutter = dfTwo["pitch_name"] == "Cutter"
Sinker = dfTwo["pitch_name"] == "Slider"
Curveball = dfTwo["pitch_name"] == "4-Seam Fastball"
Changeup = dfTwo["pitch_name"] == "Curveball"

# put the pitches back into dataframe
dfCutter = dfTwo[Cutter]
dfSinker = dfTwo[Sinker]
dfCurveball = dfTwo[Curveball]
dfChangeup = dfTwo[Changeup]

# plot the pitches
sb.set(style="darkgrid")
ax = dfCutter.plot.scatter(x="Horizontal Movement", y="Vertical Movement", c="r", label="Cutter")
dfSinker.plot.scatter(x="Horizontal Movement", y="Vertical Movement", c="b", ax=ax, label="Slider")
dfChangeup.plot.scatter(x="Horizontal Movement", y="Vertical Movement", c="g", ax=ax, label="Curveball")
dfCurveball.plot.scatter(x="Horizontal Movement", y="Vertical Movement", c="y", ax=ax, label="4-Seam Fastball")
plt.legend()
# plt.legend(bbox_to_anchor=(1.02, .1), loc="lower left", borderaxespad=0)
# sb.relplot(data=dfTwo, x=dfTwo["Horizontal Movement"], y=dfTwo["Vertical Movement"], hue=dfTwo["pitch_name"])
plt.title("Mike Mayers 2021 Pitch Movement (Pitcher's View)")
plt.show()
