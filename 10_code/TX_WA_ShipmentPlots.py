# load packages
import pandas as pd
import numpy as np
from plotnine import *

# load merged shipment data
ship_pop = pd.read_csv("../../Mid-Semester Project/SHIPMENT_merge_v2.csv")
# ship_pop = pd.read_csv("../20_intermediate_files/SHIPMENT_merge_v2.csv")

## Enter data parameters
# Baseline state abreviation first!
WA_compare = ["WA", "CO", "OR", "CA"]
TX_compare = ["TX", "KS", "AR", "NM"]
compares = [WA_compare, TX_compare]

# Same state order as "compares"
yr_before = [2010, 2006]
reform_year = [2011, 2007]
yr_after = [2012, 2008]

# Number of months in analysis
num_months = 24

## Create monthly dataset
# Extracting states of interest, grouping by state -- summing variables
monthly = (
    ship_pop.loc[
        (ship_pop.BUYER_STATE.isin(WA_compare + TX_compare)),
        ["BUYER_STATE", "YEAR/MONTH", "MME/CAP", "Post"],
    ].reset_index()
)

# Converting  YEAR/MONTH column to Month
monthly["Month"] = monthly["YEAR/MONTH"].apply(lambda x: int(str(x)[4:]))
monthly["Year"] = monthly["YEAR/MONTH"].apply(lambda x: int(str(x)[:4]))
monthly.drop("YEAR/MONTH", axis=1, inplace=True)

## Plotting
for i in range(len(compares)):

    # Subset the approiate states and years
    data = monthly.loc[
        (monthly.BUYER_STATE.isin(compares[i]))
        & (
            (monthly.Year >= yr_before[i])
            & (monthly.Year != reform_year[i])
            & (monthly.Year <= yr_after[i])
        )
    ].copy()

    # Chaning the names of the comparison states to a common name
    data.loc[data.BUYER_STATE != compares[i][0], "BUYER_STATE"] = f"{compares[i][0]} Control"

    # Making the 'Month' values in the 12 months leading up to the reform a countdown
    data.loc[(data.Post == False), "Month"] = (
        data.loc[(data.Post == False), "Month"] - 12
    )

    # Plot and save Pre-Post plot
    (
        ggplot(
            data.loc[
                data.BUYER_STATE == compares[i][0],
            ],
            aes(x="Month", y="MME/CAP", color="BUYER_STATE", shape="Post"),
        )
        + geom_smooth(method="lm")
        + geom_vline(aes(xintercept=0))
        + theme(
            plot_title=element_text(text=f"Pre-Post ({compares[i][0]})"),
            axis_title_x=element_text(text=f"Months from Policy Change"),
            axis_title_y=element_text(text="Morphine (mg) Per Cap."),
        )
    ).save(f"../30_results/{compares[i][0]}_Pre_Post.jpg")

    # Plot and save difference-in-difference plot
    (
        ggplot(
            data,
            aes(x="Month", y="MME/CAP", color="BUYER_STATE", shape="Post"),
        )
        + geom_smooth(method="lm")
        + geom_vline(aes(xintercept=0))
        + theme(
            plot_title=element_text(
                text=f"Difference-in-Difference ({compares[i][0]})"
            ),
            axis_title_x=element_text(text=f"Months from Policy Change"),
            axis_title_y=element_text(text="Morphine (mg) Per Cap."),
        )
    ).save(f"../30_results/{compares[i][0]}_DIFinDIF.jpg")
