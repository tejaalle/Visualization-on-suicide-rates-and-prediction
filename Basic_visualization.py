# Author: name (banner no) <@dal.ca>
# File: This will return all the visualization in tab for Continents.

# imports
from dash.dependencies import Output, Input, State
from matplotlib.widgets import Button, Slider
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash
import plotly.express as px
from CleanData import *
from ML1 import *
from ByContinent import *

# Main Visualization page for entire application.
def visulaize():

    # Read the main CSV
    df = pd.read_csv("master.csv")

    # Get all unique Values for the prediction.
    country_y_g = Country_year_gender()
    countries = country_y_g.countries(df)
    years = country_y_g.years(df)
    genders = country_y_g.gender(df)
    ages = country_y_g.age(df)

    cleaned_df_for_tab2 = country_y_g.byCountry_data_cleaning(df)
    cleaned_df_for_tab3 = country_y_g.byCategory_data_cleaning(df)

    # Creating main Dash App
    app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

    # First Tab: Overview & Prediction
    tab1_content = dbc.Card([
        # Displaying the all countries bar chart
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph1', figure=country_y_g.allcountries(df))),
            ]), dbc.Row([
                dbc.Col(dcc.Graph(id='graph2'), style={'display': 'none'}, id="detail_col")
            ])
        ]),
        # For Prediction.
        dbc.FormGroup([
            dbc.Label("Try predicting for future years"),
            dbc.Row([
                dbc.Col(dcc.Dropdown(id="country_dropdown1",
                                     options=[{"label": j, "value": i} for i, j in enumerate(countries)])),
                dbc.Col(
                    dcc.Dropdown(id="age_dropdown1", options=[{"label": j, "value": i} for i, j in enumerate(ages)])),
                dbc.Col(dcc.Dropdown(id="sex_dropdown1",
                                     options=[{"label": j, "value": i} for i, j in enumerate(genders)])),
                dbc.Col(dcc.Input(id='year', value="2020", type='text'))
            ])

        ]),
        dbc.Button('predict', id='button', color='primary', style={'margin-bottom': '1em'}, block=True),
        dbc.FormGroup([
            dbc.Alert(id="predicted_output", color="success"),
            dbc.Alert(id="predicted_model", color="success"),
        ]),
    ], body=True)

    @app.callback(
        [Output('predicted_output', 'children'), Output('predicted_model', 'children')],
        Input('button', 'n_clicks'),
        [State('country_dropdown1', 'value'), State('age_dropdown1', 'value'),
         State('sex_dropdown1', 'value'), State('year', 'value')])
    def prediction(n_clicks, country, age, sex, year):
        if country is None:
            return ["For Predictions, please select the values",
                    "For Predictions, please select the values"]
        else:
            predicted_value, score = suciderate_prediction(df, countries[country], ages[age], genders[sex], int(year))
            return ["The predicted suicide count in the year " + year + " is " + str(predicted_value),
                    "The model predicted "
                    "with efficiency "
                    "" + str(score)]

    @app.callback(
        [Output('graph2', 'figure'), Output('detail_col', 'style')],
        Input('graph1', 'clickData'))
    def display_graph2_data(data):
        if data is not None:
            innervalue = data['points'][0]
            if "value" in innervalue:
                return country_y_g.country_gender(df, innervalue["label"]), {"display": "block"}
            else:
                return [go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 2, 3])]), {"display": "None"}]
        else:
            return [go.Figure(data=[go.Bar(x=[1, 2, 3], y=[1, 2, 3])]), {"display": "None"}]
    # First Tab END

    # Second Tab: Visualization by countries
    country_wide_options = ["Suicide Number", "Suicide per 100k", "GDP per Capita"]

    countrywide_parameter_selection_card = dbc.Card([
        dbc.FormGroup([
            dbc.Label("Choose Value To Represent"),
            dcc.Dropdown(id="cw_dropdown", value=country_wide_options[0],
                         options=[{"label": label, "value": label} for label in country_wide_options]),
        ]),
    ], body=True)

    tab2_content = dbc.Card([
        html.H3(children='Visualizations through the years based on Country'),
        dbc.Card([
            dbc.Row([
                dbc.Col(countrywide_parameter_selection_card, md=12),
                dbc.Col(dcc.Graph(id='cw_graph'), md=12)
            ])
        ], body=True),
    ], body=True)

    @app.callback(
        Output('cw_graph', 'figure'),
        Input('cw_dropdown', 'value')
    )
    # This will return the figure based on the User input
    def country_wide_prediction(map_val):
        fig = px.choropleth(cleaned_df_for_tab2, locations='iso_alpha',
                            color=map_val,
                            color_continuous_scale=px.colors.sequential.Plasma, hover_name="country",
                            animation_frame="year")
        # ---- OLD CODE - BEFORE Professor's Remarks ---- #

        # if map_val == country_wide_options[0]:
        #     fig = px.choropleth(df, locations='iso_alpha',
        #                         color='suicides_no',
        #                         color_continuous_scale=px.colors.sequential.Plasma, hover_name="country",
        #                         animation_frame="year")
        # elif map_val == country_wide_options[1]:
        #     fig = px.choropleth(df, locations='iso_alpha', locationmode='country names',
        #                         color='suicides/100k pop',
        #                         color_continuous_scale=px.colors.sequential.Plasma, hover_name="country",
        #                         animation_frame="year")
        # elif map_val == country_wide_options[2]:
        #     fig = px.choropleth(df, locations='iso_alpha', locationmode='country names',
        #                         color='gdp_per_capita ($)',
        #                         color_continuous_scale=px.colors.sequential.Plasma, hover_name="country",
        #                         animation_frame="year")
        # else:
        #     fig = px.choropleth(cleaned_df, locations='country', locationmode='country names',
        #                         color='suicides_no',
        #                         color_continuous_scale=px.colors.sequential.Plasma, hover_name="country",
        #                         animation_frame="year")

        return fig

    # Second Tab END

    # Third Tab:
    categorical_options = ["age", "generation", "sex"]

    categorical_bar_parameter_selection_card = dbc.Card([
        # Chart Selection
        dbc.FormGroup([
            dbc.Label("Choose Type of Chart"),
            dcc.Dropdown(id="cat_type_dropdown", value="grouped",
                         options=[
                             {"label": "Grouped Bar Chart", "value": "grouped"},
                             {"label": "Stacked Bar Chart", "value": "stacked"},
                             {"label": "Scatter Plot", "value": "scatter"},
                             {"label": "Scatter Geo Plot", "value": "scatter_geo"},
                         ]),
        ]),
        # Parameter To Compare
        dbc.FormGroup([
            dbc.Label("Choose Category To Compare"),
            dcc.Dropdown(id="cat_dropdown", value=categorical_options[0],
                         options=[{"label": label, "value": label} for label in categorical_options]),
        ]),
    ], body=True)

    tab3_content = dbc.Card([
        html.H3(children='Comparing Categorical Data'),
        html.H6(children='Size of the Scatter Plots are related to GDP per Capita'),
        dbc.Row([
            dbc.Col(categorical_bar_parameter_selection_card, md=12)
        ]),
        dbc.Col(dcc.Graph(id='cat_graph'), md=12)
    ], body=True)

    @app.callback(
        Output('cat_graph', 'figure'),
        [
            Input('cat_dropdown', 'value'),
            Input('cat_type_dropdown', 'value')
        ]
    )
    def categorical_rep(cat_val, cat_type):
        if cat_type == "grouped":
            fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', barmode='group')
        elif cat_type == "stacked":
            fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year')
        elif cat_type == "scatter_geo":
            fig = px.scatter_geo(df, locations="country", locationmode="country names", color=cat_val,
                                     size="gdp_per_capita ($)", animation_frame='year')
        else:
            fig = px.scatter(df, x='country', y='suicides_no', color=cat_val, size="gdp_per_capita ($)",
                             animation_frame='year')
        fig.update_layout(width=1053, height=780, xaxis=dict(tickangle=45), uniformtext=dict(minsize=10),
                          transition={'duration': 1000})

        # ---- OLD CODE - BEFORE Professor's Remarks ---- #

        # if cat_type == "grouped":
        #     if cat_val == categorical_options[0]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', width=1200,
        #                      height=800, barmode='group')
        #         fig.update_layout(transition={'duration': 1000})
        #     elif cat_val == categorical_options[1]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', width=1200,
        #                      height=800, barmode='group')
        #     elif cat_val == categorical_options[2]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', height=800,
        #                      width=1200, barmode='group')
        #     else:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', height=800,
        #                      width=1200, barmode='group')
        # elif cat_type == "stacked":
        #     if cat_val == categorical_options[0]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', width=1200,
        #                      height=800)
        #         fig.update_layout(transition={'duration': 1000})
        #     elif cat_val == categorical_options[1]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', width=1200,
        #                      height=800)
        #     elif cat_val == categorical_options[2]:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', height=800,
        #                      width=1200)
        #     else:
        #         fig = px.bar(df, x='country', y=df["suicides_no"], color=cat_val, animation_frame='year', height=800,
        #                      width=1200)
        # elif cat_type == "scatter_geo":
        #     if cat_val == categorical_options[0]:
        #         fig = px.scatter_geo(df, locations="country", locationmode="country names", color=cat_val,
        #                              size="gdp_per_capita ($)", animation_frame='year')
        #     elif cat_val == categorical_options[1]:
        #         fig = px.scatter_geo(df, locations="country", locationmode="country names", size="gdp_per_capita ($)",
        #                              color=cat_val, animation_frame='year')
        #     elif cat_val == categorical_options[2]:
        #         fig = px.scatter_geo(df, locations="country", locationmode="country names", size="gdp_per_capita ($)",
        #                              color=cat_val, animation_frame='year')
        #     else:
        #         fig = px.scatter_geo(df, locations="country", locationmode="country names", size="gdp_per_capita ($)",
        #                              color=cat_val, animation_frame='year')
        # else:
        #     if cat_val == categorical_options[0]:
        #         fig = px.scatter(df, x='country', y='suicides_no', color=cat_val, size="gdp_per_capita ($)",
        #                          animation_frame='year')
        #     elif cat_val == categorical_options[1]:
        #         fig = px.scatter(df, x='country', y='suicides_no', color=cat_val, size="gdp_per_capita ($)",
        #                          animation_frame='year')
        #     elif cat_val == categorical_options[2]:
        #         fig = px.scatter(df, x='country', y='suicides_no', color=cat_val, size="gdp_per_capita ($)",
        #                          animation_frame='year')
        #     else:
        #         fig = px.scatter(df, x='country', y='suicides_no', color=cat_val, size="gdp_per_capita ($)",
        #                          animation_frame='year')


        return fig
    # Third Tab END

    # Fourth Tab:
    countryWide1 = dbc.Card([
        dbc.FormGroup([
            dbc.Label("Choose First Value"),
            dcc.Dropdown(id="cw_dropdown_1", value=country_wide_options[0],
                         options=[{"label": label, "value": label} for label in country_wide_options]),
            dbc.Label("Choose Second Value"),
            dcc.Dropdown(id="cw_dropdown_2", value=country_wide_options[0],
                         options=[{"label": label, "value": label} for label in country_wide_options]),
        ]),
    ], body=True)

    tab4_content = dbc.Card([
        dbc.FormGroup([
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph6', figure=country_y_g.suicide_by_year(df)))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph4', figure=country_y_g.GenerationSuicide(df)))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph5', figure=country_y_g.suicide_age(df)))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph7', figure=country_y_g.gdp_year(df)))
            ]),
            dbc.Row([
                dbc.Col(dcc.Graph(id='graph8', figure=country_y_g.gdp_suicide_contour(df)))
            ])
        ]),
        html.Hr(),
        html.H3(children='Features Co-relation'),
        dbc.Card([
            dbc.Row([
                dbc.Col(countryWide1, md=12),
                dbc.Col(dcc.Graph(id='cw_graph1'), md=12)
            ])
        ], body=True)
    ], body=True)

    @app.callback(
        Output('cw_graph1', 'figure'),
        [Input('cw_dropdown_1', 'value'),
         Input('cw_dropdown_2', 'value')]
    )
    def correlation(val1, val2):
        corr = df.corr()
        df_1 = df[['suicides_no', 'suicides/100k pop']]
        df_2 = df[['suicides/100k pop', 'gdp_per_capita ($)']]
        df_3 = df[['gdp_per_capita ($)', 'suicides_no']]
        df_1 = df_1.corr()
        df_2 = df_2.corr()
        df_3 = df_3.corr()

        fig = px.imshow(corr, color_continuous_scale=px.colors.diverging.Tealrose)
        if (val1 == country_wide_options[0] and val2 == country_wide_options[1]) | (
                val2 == country_wide_options[0] and val1 == country_wide_options[1]):
            fig = px.imshow(df_1, color_continuous_scale=px.colors.diverging.Tealrose)
        elif (val1 == country_wide_options[1] and val2 == country_wide_options[2]) | (
                val2 == country_wide_options[1] and val1 == country_wide_options[2]):
            fig = px.imshow(df_2, color_continuous_scale=px.colors.diverging.Tealrose)
        elif (val1 == country_wide_options[0] and val2 == country_wide_options[2]) | (
                val2 == country_wide_options[0] and val1 == country_wide_options[2]):
            fig = px.imshow(df_3, color_continuous_scale=px.colors.diverging.Tealrose)
        return fig
    # Fourth Tab END

    # Fifth Tab: By Continent
    tab5_content = dbc.Card([tabContinent()], body=True)
    # Fifth Tab END

    # Main Layout
    app.layout = dbc.Container([
        html.H1(children='Binary Vision - Suicide Rate Visualization and Prediction',
                style={"margin-top": 50}),
        html.Div(children='Visualization on suicide data', className="mb-3"),
        html.Div(
            [
                dbc.Button(
                    "Group Members - Binary Vision",
                    id="collapse-button",
                    className="mb-3",
                    color="success",
                ),
                dbc.Collapse(
                    dbc.Card(dbc.CardBody([
                        dbc.Row([
                            dbc.Col([html.Div("B00851387"), html.Div("Jay Gajjar")],
                                    style={"border": "1px solid green", "margin-right": 10}),
                            dbc.Col([html.Div("B00854837"), html.Div("Teja Alle")],
                                    style={"border": "1px solid green", "margin-right": 10}),
                        ], style={"margin-bottom": 10, "text-align": "left"}),
                        dbc.Row([
                            dbc.Col([html.Div("B00853757"), html.Div("Shivani Sharma")],
                                    style={"border": "1px solid green", "margin-right": 10}),
                            dbc.Col([html.Div("B00843516"), html.Div("Krutin Trivedi")],
                                    style={"border": "1px solid green", "margin-right": 10}),
                        ], style={"text-align": "left"}),
                    ], style={"padding": 30})),
                    id="collapse",
                ),
            ], className="mb-3", style={"text-align": "right"}
        ),
        html.Hr(style={"margin-top": 50, "margin-bottom": 50}),
        dbc.Tabs([
            dbc.Tab(tab1_content, label="Overview & Prediction",
                    tab_style={"border": "1px solid green", "border-bottom": "0px", "margin-right": 10, "border-radius": 5, "font-size":14},
                    style={"border": "1px solid green", "border-radius": 5}),
            dbc.Tab(tab2_content, label="Visualization by Country",
                    tab_style={"border": "1px solid #00aef9", "border-bottom": "0px", "margin-right": 10, "border-radius": 5, "font-size":14},
                    style={"border": "1px solid #00aef9", "border-radius": 5}),
            dbc.Tab(tab3_content, label="Visualization by Category",
                    tab_style={"border": "1px solid gray", "border-bottom": "0px", "margin-right": 10, "border-radius": 5, "font-size":14},
                    style={"border": "1px solid gray", "border-radius": 5}),
            dbc.Tab(tab4_content, label="Corelation between attributes ",
                    tab_style={"border": "1px solid red", "border-bottom": "0px","margin-right": 10, "border-radius": 5, "font-size":14},
                    style={"border": "1px solid red", "border-radius": 5}),
            dbc.Tab(tab5_content, label="Visualization by Continent",
                    tab_style={"border": "1px solid blue", "border-bottom": "0px", "border-radius": 5, "font-size":14},
                    style={"border": "1px solid blue", "border-radius": 5}),
        ]),
        html.Hr(style={"margin-top": 50, "margin-bottom": 50}),
    ])

    @app.callback(
        Output("collapse", "is_open"),
        [Input("collapse-button", "n_clicks")],
        [State("collapse", "is_open")],
    )
    def toggle_collapse(n, is_open):
        if n:
            return not is_open
        return is_open
    # Main Layout END

    return app


if __name__ == "__main__":
    app_t = visulaize()
    app_t.run_server(debug=True)
