from functools import reduce
from typing import Callable

import numpy as np
import pandas as pd
import math
Preprocessor = Callable[[pd.DataFrame], pd.DataFrame]


class DataSchema:
    record_id = 'Record ID'
    airport_name = "Airport: Name"
    
    altitude_bin = "Altitude bin"
    aircraft_make_model = "Aircraft: Make/Model"
    wildlife_nbr_struck = "Wildlife: Number struck"

    wildlife_nbr_struck_actual = "Wildlife: Number Struck Actual"
    aircraft_nbr_engines = "Aircraft: Number of engines?"
    aircraft_airline_operator = "Aircraft: Airline/Operator"
    
    flight_date = "FlightDate"
    effect_indicated_damage = "Effect: Indicated Damage"
    origin_state = "Origin State"

    when_phase_of_flight = "When: Phase of flight"
    remains_of_wildlife_collected = "Remains of wildlife collected?"
    remains_of_wildlife_sent_to_smithsonian = "Remains of wildlife sent to Smithsonian"

    wildlife_size = "Wildlife: Size"
    cost_total = "Cost: Total $"
    wildlife_species = "Wildlife: Species"
    
    conditions_sky = "Conditions: Sky"
    pilot_warned_of_birds_or_wildlife = "Pilot warned of birds or wildlife"
    feet_above_ground = "Feet above ground"

    nbr_of_people_injured = "Number of people injured"
    is_aircraft_large = "Is Aircraft Large?"

    year = "year"
    year_groups = "year-groups"
    any_cost = "Any Cost?"


def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    return df.drop_duplicates()

def iqr_cleaning(df: pd.DataFrame, attr: str, thresh = 0) -> pd.DataFrame:
    if df[attr].dtype == np.float64 or df[attr].dtype == np.float32 or df[attr].dtype == np.int64 or df[attr].dtype == np.int32:
        q1, q2, q3 = df[attr].quantile([.25,.5,.75])
        iqr = q3 - q1
        return df[(df[attr] >= q1 - thresh * iqr) & (df[attr] <= q3 + thresh * iqr)]
    raise ValueError("attr should be of float or int dtype")

def change_types(df: pd.DataFrame) -> pd.DataFrame:
    df["Aircraft: Make/Model"] = df["Aircraft: Make/Model"].astype("category")
    df["Airport: Name"] = df["Airport: Name"].astype("category")
    df["Conditions: Sky"] = df["Conditions: Sky"].astype("category")
    df["Conditions: Precipitation"] = df["Conditions: Precipitation"].astype("category")
    df["Is Aircraft Large?"] =df["Is Aircraft Large?"].map({"Yes": True, "No": False})
    df["Wildlife: Size"] = df["Wildlife: Size"].astype("category")
    df["Effect: Indicated Damage"] =df["Effect: Indicated Damage"].astype('category')
    df["Effect: Impact to flight"] = df["Effect: Impact to flight"].astype('category')
    df["Aircraft: Type"] = df["Aircraft: Type"].astype("category")
    df["Pilot warned of birds or wildlife?"] = df["Pilot warned of birds or wildlife?"].map({"Y": True, "N": False, np.nan: np.nan})
    df["Origin State"] = df["Origin State"].astype("category")
    df["Effect: Indicated Damage"] = df["Effect: Indicated Damage"].map({"Caused damage": True, "No damage": False}).astype("boolean")

    return df

def mask_column(df: pd.DataFrame) -> pd.DataFrame:
    df["Wildlife: Number struck"] = df["Wildlife: Number struck"].mask(df["Wildlife: Number Struck Actual"] > 100, "Over 100")
    df["Wildlife: Number struck"] = df["Wildlife: Number struck"].mask((df["Wildlife: Number Struck Actual"] <= 100) & ( df["Wildlife: Number Struck Actual"] >= 11), "11 to 100")
    df["Wildlife: Number struck"] = df["Wildlife: Number struck"].mask((df["Wildlife: Number Struck Actual"] >= 2) & (df["Wildlife: Number Struck Actual"] <= 10), "2 to 10")
    df["Wildlife: Number struck"] = df["Wildlife: Number struck"].mask(df["Wildlife: Number Struck Actual"] == 1, 1)
    df["Is Aircraft Large?"] = df["Is Aircraft Large?"].mask(df["Aircraft: Number of engines?"] == 1, "No")

    return df

