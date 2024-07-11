from .source import DataSource
from .loader import DataSchema

import plotly.express as px
import plotly.graph_objects as go

from plotly.subplots import make_subplots

import pandas as pd
import numpy as np

from collections import Counter


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
        ]).count()[DataSchema.record_id].to_numpy().reshape((2, 2)),
        y=["No Damage", "Caused Damage"],
        x=['No Cost', 'Cost'],
        colorscale=px.colors.sequential.Viridis,
        showscale=False
    ), row=1, col=1)

    fig.add_trace(trace=go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.effect_indicated_damage,
            DataSchema.altitude_bin
        ], observed=True).count()[DataSchema.record_id].to_numpy().reshape((2, 2)),
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


def plot_average_strike_height(ds: DataSource) -> go.Figure:

    grouping = grouped_mean(
        ds.df,
        DataSchema.wildlife_size,
        DataSchema.feet_above_ground
    )

    table = go.Table(
        header=dict(values=[
                    DataSchema.wildlife_size,
                    DataSchema.feet_above_ground
                    ]),
        cells=dict(
            values=[
                list(grouping.keys()),
                list(grouping)
            ]
        )
    )

    fig = go.Figure(data=[table])
    fig.update_layout(title_text="Average strike height of each wildlife")
    return fig


def plot_avg_height_table(ds: DataSource) -> go.Figure:

    grouping = grouped_mean(
        ds.df,
        DataSchema.aircraft_nbr_engines,
        DataSchema.feet_above_ground
    )

    table = go.Table(
        header=dict(values=[
            DataSchema.aircraft_nbr_engines,
            DataSchema.feet_above_ground
        ]),
        cells=dict(
            values=[
                list(grouping.keys()),
                list(grouping)
            ]
        )
    )

    fig = go.Figure(data=[table])
    fig.update_layout(title_text="Average Height With respect Engines")

    return fig


def plot_top_ten_airlines(ds: DataSource) -> go.Figure:
    counts = ds.df.groupby(by=[DataSchema.aircraft_airline_operator], observed=True).count()[
        DataSchema.record_id]
    counts = counts.sort_values(ascending=False)
    counts = counts[:10]

    table = go.Table(
        header=dict(values=[
            DataSchema.aircraft_airline_operator,
            "Number of bird strikes"
        ]),
        cells=dict(
            values=[
                list(counts.keys()),
                list(counts)
            ]
        ),

    )

    fig = go.Figure(data=[table])
    fig.update_layout(title_text="Top Ten Airlines with most bird strikes")

    return fig


def plot_top_fifty_airports(ds: DataSource) -> go.Figure:
    counts = ds.df.groupby(by=[DataSchema.airport_name], observed=True).count()[
        DataSchema.record_id]
    counts = counts.sort_values(ascending=False)
    counts = counts[:50]

    table = go.Table(
        header=dict(values=[
            DataSchema.airport_name,
            "Number of bird strikes"
        ]),
        cells=dict(
            values=[
                list(counts.keys()),
                list(counts)
            ]
        ),

    )

    fig = go.Figure(data=[table])
    fig.update_layout(title_text="Top Fifty Airports")

    return fig


def plot_costs_histogram(ds: DataSource) -> go.Figure:
    costs = ds.df[(ds.df[DataSchema.effect_indicated_damage] == True) &
                  (ds.df["Any Cost?"] == True) & (ds.df[DataSchema.is_aircraft_large] == False)][DataSchema.cost_total].to_numpy()

    fig = go.Figure(
        data=[go.Histogram(x=costs, histnorm='probability', nbinsx=75)])

    fig.update_layout(title="Costs",  xaxis_title="Costs",
                      yaxis_title="probability")
    return fig


def plot_yearly_cost(ds: DataSource) -> go.Figure:
    costs = ds.df[(ds.df[DataSchema.effect_indicated_damage] == True) &
                  (ds.df["Any Cost?"] == True) & (ds.df[DataSchema.is_aircraft_large] == False)][DataSchema.cost_total].to_numpy()

    fig = px.histogram(
        data_frame=costs, x=ds.df[DataSchema.year_groups], y=ds.df[DataSchema.cost_total], histfunc="avg")

    fig.update_layout(title="Yearly Costs",
                      xaxis_title="years", yaxis_title="average cost")
    return fig


def plot_heights_histogram(ds: DataSource) -> go.Figure:
    heights = ds.df[(ds.df[DataSchema.effect_indicated_damage] == True) &
                    (ds.df["Any Cost?"] == True)][DataSchema.feet_above_ground].to_numpy()

    fig = go.Figure(data=go.Histogram(
        x=heights, histnorm="probability", nbinsx=75))

    fig.update_layout(title="Feet Above Ground",
                      xaxis_title="Feet Above Ground", yaxis_title="probability")
    return fig


