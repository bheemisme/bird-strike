import seaborn as sns
import matplotlib.pyplot as plt

from .source import DataSource
from .loader import DataSchema

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import pandas as pd
import numpy as np


def iqr_cleaning(data: np.ndarray | pd.Series, percentile=0):
    q1 = np.percentile(data, 25)
    q3 = np.percentile(data, 75)
    iqr = q3 - q1
    lower_bound = q1 - (percentile * iqr)
    upper_bound = q3 + (percentile * iqr)

    return data[(data >= lower_bound) & (data <= upper_bound)]


def grouped_mean(df: pd.DataFrame, group: str, value: str):
    return df.groupby(by=[group], observed=True)[value].apply(lambda x: iqr_cleaning(x).mean())


def plot_actual_strikes_per_year(ds: DataSource) -> go.Figure:
    fig = px.histogram(
        data_frame=ds.df,
        x=DataSchema.year_groups,
        y=DataSchema.wildlife_nbr_struck_actual,
        color_discrete_sequence=['#3cc389'],
        histfunc="sum",
        title="Number of Bird Strikes / year",
        category_orders={
            DataSchema.year: ds.sorted_year_groups()
        },
    )

    fig.update_layout(yaxis_title="Actual Number of bird strikes",
                      xaxis_title="Year")

    return fig


def plot_phase_damage(ds: DataSource) -> go.Figure:

    fig = px.histogram(
        data_frame=ds.df,
        x=DataSchema.when_phase_of_flight,
        color=DataSchema.effect_indicated_damage,
        y=DataSchema.wildlife_nbr_struck_actual,
        histfunc='sum',
        title="Phase of flight / Bird Strikes",
        barmode="group",
        labels={
            DataSchema.effect_indicated_damage: "Is Damaged?"
        }
    )

    fig.update_layout(
        yaxis_title="Actual Number of bird strikes",
        xaxis_title="Phase of flight",
        showlegend=True
    )

    return fig


def plot_wildlife_size_nbr_struck_actual(ds: DataSource) -> go.Figure:

    fig = px.histogram(
        data_frame=ds.df,
        x=DataSchema.wildlife_size,
        color=DataSchema.conditions_sky,
        y=DataSchema.wildlife_nbr_struck_actual,
        histfunc="sum",
        title="Wildllife Size / Conditions Sky",
        barmode="overlay"
    )

    fig.update_layout(
        yaxis_title="No. of Bird Strikes",
        xaxis_title="Wildlife Size",
        showlegend=True
    )

    return fig


def plot_damaged_pie(ds: DataSource) -> go.Figure:
    pivot = ds.df.groupby(by=[DataSchema.effect_indicated_damage]).count()[
        "Record ID"]

    labels = list(
        map(lambda x: "Caused damage" if x else "No damage", pivot.keys()))

    vals = list(pivot)

    fig = px.pie(
        data_frame=ds.df,
        names=labels,
        values=vals,
        title=f"No. of Aircrafts / Indicated Damage"
    )

    return fig


def plot_damage_any_cost(ds: DataSource) -> go.Figure:
    fig = make_subplots(rows=1, cols=3, subplot_titles=(
        "Damage To Cost",
        "Damage to Altitude",
        "Cost to Altitude"
    ))

    fig.add_trace(trace=go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.effect_indicated_damage,
            DataSchema.any_cost
        ]).count()["Record ID"].to_numpy().reshape((2, 2)),
        y=["No Damage", "Caused Damage"],
        x=['No Cost', 'Cost'],
        colorscale=px.colors.sequential.Viridis,
        showscale=False
    ), row=1, col=1)

    fig.add_trace(trace=go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.effect_indicated_damage,
            DataSchema.altitude_bin
        ], observed=True).count()["Record ID"].to_numpy().reshape((2, 2)),
        y=["No Damage", "Caused Damage"],
        x=['< 1000ft', '> 1000ft'],
        colorscale=px.colors.sequential.Viridis,
        showscale=False
    ), row=1, col=2)

    fig.add_trace(trace=go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.any_cost,
            DataSchema.altitude_bin
        ], observed=True).count()["Record ID"].to_numpy().reshape((2, 2)),
        y=["No Cost", "Cost"],
        x=['< 1000ft', '> 1000ft'],
        colorscale=px.colors.sequential.Viridis,

    ), row=1, col=3,)

    return fig


def plot_aircraft_size(ds: DataSource) -> go.Figure:

    fig = make_subplots(rows=1, cols=2, subplot_titles=(
        "Damage / Aircraft Size", "Aircraft Size / Altitude"))

    t1 = px.histogram(data_frame=ds.df,
                      x=DataSchema.effect_indicated_damage,
                      y=DataSchema.record_id,
                      color=DataSchema.is_aircraft_large,
                      histfunc="count",
                      barmode="group"
                      )

    t2 = go.Histogram(
        histfunc="avg",
        x=ds.df[DataSchema.is_aircraft_large],
        y=ds.df[DataSchema.feet_above_ground],
        showlegend=False,
    )
    fig.add_trace(trace=t1.data[0], row=1, col=1)
    fig.add_trace(trace=t1.data[1], row=1, col=1)
    fig.add_trace(trace=t2, row=1, col=2)

    fig.update_xaxes(title_text="Is Aircraft Large?", row=1, col=2)
    fig.update_xaxes(title_text="Is Damaged?", row=1, col=1)

    fig.update_yaxes(title_text="Altitude", row=1, col=2)
    fig.update_yaxes(title_text="No. of aircrafts", row=1, col=1)

    return fig


def plot_table_one(ds: DataSource) -> go.Figure:

    t1 = grouped_mean(
        ds.df,
        DataSchema.wildlife_size,
        DataSchema.feet_above_ground
    )

    table1 = go.Table(
        header=dict(values=[DataSchema.wildlife_size,
                    DataSchema.feet_above_ground]),
        cells=dict(
            values=[
                list(t1.keys()),
                list(t1)
            ]
        )
    )

    fig = go.Figure(data=[table1])

    return fig


def plot_table_two(ds: DataSource) -> go.Figure:

    t2 = grouped_mean(
        ds.df,
        DataSchema.aircraft_nbr_engines,
        DataSchema.feet_above_ground
    )

    table2 = go.Table(
        header=dict(values=[
            DataSchema.aircraft_nbr_engines,
            DataSchema.feet_above_ground
        ]),
        cells=dict(
            values=[
                list(t2.keys()),
                list(t2)
            ]
        )
    )

    fig = go.Figure(data=[table2])

    return fig