def drop_nulls(df: pd.DataFrame) -> pd.DataFrame:
    df = df.dropna(how="all", axis=0)
    df = df.dropna(subset=["Feet above ground"], how="any", axis=0)

    df = df.dropna(subset=[
        'Aircraft: Number of engines?',
        "Effect: Impact to flight",
        "Conditions: Precipitation"
    ],axis=0, how="all")


    df[
        (df['Aircraft: Number of engines?'].isna()) &
        (df["Effect: Impact to flight"].isna()) &
        (df["Conditions: Precipitation"].isna())
    ].shape

    df = df.dropna(subset=["Aircraft: Number of engines?"], how="any", axis=0)

    df["Pilot warned of birds or wildlife?"] = df["Pilot warned of birds or wildlife?"].astype("boolean")
    df = df.drop(labels=['Effect: Impact to flight', "Conditions: Precipitation", "Remarks", "Aircraft: Type"], axis = 1)
    return df

def change_types_2(df: pd.DataFrame) -> pd.DataFrame:
    df["Altitude bin"] = df["Altitude bin"].astype("category")
    df["Is Aircraft Large?"] = df["Is Aircraft Large?"].map(
        {"No": False, True: True, False: False})
    df["Wildlife: Species"] = df["Wildlife: Species"].astype('category')
    df["Aircraft: Airline/Operator"] = df["Aircraft: Airline/Operator"].astype(
        "category")
    df["When: Phase of flight"] = df["When: Phase of flight"].astype("category")
    df["Wildlife: Number struck"] = df["Wildlife: Number struck"].map(
        {"Over 100": "Over 100", "2 to 10": "2 to 10", "11 to 100": "11 to 100", 1: "1"}).astype("category")
    df["Aircraft: Number of engines?"] = df["Aircraft: Number of engines?"].map(
        {"C": "C", 1: "1", 2: "2", 3: "3", 4: "4"}).astype("category")
    df["Remains of wildlife collected?"] = df["Remains of wildlife collected?"].astype("boolean")
    df["Remains of wildlife sent to Smithsonian"] = df["Remains of wildlife sent to Smithsonian"].astype("boolean")

    return df

def mask_column_two(df: pd.DataFrame) -> pd.DataFrame:
    from collections import Counter

    tt =  'Aircraft: Airline/Operator'
    x    = df[df["Origin State"].isna()][tt].to_list()
    x = set(x)

    for i in x:
        l = df[(~df["Origin State"].isna()) & (df[tt] == i)]["Origin State"].to_list()

    if len(l) > 0:
        df["Origin State"] = df["Origin State"].mask(
                                                        (df[tt] == i) & 
                                                        (df["Origin State"].isna()), 
                                                        Counter(l).most_common()[0][0]
                                                    )

    df = df.dropna(axis=0, subset=["Origin State"])

    return df

def add_year_groups(df: pd.DataFrame) -> pd.DataFrame:
    df[DataSchema.year]   = df[DataSchema.flight_date].dt.year

    min_year, max_year = df[DataSchema.year].min(), df[DataSchema.year].max()
    year_groups_list = list(range(min_year, max_year+2,2))
    df[DataSchema.year_groups] = pd.cut(df[DataSchema.year],year_groups_list,include_lowest=True)
    df[DataSchema.year_groups] = df[DataSchema.year_groups].map(lambda x: f'{x.left}-{x.right}')

    return df

def add_any_cost(df: pd.DataFrame) -> pd.DataFrame:
    df["Any Cost?"] = df["Cost: Total $"].map(lambda x: False if x == 0 else True)
    return df


def compose(*functions: Preprocessor) -> Preprocessor:
    return reduce(lambda f, g: lambda x: g(f(x)), functions)

def load_data(path: str) -> pd.DataFrame:
    data = pd.read_excel(
        path
    )
    data.set_index("Record ID",drop=False,inplace=True)
    preprocessor = compose(
        change_types,
        remove_duplicates,
        mask_column,
        drop_nulls,
        mask_column_two,
        change_types_2,
        add_year_groups,
        add_any_cost
    )
    return preprocessor(data)