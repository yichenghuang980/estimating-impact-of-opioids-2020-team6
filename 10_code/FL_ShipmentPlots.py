# load packages
import pandas as pd
import numpy as np
from plotnine import *

## Load merged shipment/population data
ship_pop = pd.read_csv("../../Mid-Semester Project/SHIPMENT_merge.csv")
# ship_pop = pd.read_csv("../20_intermediate_files/SHIPMENT_merge.csv")

## Create variables for the states to be plotted and cutoff year
FL_compare = ["FL", "LA", "MS", "SC"]
FL_year = 2010

#### PRE-POST (Florida)

# Subset Florida data and group all the counties together -- summing other variables
FL = (
    ship_pop.loc[(ship_pop.BUYER_STATE == "FL"), ["Year", "MME/CAP", "Post"]]
    .groupby(["Year"])
    .sum()
    .reset_index()
)

# Convert "Post" from an integer back to a boolean value
FL["Post"] = FL.Post != 0

# Plot Florida data and save
(
    ggplot(FL, aes(x="Year", y="MME/CAP", color="Post"))
    + geom_smooth(method="lm")
    + geom_vline(aes(xintercept=FL_year))
    + theme(plot_title=element_text(text="Pre-Post (Florida)"))
).save("../20_intermediate_files/FL_Pre_Post.jpg")

#### DIFFERENCE-IN-DIFFERENCE

# Subset states in "FL_compare"
FL_data = ship_pop.loc[(ship_pop.BUYER_STATE.isin(FL_compare))].copy()

# Group each state, combining all the counties -- summing other variables
FL_data.loc[FL_data.BUYER_STATE != "FL", "BUYER_STATE"] = "Not FL"
FL_data = (
    FL_data[["BUYER_STATE", "Year", "MME/CAP", "Post"]]
    .groupby(["BUYER_STATE", "Year"])
    .sum()
    .reset_index()
)

# Convert "Post" from an integer back to a boolean value
FL_data["Post"] = data.Post != 0

# Plot data
(
    ggplot(FL_data, aes(x="Year", y="MME/CAP", color="BUYER_STATE", shape="Post"))
    + geom_smooth(method="lm")
    + geom_vline(aes(xintercept=FL_year))
    + theme(plot_title=element_text(text="Difference-in-Difference (Florida)"))
).save("../20_intermediate_files/FL_DIFinDIF.jpg")
