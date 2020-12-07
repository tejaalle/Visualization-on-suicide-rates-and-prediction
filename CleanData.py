# Author: name (banner no) <@dal.ca>
# File: This will return all the visualization in tab for Continents.

# imports
import pandas as pd
import plotly.graph_objects as go
import seaborn as sns

from ByContinent import Sucides_by_Continet

sns.set()
import matplotlib.pyplot as plt
import plotly.express as px
import pycountry_convert as pc

# df = pd.read_csv("master.csv")

class Country_year_gender:

    # To return unique contries.
    def countries(self, df):
        return df["country"].unique()

    # To return unique years
    def years(self, df):
        return df["year"].unique()

    # To return unique gender
    def gender(self, df):
        return df["sex"].unique()

    # To return unique age
    def age(self, df):
        return df["age"].unique()

    # To return Visualization in bar chart for the all the counties
    def allcountries(self, df):
        allcountries = df.groupby("country")["suicides_no"].sum()
        trace = go.Bar(x=allcountries.index, y=allcountries)
        layout = go.Layout(title="Total sucide count between 1985-2016", xaxis=dict(tickangle=45),
                           uniformtext=dict(minsize=10))
        fig = go.Figure(data=trace, layout=layout)
        return fig

    # To return Visualization in (**AS ABOVE**)
    def country_gender(self,df, country):
        x = ["male", "female"]
        onlycountry = df.loc[df["country"] == country]
        year_group = onlycountry.groupby("year")["suicides_no"].sum()
        plot_x = year_group.index
        plot_y = year_group
        age_group= onlycountry.groupby("age")["suicides_no"].sum()
        pie_lables = age_group.index
        pie_values = age_group
        y = []
        for i in x:
            gender = onlycountry.loc[onlycountry["sex"] == i]
            y.append(gender["suicides_no"].sum())
        trace = [go.Scatter(x=plot_x, y=plot_y, mode='lines', visible=True), go.Bar(x=x, y=y, visible=False),go.Pie(labels=pie_lables,values=pie_values,visible=False)]
        layout = go.Layout(title="Detail sucide count of " + country)
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(
            updatemenus=[
                dict(type="buttons",
                     direction="left",
                     buttons=[
                         dict(
                             label="All Years",
                             method="update",
                             args=[{"type": ["scatter", "bar","pie"], "mode": ["lines", "", ""],
                                    "visible": [True, False,False]}],
                         ), dict(
                             label="Gender",
                             method="update",
                             args=[{"type": ["scatter", "bar","pie"], "mode": ["lines", "", ""],
                                    "visible": [False, True,False]}],
                         ),
                         dict(
                             label="Age",
                             method="update",
                             args=[{"type": ["scatter", "bar","pie"], "mode": ["lines", "", ""],
                                    "visible": [False, False, True]}],
                         )
                     ],
                     pad={"r": 10, "t": 0}, showactive=True, x=0.11, xanchor="left", y=1.1, yanchor="top"
                     ),
            ]
        )
        return fig

    # To return Visualization in heat co-relation
    def heat_coorelation(self, df):
        corr = df.corr()
        fig = px.imshow(corr, color_continuous_scale=px.colors.diverging.Tealrose, title="Heatmap Correlation")
        return fig

    # To return Visualization in bar chart for the generation by suicides_no
    def GenerationSuicide(self, df):
        generation = df.groupby(["generation", "sex"])["suicides_no"].sum()

        newDict = {"generation": [],
                   "sex": [],
                   "suicides_no": []
                   }
        for name, group in df.groupby(['generation', 'sex']):
            newDict["generation"].append(name[0])
            newDict["sex"].append(name[1])
            newDict["suicides_no"].append(generation[name[0], name[1]])

        fig_df = pd.DataFrame.from_dict(newDict)
        trace = [go.Bar(name="female", x=fig_df["generation"].iloc[::2], y=fig_df["suicides_no"].iloc[::2],
                        marker=dict(color='#FFAE49')),
                 go.Bar(name="male", x=fig_df["generation"].iloc[1::2], y=fig_df["suicides_no"].iloc[1::2],
                        marker=dict(color='#44A5C2'))]
        layout = go.Layout(title="Suicides number by generation and sex", font=dict(size=13),
                           xaxis=dict(title="generation"), yaxis=dict(title="suicides_no"),
                           legend=dict(title="Legends"), plot_bgcolor="ghostwhite")
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(barmode='group')
        return fig

        # ---- OLD CODE - BEFORE Professor's Remarks ---- #
        # fig = px.bar(df, x='generation', y='suicides_no', color='sex', barmode='group', title='Suicides number by '
        #                                                                                       'generation and sex')
        # return fig

    # To return Visualization in bar chart for the age by suicides_no
    def suicide_age(self, df):
        continents = df.groupby(["age", "sex"])["suicides_no"].sum()

        newDict = {"age": [],
                   "sex": [],
                   "suicides_no": []
                   }
        for name, group in df.groupby(['age', 'sex']):
            newDict["age"].append(name[0])
            newDict["sex"].append(name[1])
            newDict["suicides_no"].append(continents[name[0], name[1]])

        fig_df = pd.DataFrame.from_dict(newDict)
        trace = [go.Bar(name="female", x=fig_df["age"].iloc[::2], y=fig_df["suicides_no"].iloc[::2],
                        marker=dict(color='#FFAE49')),
                 go.Bar(name="male", x=fig_df["age"].iloc[1::2], y=fig_df["suicides_no"].iloc[1::2],
                        marker=dict(color='#44A5C2'))]
        layout = go.Layout(title="Suicides number by age and sex", font=dict(size=13),
                           xaxis=dict(title="age"), yaxis=dict(title="suicides_no"),
                           legend=dict(title="Legends"), plot_bgcolor="ghostwhite")
        fig = go.Figure(data=trace, layout=layout)
        fig.update_layout(barmode='group')
        return fig

        # ---- OLD CODE - BEFORE Professor's Remarks ---- #

        # fig = px.bar(df, x='age', y='suicides_no', color='sex', title='Suicides number by '
        #                                                               'Age and sex', height=400)
        # return fig

    # To return Visualization in bar chart for the year by suicides_no
    def suicide_by_year(self, df):
        df_time = df.groupby(["year"]).suicides_no.sum()
        trace = go.Bar(x=df_time.index, y=df_time)
        layout = go.Layout(title="Total suicide count between 1985-2016")
        fig = go.Figure(data=trace, layout=layout)
        return fig

    # To return Visualization in scatter plot for the GDP by year
    def gdp_year(self, df):
        fig = px.scatter(df, x=' gdp_for_year ($) ', y='suicides_no', color='year', title='Checking the relationship '
                                                                                          'between gdp for year and '
                                                                                          'number of suicides')
        return fig

    # To return Visualization in density contour for the GDP by suicides_no
    def gdp_suicide_contour(self, df):
        df = df.sort_values(by=['year'])
        fig = px.density_contour(df, x=' gdp_for_year ($) ', y='suicides_no', color='year', marginal_y="histogram"
                                 , animation_frame='year',
                                 animation_group='country')
        return fig

    # Cleaning the data for the Visualization by Country
    def byCountry_data_cleaning(self, df):

        # test = (df['year'] == 1987) & (df['country'] == 'Albania')
        # print(df[test].filter(items=['country',
        #                                  'year',
        #                                  'suicides_no',
        #                                  'suicides/100k pop',
        #                                  'population']))

        countries = df.groupby(["country", "year"])["suicides_no"].sum()
        population = df.groupby(["country", "year"])["population"].sum()

        newDict = {"country": [],
                   "year": [],
                   "Suicide Number": [],
                   "Suicide per 100k": [],
                   "GDP per Capita": []
                   }
        for name, group in df.groupby(['country', 'year']):
            newDict["country"].append(name[0])
            newDict["year"].append(name[1])
            newDict["Suicide Number"].append(countries[name[0], name[1]])
            newDict["Suicide per 100k"].append((countries[name[0], name[1]] * 1000000) / population[name[0], name[1]])
            newDict["GDP per Capita"].append(group['gdp_per_capita ($)'].iloc[0])

        new_df = pd.DataFrame.from_dict(newDict)
        sucides_by_continet = Sucides_by_Continet()
        updated_df = sucides_by_continet.updateData(new_df)
        updated_df['iso_alpha'] = updated_df.apply(lambda row: pc.country_name_to_country_alpha3(row.country, cn_name_format="default"), axis=1)
        print('---------------------')
        print(updated_df)
        print('---------------------')
        return updated_df.sort_values(by=['year'])

    def byCategory_data_cleaning(self, df):
        df = df.replace(to_replace="5-14 years", value="05-14 years")
        countries = df.groupby(["country", "age", "year"])["suicides_no"].sum()

        newDict = {"country": [],
                   "age": [],
                   "year": [],
                   "suicides_no": [],
                   "gdp_per_capita ($)": []
                   }
        for name, group in df.groupby(['country', 'age', 'year']):
            newDict["country"].append(name[0])
            newDict["age"].append(name[1])
            newDict["year"].append(name[2])
            newDict["suicides_no"].append(countries[name[0], name[1], name[2]])
            newDict["gdp_per_capita ($)"].append(group['gdp_per_capita ($)'].iloc[0])

        fig_df = pd.DataFrame.from_dict(newDict)
        return fig_df.sort_values(by=['year', 'age'])

