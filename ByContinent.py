# Author: Krutin Trivedi (kr650539) <krutin@dal.ca>
# File: This will return all the visualization in tab for Continents.

# imports
import pandas as pd
import pycountry_convert as pc
import plotly.graph_objects as go
import plotly.express as px

from dash.dependencies import Output, Input, State
from matplotlib.widgets import Button, Slider
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash


class Sucides_by_Continet:

    # To update the city names to get the proper Continent name
    def updateData(self, df):
        return df.replace(["Cabo Verde", "Republic of Korea", "Russian Federation", "Serbia", "United States", "Saint Vincent and Grenadines"],
                          ["Cape Verde", "South Korea", "Russia", "Republic of Serbia", "United States of America", "Saint Vincent and the Grenadines"])

    # To return unique contries
    def country(self, df):
        return df["country"].unique()

    # To return unique gender
    def gender(self, df):
        return df["sex"].unique()

    # To return unique age(age-group)
    def age(self, df):
        return df["age"].unique()

    # To Add another Column of Continents.
    def addContinent(self, df):
        df['Continent'] = df.apply(lambda row: pc.convert_continent_code_to_continent_name(pc.country_alpha2_to_continent_code(pc.country_name_to_country_alpha2(row.country, cn_name_format="default"))), axis=1)

    # To return unique Continents
    def continent(self, df):
        return df['Continent'].unique()

    # To return Visualization of bar chart for the continent by suicides_no
    def continent_by_suicides_no(self, df):
        continents = df.groupby(["Continent", "sex"])["suicides_no"].sum()

        newDict = {"Continent": [],
                   "sex": [],
                   "suicides_no": []
                   }
        for name, group in df.groupby(['Continent', 'sex']):
            newDict["Continent"].append(name[0])
            newDict["sex"].append(name[1])
            newDict["suicides_no"].append(continents[name[0], name[1]])

        fig_df = pd.DataFrame.from_dict(newDict)
        trace = [go.Bar(name="female", x=fig_df["Continent"].iloc[::2], y=fig_df["suicides_no"].iloc[::2],
                        marker=dict(color='#FFAE49')),
                 go.Bar(name="male", x=fig_df["Continent"].iloc[1::2], y=fig_df["suicides_no"].iloc[1::2],
                        marker=dict(color='#44A5C2'))]
        layout = go.Layout(title="Suicides by continent for sex between 1985-2016", font=dict(size=13),
                           xaxis=dict(title="Continent"), yaxis=dict(title="suicides number"),
                           legend=dict(title="Legends"), plot_bgcolor="ghostwhite")
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(barmode='group')
        return fig

    # To return Visualization of bar chart for the continent by suicides per 100k
    def continent_by_suicides_per_100k(self, df):
        continents = df.groupby(["Continent", "sex"])["suicides/100k pop"].sum()

        newDict = {"Continent": [],
                   "sex": [],
                   "suicides/100k pop": []
                   }
        for name, group in df.groupby(['Continent', 'sex']):
            newDict["Continent"].append(name[0])
            newDict["sex"].append(name[1])
            newDict["suicides/100k pop"].append(continents[name[0], name[1]])

        fig_df = pd.DataFrame.from_dict(newDict)
        trace = [go.Bar(name="female", x=fig_df["Continent"].iloc[::2], y=fig_df["suicides/100k pop"].iloc[::2],
                        marker=dict(color='#FFAE49')),
                 go.Bar(name="male", x=fig_df["Continent"].iloc[1::2], y=fig_df["suicides/100k pop"].iloc[1::2],
                        marker=dict(color='#44A5C2'))]
        layout = go.Layout(title="Suicides per 100k people by continent for sex between 1985-2016", font=dict(size=13),
                           xaxis=dict(title="Continent"), yaxis=dict(title="suicides per 100k population"),
                           legend=dict(title="Legends"), plot_bgcolor="ghostwhite")
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(barmode='group')
        return fig

    # To return Visualization of bar chart for the continent by age
    def continent_by_age(self, df):
        df = df.replace(to_replace="5-14 years", value="05-14 years")
        continents = df.groupby(["Continent", "age"])["suicides/100k pop"].sum()

        newDict = {"Continent": [],
                   "age": [],
                   "suicides/100k pop": []
                   }
        for name, group in df.groupby(['Continent', 'age']):
            newDict["Continent"].append(name[0])
            newDict["age"].append(name[1])
            newDict["suicides/100k pop"].append(continents[name[0], name[1]])

        fig_df = pd.DataFrame.from_dict(newDict)
        trace = [go.Bar(name="05-14 years", x=fig_df["Continent"].iloc[::6], y=fig_df["suicides/100k pop"].iloc[::6],
                        marker=dict(color='#003f5c')),
                 go.Bar(name="15-24 years", x=fig_df["Continent"].iloc[1::6], y=fig_df["suicides/100k pop"].iloc[1::6],
                        marker=dict(color='#444e86')),
                 go.Bar(name="25-34 years", x=fig_df["Continent"].iloc[2::6], y=fig_df["suicides/100k pop"].iloc[2::6],
                        marker=dict(color='#955196')),
                 go.Bar(name="35-54 years", x=fig_df["Continent"].iloc[3::6], y=fig_df["suicides/100k pop"].iloc[3::6],
                        marker=dict(color='#dd5182')),
                 go.Bar(name="55-74 years", x=fig_df["Continent"].iloc[4::6], y=fig_df["suicides/100k pop"].iloc[4::6],
                        marker=dict(color='#ff6e54')),
                 go.Bar(name="75+ years", x=fig_df["Continent"].iloc[5::6], y=fig_df["suicides/100k pop"].iloc[5::6],
                        marker=dict(color='#ffa600'))]
        layout = go.Layout(title="Suicides per 100k people by continent for age between 1985-2016", font=dict(size=13),
                           xaxis=dict(title="Continent"), yaxis=dict(title="suicides per 100k population"),
                           legend=dict(title="Legends"), plot_bgcolor="ghostwhite")
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(barmode='group')
        return fig

    # Scatter geo plot for Continents.
    def suicidesbygeo(self, df):
        df['iso_alpha'] = df.apply(lambda row: pc.country_name_to_country_alpha3(row.country, cn_name_format="default"), axis=1)
        df = df.sort_values(by=['year'])
        fig = px.scatter_geo(df, locations="iso_alpha", color="Continent",
                             hover_name="country", size="suicides_no",
                             animation_frame="year", title="Continent wide suicides with each year")
        fig.update_layout(width=1080, height=600)
        return fig

    # Sunburst graph for Continents.
    def sunburstgraph(self, df):
        fig = px.sunburst(df, path=['Continent', 'sex', 'age'], values='suicides_no', title="Suicides with respect to Continent, Sex and Age")
        return fig

    # Pie chart for Continents.
    def piechart(self, df):
        continents = df.groupby("Continent")["suicides_no"].sum()
        newDict = {"Continent": [],
                   "suicides_no": [],
                   }
        for name in df['Continent'].unique():
            newDict["Continent"].append(name)
            newDict["suicides_no"].append(continents[name])

        fig_df = pd.DataFrame.from_dict(newDict)
        fig = go.Figure(data=[go.Pie(labels=fig_df["Continent"], values=fig_df['suicides_no'])],
                        layout=go.Layout(title="Suicides by continent between 1985-2016", legend=dict(title="Legends")))
        return fig