def plot_pilot_warnings(ds: DataSource) -> go.Figure:
    # pilot_warns = ds.df["Pilot warned of birds or wildlife?"].to_list()
    # pilot_warns = Counter(pilot_warns)
    fig = make_subplots(rows=2, cols=2, shared_xaxes='rows', subplot_titles=("Are Pilots Warned?","Warning to Average Cost",
                                                                              "Warnig to Damage", "Warning to Cost"))

    fig1 = px.histogram(
        data_frame=ds.df, x=DataSchema.pilot_warned_of_birds_or_wildlife, histfunc='count').data[0]

    fig2 = go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.effect_indicated_damage,
            DataSchema.pilot_warned_of_birds_or_wildlife
        ], observed=True).count()[DataSchema.record_id].to_numpy().reshape((2, 2)),
        y=["No Damage", "Caused Damage"],
        x=['No Warning', 'Warned'],
        colorscale=px.colors.sequential.Viridis,
        showscale=False)
    fig3 = go.Heatmap(
        z=ds.df.groupby(by=[
            DataSchema.any_cost,
            DataSchema.pilot_warned_of_birds_or_wildlife
        ], observed=True).count()[DataSchema.record_id].to_numpy().reshape((2, 2)),
        y=["No Cost", "Occurred Cost"],
        x=['No Warning', 'Warned'],
        colorscale=px.colors.sequential.Viridis,
        showscale=True
    )

    fig4 = px.histogram(data_frame=ds.df,
                        x=DataSchema.pilot_warned_of_birds_or_wildlife,
                        y=DataSchema.cost_total, histfunc='avg').data[0]

    fig.add_trace(trace=fig1, row=1, col=1)
    fig.add_trace(trace=fig4, row=1, col=2)

    fig.add_trace(trace=fig2, row=2, col=1)
    fig.add_trace(trace=fig3, row=2, col=2)

    fig.update_layout(title="Pilot warnings and Impact", height=800)
    return fig


def plot_engines_pie(ds: DataSource) -> go.Figure:
    k = ds.df[(ds.df[DataSchema.effect_indicated_damage]) & (
        ds.df["Any Cost?"] == True)][DataSchema.aircraft_nbr_engines]
    k = Counter(k)

    fig = go.Figure(data=go.Pie(values=tuple(k.values()),
                                labels=tuple(k.keys())))

    fig.update_layout(
        title="Number of engines",

    )
    return fig


def plot_heights(ds: DataSource) -> go.Figure:

    pivot = ds.df[(ds.df[DataSchema.effect_indicated_damage])
                  & (ds.df["Any Cost?"] == True)]

    fig = make_subplots(rows=1, cols=2, subplot_titles=(
        "Height to Strikes",
        "Height to Cost"
    ))

    trace_one = px.scatter(pivot, y=DataSchema.wildlife_nbr_struck_actual,
                           x=DataSchema.feet_above_ground).data[0]
    trace_two = px.scatter(pivot, y=DataSchema.cost_total,
                           x=DataSchema.feet_above_ground,
                           color_discrete_sequence=["green"],
                           ).data[0]

    fig.add_trace(trace=trace_one, row=1, col=1)
    fig.add_trace(trace=trace_two, row=1, col=2)
    fig.update_xaxes(row=1, col=1, title_text="Feet Above Ground")
    fig.update_xaxes(row=1, col=2, title_text="Feet Above Ground")
    fig.update_yaxes(row=1, col=1, title_text="No. of Strikes")
    fig.update_yaxes(row=1, col=2, title_text="Total Cost")

    return fig


def plot_phase_height(ds: DataSource) -> go.Figure:
    pivot = ds.df[(ds.df[DataSchema.effect_indicated_damage])
                  & (ds.df["Any Cost?"] == True)]

    fig = px.histogram(data_frame=pivot, x=DataSchema.when_phase_of_flight,
                       y=DataSchema.feet_above_ground, histfunc="avg")

    fig.update_layout(yaxis_title="Average Height")
    return fig


def plot_effect_impact(ds: DataSource) -> go.Figure:
    pivot = ds.df[(ds.df[DataSchema.effect_indicated_damage])
                  & (ds.df["Any Cost?"] == True)]

    fig = px.histogram(data_frame=pivot,
                       x=DataSchema.aircraft_make_model,
                       y=DataSchema.cost_total,
                       histfunc="avg"
                       )
    fig.update_layout(yaxis_title="average cost",
                      xaxis_title="aircraft",
                      title_text="Average Cost per Aircraft")

    return fig


def plot_aircraft_altitude(ds: DataSource) -> go.Figure:
    pivot = ds.df[(ds.df[DataSchema.effect_indicated_damage])
                  & (ds.df["Any Cost?"] == True)]

    fig = px.histogram(data_frame=pivot,
                       x=DataSchema.aircraft_make_model,
                       y=DataSchema.feet_above_ground,
                       histfunc="avg"
                       )

    fig.update_layout(yaxis_title="average height",
                      title_text="Altitude At the time of strike", xaxis_title="aircraft")

    return fig


def plot_strike_altitude(ds: DataSource) -> go.Figure:
    pivot = ds.df[(ds.df[DataSchema.effect_indicated_damage])
                  & (ds.df["Any Cost?"] == True)]

    fig = make_subplots(rows=2, cols=2, subplot_titles=(
        "Average Cost as per altitude",
        "No. of aircrafts incurred cost",
        "Damage as per aircraft",

    ), specs=[[{}, {}], [{"colspan": 2}, None]],
        shared_xaxes='rows',  # type: ignore
        vertical_spacing=0.4)
    # print(pivot["altitude_groups"])
    fig1 = px.histogram(data_frame=pivot,
                        x=DataSchema.altitude_groups,
                        y=DataSchema.effect_indicated_damage,
                        histfunc='count').data[0]

    fig2 = px.histogram(data_frame=pivot,
                        x=DataSchema.altitude_groups,
                        y=DataSchema.cost_total,
                        histfunc='avg').data[0]

    fig3 = px.histogram(data_frame=pivot,
                        x=DataSchema.altitude_groups,
                        y=DataSchema.any_cost,
                        histfunc='count').data[0]

    fig.add_trace(trace=fig3, row=1, col=1, )
    fig.update_xaxes(row=1, col=1, title="Altitude", showticklabels=True)
    fig.add_trace(trace=fig1, row=1, col=2)
    fig.update_xaxes(row=1, col=2, title="Altitude", showticklabels=True)
    fig.add_trace(trace=fig2, row=2, col=1)
    fig.update_xaxes(row=2, col=1, title="Altitude", showticklabels=True)
    fig.update_layout(
        title_text="Impact of Strike as per Altitude", height=700)

    return fig
