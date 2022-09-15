from dash import Dash, html, dcc, dash_table, Input, Output, State
import dash_bootstrap_components as dbc
import plotly.express as px
import pandas as pd
import cs411_project_mysql
import cs411_project_mongo
import cs411_project_neo4j
import cs411_project_scholarly

all_faculty_name = cs411_project_mysql.all_faculty_name()
all_keyword = cs411_project_mysql.all_keyword()

app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

app.layout = html.Div([
    html.H1(['Exploration of Faculty in The Academic World'], style={'text-align':'center'}),
    dbc.Row([
        html.Div([
            html.H4(['Please Select Faculty Name To Display Basic Info'], style={'text-align':'center'}),
            dcc.Dropdown(
                id='faculty_name_dropdown',
                options=[{"label": x[0], "value": x[0]} for x in all_faculty_name],
            ),
            html.Br(),
            dash_table.DataTable(
                id='faculty_info_table',
                columns=[{'name': 'Position', 'id': 'Position'}, {'name': 'Email', 'id': 'Email'}, {'name': 'Phone', 'id': 'Phone'}, {'name': 'University', 'id': 'University'}],
                editable=True,
                style_cell={'textAlign': 'left'}
            ),
            html.Button("Update Faculty Basic Info", id="update_faculty_mongo"),
            html.Div(id="placeholder"),
        ]),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.Img(id='faculty_image', style={'width': '400px'}),
            ]), width={"size": 4, "offset": 1},
        ),
        dbc.Col(
            html.Div([
                html.H4(['Faculty Number of Publications By Year'], style={'text-align':'center'}),
                dcc.Graph(id="faculty_publication_bar_chart", figure={}),
            ]), width=7
        ),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H4(['Please Select Faculty Name To Search Latest Publications'], style={'text-align':'center'}),
                dcc.Dropdown(
                    id='faculty_name_dropdown_2',
                    options=[{"label": x[0], "value": x[0]} for x in all_faculty_name],
                ),
                html.H4(['Publications In 2022 From Google Scholar Profile'], style={'text-align':'center'}),
                dash_table.DataTable(
                    id = 'pub_2022_table',
                    columns=[{'name': 'Title', 'id': 'title'}, {'name': 'Venue', 'id': 'venue'}, {'name': 'Year', 'id': 'year'}],
                    style_cell={'textAlign': 'left', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'overflowX': 'auto'}
                ),
                html.Div(id="placeholder2"),
                html.Button("Insert New Publications", id="update_publication_sql"),
            ]), width=12
        ),
    ]),
    html.Br(),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H4(['Select Faculty By Keyword'], style={'text-align':'center'}),
                dcc.Dropdown(
                    id='keyword_dropdown',
                    options=[{"label": x[0], "value": x[0]} for x in all_keyword],
                ),
                html.Div(id="top_faculty_table")
            ]), width=5
        ),
        dbc.Col(
            html.Div([
                html.H4(['Display Fields Of Interests By Faculty'], style={'text-align':'center'}),
                dcc.Dropdown(
                    id='faculty_name_dropdown_3',
                    options=[{"label": x[0], "value": x[0]} for x in all_faculty_name],
                ),
                dcc.Graph(id="faculty_keyword_pie_chart", figure={}),
            ]), width=7
        ),
    ]),
    html.Br(),
    html.Br(),
    dbc.Row([
        dbc.Col(
            html.Div([
                html.H4(['Please Select Two Faculty To Display Co-authored Publications'], style={'text-align':'center'}),
                dcc.Dropdown(
                    id='faculty_1',
                    options=[{"label": x[0], "value": x[0]} for x in all_faculty_name],
                ),
                dcc.Dropdown(
                    id='faculty_2',
                    options=[{"label": x[0], "value": x[0]} for x in all_faculty_name],
                ),
                html.Div(id="coauthor_publication_list")
            ]), width=12
        ),
    ]),
])

