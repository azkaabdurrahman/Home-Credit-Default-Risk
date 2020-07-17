import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
import pandas as pd
import seaborn as sns
import dash_table
from dash.dependencies import Input, Output, State


def generate_table(dataframe, page_size=10):
    return dash_table.DataTable(
        id='dataTable',
        columns=[{
            "name": i,
            "id": i
        } for i in dataframe.columns],
        data=dataframe.to_dict('records'),
        page_action="native",
        page_current=0,
        page_size=page_size,
    )


app_train = pd.read_csv('app_cleaned3.csv')
app_traint1 = app_train[app_train['TARGET'] == 1]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

app.layout = html.Div(
    children=[
        html.H1('Home Credit Default Risk Dashboard'),
        html.Div(children='''
        by: Naufal Azka Abdurrahman
    '''),
        dcc.Tabs(
            children=[
                dcc.Tab(
                    value='Tab1',
                    label='Graph Example',
                    children=[
                                                
                        html.Div([dcc.Graph( 
                        id = 'pie-chart-all',
                        figure = {'data': [
                        go.Pie(
                        values = [app_train[app_train['CODE_GENDER'] == 'M']['TARGET'].count(),
                        app_train[app_train['CODE_GENDER'] == 'F']['TARGET'].count()],
                        labels = ['Male', 'Female']
                        )], 'layout': go.Layout(title = 'Klien Male dan Female Keseluruhan')
                        })], className = 'col-6'), ### dccgraph 1 ###

                        html.Div([dcc.Graph(
                        id = 'pie-chart-t1',
                        figure = {'data' : [
                        go.Pie(
                        values = [app_traint1[app_traint1['CODE_GENDER'] == 'M']['TARGET'].count(),
                        app_traint1[app_traint1['CODE_GENDER'] == 'F']['TARGET'].count()],
                        labels = ['Male', 'Female']
                        )], 'layout': go.Layout(title = 'Gagal bayar by Sex')}
                        )], className = 'col-6') ### dccgraph 2 ###
                    ], className = 'row'),
                dcc.Tab(
                    value='Tab2',
                    label='Scatter chart',
                    children=[
                        html.Div(children=dcc.Graph(
                            id='graph-scatter',
                            figure={
                                'data': [
                                    go.Scatter(x=app_train[app_train['TARGET'] == i]['AMT_CREDIT'],
                                               y=app_train[app_train['TARGET'] == i]['AMT_INCOME_TOTAL'],
                                               mode='markers',
                                               name='Day {}'.format(i))
                                    for i in app_train['TARGET'].unique()
                                ],
                                'layout':
                                go.Layout(
                                    xaxis={'title': 'AMT_CREDIT'},
                                    yaxis={'title': ' AMT_INCOME_TOTAL'},
                                    title='Income and Credit Scatter Visualization',
                                    hovermode='closest')
                            }))
                    ]),
                dcc.Tab(value='Tab3',
                        label='Data Frame app_train',
                        children=[
                            html.Div(children=[
                                html.Div([
                                    html.P('Target'),
                                    dcc.Dropdown(value='',
                                                 id='filter-target',
                                                 options=[{'label': 'None','value': ''}, {'label': 'Not Failed','value': 0}, 
                                                 {'label': 'Failed','value': 1}])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Sex'),
                                    dcc.Dropdown(value='',
                                                 id='filter-sex',
                                                 options=[{'label': 'None','value': ''}, {'label': 'Female','value': 'F'}, 
                                                 {'label': 'Male','value': 'M'}])
                                ],
                                         className='col-3'),
                                
                                html.Div([
                                    html.P('Contract Type'),
                                    dcc.Dropdown(value='',
                                                 id='filter-contract',
                                                 options=[ {'label': 'Cash loans','value': 'Cash loans'}, 
                                                 {'label': 'Revolving loans','value': 'Revolving loans'},                     
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Own Car'),
                                    dcc.Dropdown(value='',
                                                 id='filter-car',
                                                 options=[{'label': 'Yes','value': 'Y'}, 
                                                 {'label': 'No','value': 'N'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3'),
                                html.Div([
                                    html.P('Own House'),
                                    dcc.Dropdown(value='',
                                                 id='filter-house',
                                                 options=[{'label': 'Yes','value': 'Y'}, 
                                                 {'label': 'No','value': 'N'},
                                                 {'label': 'None','value': ''}])
                                ],
                                         className='col-3')

                            ],
                                     className='row'),
                            html.Br(),
                            html.Div([
                                html.P('Max Rows:'),
                                dcc.Input(id ='filter-row',
                                          type = 'number', 
                                          value = 10)
                            ], className = 'row col-3'),

                            html.Div(children =[
                                    html.Button('search',id = 'filter')
                             ],className = 'row col-4'),
                             
                            html.Div(id='div-table',
                                     children=[generate_table(app_train)])
                        ])
            ],
            ## Tabs Content Style
            content_style={
                'fontFamily': 'Arial',
                'borderBottom': '1px solid #d6d6d6',
                'borderLeft': '1px solid #d6d6d6',
                'borderRight': '1px solid #d6d6d6',
                'padding': '44px'
            })
    ],
    #Div Paling luar Style
    style={
        'maxWidth': '1200px',
        'margin': '0 auto'
    })

@app.callback(
    Output(component_id = 'div-table',component_property = 'children'),
    [Input(component_id = 'filter', component_property = 'n_clicks')],
    [State(component_id = 'filter-row', component_property = 'value'),
    State(component_id = 'filter-target', component_property = 'value'),
    State(component_id = 'filter-sex', component_property = 'value'),
    State(component_id = 'filter-contract', component_property = 'value'),
    State(component_id = 'filter-car', component_property = 'value'),
    State(component_id = 'filter-house', component_property = 'value')
    ]
)

def update_table(n_clicks, row, target, sex, contract, car, house):
    app_train = pd.read_csv('app_cleaned3.csv')
    if target != '':
        app_train = app_train[app_train['TARGET'] == target]
    if sex != '':
        app_train = app_train[app_train['CODE_GENDER'] == sex]
    if contract != '':
        app_train = app_train[app_train['NAME_CONTRACT_TYPE'] == contract]
    if car != '':
        app_train = app_train[app_train['FLAG_OWN_CAR'] == car]
    if house != '':
        app_train = app_train[app_train['FLAG_OWN_REALTY'] == house]
    
    children = [generate_table(app_train, page_size = row)]
    return children
    
    


if __name__ == '__main__':
    app.run_server(debug=True)