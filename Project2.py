import pandas as pd
from dash import Dash, dcc, html, Input, Output
import plotly.express as px

DATA_FILE = "dealt-with-anxiety-depression-religious-spiritual.csv"
VALUE_COL = "Engaged in religious/spiritual activities"

def load_data():
    df = pd.read_csv(DATA_FILE)
    df = df.rename(columns={VALUE_COL: "value"})
    df["type"] = df["Code"].apply(lambda x: "Aggregate/Region" if pd.isna(x) else "Country")
    return df

df = load_data()
country_df = df[df["type"] == "Country"].copy()

app = Dash(__name__)

app.layout = html.Div(
    style={
        "fontFamily": "Arial, sans-serif",
        "maxWidth": "1200px",
        "margin": "0 auto",
        "padding": "20px"
    },
    children=[
        html.H1("Religious/Spiritual Coping Activities Dashboard"),

        html.P(
            "This dashboard shows the percentage of respondents in 2020 who reported "
            "using religious or spiritual activities to feel better after experiencing "
            "anxiety or depression severe enough to disrupt regular daily activities "
            "for two weeks or longer."
        ),

        html.P(
            "Instructions: choose whether to include aggregate regions, select top or bottom "
            "entities, adjust how many entities to display, and optionally search for an entity."
        ),

        html.Div(
            style={
                "display": "grid",
                "gridTemplateColumns": "1fr 1fr",
                "gap": "16px",
                "marginBottom": "24px"
            },
            children=[
                html.Div([
                    html.Label("Include aggregate regions"),
                    dcc.Checklist(
                        id="include-aggregates",
                        options=[{"label": " Show aggregate regions/continents", "value": "yes"}],
                        value=[]
                    )
                ]),

                html.Div([
                    html.Label("Comparison mode"),
                    dcc.RadioItems(
                        id="rank-mode",
                        options=[
                            {"label": " Top values", "value": "top"},
                            {"label": " Bottom values", "value": "bottom"}
                        ],
                        value="top",
                        inline=True
                    )
                ]),

                html.Div([
                    html.Label("Number of entities to display"),
                    dcc.Slider(
                        id="count-slider",
                        min=5,
                        max=25,
                        step=1,
                        value=10,
                        marks={5: "5", 10: "10", 15: "15", 20: "20", 25: "25"}
                    )
                ]),

                html.Div([
                    html.Label("Search entity name"),
                    dcc.Input(
                        id="search-input",
                        type="text",
                        placeholder="Type a country or region name",
                        value="",
                        style={"width": "100%"}
                    )
                ])
            ]
        ),

        html.Div(id="summary-text", style={"marginBottom": "20px", "fontWeight": "bold"}),

        dcc.Graph(id="bar-chart"),
        dcc.Graph(id="histogram-chart"),
        dcc.Graph(id="map-chart")
    ]
)

@app.callback(
    Output("summary-text", "children"),
    Output("bar-chart", "figure"),
    Output("histogram-chart", "figure"),
    Output("map-chart", "figure"),
    Input("include-aggregates", "value"),
    Input("rank-mode", "value"),
    Input("count-slider", "value"),
    Input("search-input", "value")
)
def update_dashboard(include_aggregates, rank_mode, count_value, search_value):
    filtered = df.copy() if "yes" in include_aggregates else country_df.copy()

    if search_value:
        filtered = filtered[filtered["Entity"].str.contains(search_value, case=False, na=False)]

    if filtered.empty:
        empty_fig = px.scatter(title="No data available for the current filters.")
        empty_fig.update_xaxes(visible=False)
        empty_fig.update_yaxes(visible=False)
        return "No entities match the current filters.", empty_fig, empty_fig, empty_fig

    ranked = filtered.sort_values("value", ascending=(rank_mode == "bottom")).head(count_value)
    ranked = ranked.sort_values("value", ascending=True)

    summary = (
        f"Showing {len(filtered)} entities. Average percentage: {filtered['value'].mean():.2f}. "
        f"Highest percentage: {filtered.loc[filtered['value'].idxmax(), 'Entity']} "
        f"({filtered['value'].max():.2f})."
    )

    bar_fig = px.bar(
        ranked,
        x="value",
        y="Entity",
        orientation="h",
        title=f"{'Top' if rank_mode == 'top' else 'Bottom'} {count_value} entities",
        labels={"value": "Used religious/spiritual activities to cope with anxiety/depression", "Entity": "Entity"}
    )
    bar_fig.update_layout(yaxis={"categoryorder": "total ascending"})

    hist_fig = px.histogram(
        filtered,
        x="value",
        nbins=15,
        title="Distribution of engagement values",
        labels={"value": "Used religious/spiritual activities to cope with anxiety/depression"}
    )

    map_data = filtered[filtered["Code"].notna()].copy()
    if map_data.empty:
        map_fig = px.scatter(title="Map unavailable for the current filters.")
        map_fig.update_xaxes(visible=False)
        map_fig.update_yaxes(visible=False)
    else:
        map_fig = px.choropleth(
            map_data,
            locations="Code",
            color="value",
            hover_name="Entity",
            title="World map of engagement values",
            labels={"value": "Used religious/spiritual activities to cope with anxiety/depression"}
        )

    return summary, bar_fig, hist_fig, map_fig