@app.callback(
    [Output(component_id='faculty_info_table', component_property='data'),
     Output(component_id='faculty_image', component_property='src'),
     Output(component_id='faculty_publication_bar_chart', component_property='figure')],
    Input(component_id='faculty_name_dropdown', component_property='value')
)
def show_faculty_info(name):
    faculty_info = cs411_project_mongo.faculty_info_by_name(name)
    faculty_publication_info = cs411_project_mysql.faculty_publication_by_year(name)
    if faculty_info:
        data=[{'Position':faculty_info['position'], 'Email':faculty_info['email'], 'Phone':faculty_info['phone'], 'University':faculty_info['affiliation']['name']}]
        faculty_publication_df = pd.DataFrame(faculty_publication_info, columns =['Year', 'Number_of_Publications'])
        fig = px.bar(faculty_publication_df, x="Year", y="Number_of_Publications")
        return data, faculty_info['photoUrl'], fig
    else:
        return [{'Position':'', 'Email':'', 'Phone':'', 'University':''}], '', {}

@app.callback(
    Output(component_id='pub_2022_table', component_property='data'),
    Input(component_id='faculty_name_dropdown_2', component_property='value')
)
def faculty_2022_pub(name):
    if not name:
        return []
    faculty_2022_pub = cs411_project_scholarly.google_scholar(name)
    if faculty_2022_pub == -1:
        return []
    else:
        return faculty_2022_pub

@app.callback(
    Output("placeholder", "children"),
    Input("update_faculty_mongo", "n_clicks"),
    [State("faculty_info_table", "data"),
     State(component_id='faculty_name_dropdown', component_property='value')],
    prevent_initial_call=True
)
def update_faculty_mongo(n_clicks, data, name):
    data = data[0]
    university_info = cs411_project_mysql.university_info(data['University'])
    cs411_project_mongo.update_faculty_info(data, name, university_info)
    return ""

@app.callback(
    Output("placeholder2", "children"),
    Input("update_publication_sql", "n_clicks"),
    [State("pub_2022_table", "data"),
     State(component_id='faculty_name_dropdown_2', component_property='value')],
    prevent_initial_call=True
)
def insert_new_publications(n_clicks, data, name):
    cs411_project_mysql.insert_publications(n_clicks, data, name)
    return ""

@app.callback(
    Output(component_id='top_faculty_table', component_property='children'),
    Input(component_id='keyword_dropdown', component_property='value')
)
def top_faculty_by_keyword(keyword):
    faculty_keyword_info = cs411_project_mysql.top_faculty_by_keyword(keyword)
    if faculty_keyword_info:
        faculty_table = dash_table.DataTable(
            columns=[{'name': 'Top Faculty', 'id': 'faculty'}, {'name': 'Keyword Score', 'id': 'score'}],
            data = [{"faculty": x[0], "score": x[1]} for x in faculty_keyword_info],
            style_cell={'textAlign': 'left'}
        )
        return faculty_table
    else:
        return ''

@app.callback(
    Output(component_id='coauthor_publication_list', component_property='children'),
    [Input(component_id='faculty_1', component_property='value'),
     Input(component_id='faculty_2', component_property='value')]
)
def coauthor(f1, f2):
    coauthor_info = cs411_project_neo4j.match_faculty(f1, f2)
    if coauthor_info:
        coauthor_table = dash_table.DataTable(
            columns=[{'name': 'Co-authored Publications', 'id': 'Publications'}],
            data = [{"Publications": x['p.title']} for x in coauthor_info],
            style_cell={'textAlign': 'left', 'minWidth': '180px', 'width': '180px', 'maxWidth': '180px', 'overflowX': 'auto'}
        )
        return coauthor_table
    else:
        return 'No co-authored publication'

@app.callback(
    Output(component_id='faculty_keyword_pie_chart', component_property='figure'),
    Input(component_id='faculty_name_dropdown_3', component_property='value')
)
def show_faculty_keyword_pie_chart(name):
    faculty_keyword = cs411_project_mongo.faculty_keyword_by_name(name)
    if faculty_keyword:
        faculty_keyword = faculty_keyword['keywords']
        faculty_keyword_df = pd.DataFrame(faculty_keyword)
        fig = px.pie(faculty_keyword_df, names="name", values="score")
        return fig
    else:
        return {}

if __name__ == '__main__':
    app.run_server(host = '127.0.0.1', debug=True)