# This will return A tab for the Continents Graph.
def tabContinent():
    df = pd.read_csv("master.csv")
    # test = (df['year'] == 1985) & (df['country'] == 'Mauritius')
    # print(df[test].sort_values(by=['suicides_no']).filter(items=['country',
    #                                                              'year',
    #                                                              'suicides_no',
    #                                                              'suicides/100k pop',
    #                                                              'gdp_per_capita ($)']))

    sucides_by_continet = Sucides_by_Continet()
    df = sucides_by_continet.updateData(df)
    sucides_by_continet.addContinent(df)
    tab5 = dbc.FormGroup([
            dbc.Row([
                dbc.Col(dcc.Graph(id='continent_by_suicides_no', figure=sucides_by_continet.continent_by_suicides_no(df))),
            ]), dbc.Row([
                dbc.Col(dcc.Graph(id='continent_by_suicides_per_100k', figure=sucides_by_continet.continent_by_suicides_per_100k(df))),
            ]), dbc.Row([
                dbc.Col(dcc.Graph(id='continent_by_age', figure=sucides_by_continet.continent_by_age(df)))
            ]), dbc.Row([
                dbc.Col(dcc.Graph(id='suicidesbygeo', figure=sucides_by_continet.suicidesbygeo(df)))
            ]),  dbc.Row([
                dbc.Col(dcc.Graph(id='sunburstgraph', figure=sucides_by_continet.sunburstgraph(df)))
            ]),  dbc.Row([
                dbc.Col(dcc.Graph(id='piechart', figure=sucides_by_continet.piechart(df)))
            ])
        ])
    return tab5



