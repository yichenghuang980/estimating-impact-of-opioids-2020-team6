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

# Subset states in "FL_compare"
FL_data = ship_pop.loc[(ship_pop.BUYER_STATE.isin(FL_compare))].copy()

# Group each state, combining all the counties -- summing other variables
FL_data.loc[FL_data.BUYER_STATE != "FL", "BUYER_STATE"] = "Not FL"
FL_data = (
    FL_data[["BUYER_STATE", "Year", "MME/CAP", "Post"]]
    .groupby(["BUYER_STATE", "Year"])
    .mean()
    .reset_index()
)

# Check for equal amount of data for FL and comparison states
assert len(FL_data[FL_data.BUYER_STATE == "FL"]) == len(
    FL_data[FL_data.BUYER_STATE != "FL"]
)

# Convert "Post" from an integer back to a boolean value
FL_data["Post"] = FL_data.Post != 0
FL_data["Year"] = FL_data["Year"].apply(lambda x: int(x))
FL_data.loc[:, "Year"] = FL_data.loc[:, "Year"] - FL_year

### Plot data
# Pre-Post
(
    ggplot(
        FL_data.loc[
            FL_data.BUYER_STATE == "FL",
        ],
        aes(x="Year", y="MME/CAP", color="Post"),
    )
    + geom_smooth(method="lm")
    + geom_vline(aes(xintercept=0))
    + theme(
        plot_title=element_text(text="Pre-Post (Florida)"),
        axis_title_x=element_text(text="Years from Policy Change"),
        axis_title_y=element_text(text="Morphine (mg) Per Cap."),
    )
).save("../30_results/FL_Pre_Post.jpg")

# Differnece-in-Difference
(
    ggplot(FL_data, aes(x="Year", y="MME/CAP", color="BUYER_STATE", shape="Post"))
    + geom_smooth(method="lm")
    + geom_vline(aes(xintercept=0))
    + theme(
        plot_title=element_text(text="Difference-in-Difference (Florida)"),
        axis_title_x=element_text(text="Years from Policy Change"),
        axis_title_y=element_text(text="Morphine (mg) Per Cap."),
    )
).save("../30_results/FL_DIFinDIF.jpg")
