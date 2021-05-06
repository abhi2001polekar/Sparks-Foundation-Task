import dash
import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from numpy import random

random.seed(101)
us_state_code = {     #mapping through dictionary
    'Alabama': 'AL',
    'Alaska': 'AK',
    'American Samoa': 'AS',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'District of Columbia': 'DC',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Guam': 'GU',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Northern Mariana Islands':'MP',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Puerto Rico': 'PR',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virgin Islands': 'VI',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY'
}
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.LUX])

df = pd.read_csv('SampleSuperstore.csv')
df['code']=df['State']
df.replace({"code": us_state_code},inplace=True)  #mapping dictionary to state code



n_by_state = df.groupby(by=["code","State"])[["Profit","State","Sales","Discount"]].mean().reset_index()

df['sum_of_profit']  = df['Sales']
n_by_state['text'] = n_by_state['State']
for i in n_by_state.index:
    n_by_state['text'].iloc[i] = str(n_by_state['State'].iloc[i]) + '<br>' + \
                                'Average Sales ' + str(n_by_state['Sales'].iloc[i]) +"<br>"+ \
                                'Average Profit ' + str(n_by_state['Profit'].iloc[i]) +"<br>"+ \
                                 'Average Discount Offer ' + str(n_by_state['Discount'].iloc[i]) + "<br>"



col = df.columns
fig = go.Figure(data=go.Choropleth(
    locations=n_by_state['code'],
    z=n_by_state['Profit'],
    locationmode='USA-states',
    colorscale='RdBu',
    showscale=False,
    autocolorscale=False,
    text=n_by_state['text']
))
fig.update_traces(
    marker_line_color="white", # line markers between states


)
fig.update_layout(
    showlegend=False,
    title={
        'text': "MAP PLOTTING (USA)",
        'y':0.9,
        'x':0.5,
        'xanchor': 'center',
        'yanchor': 'top'
    },
    xaxis=dict(
            fixedrange=True
        ),
    yaxis=dict(
            fixedrange=True
        ),
    margin=dict(t=0,b=0,l=0,r=0),
    font={
      'color':'black'
    },
    geo = dict(
        scope='usa',
        projection=go.layout.geo.Projection(type = 'albers usa'),
        showlakes=True, # lakes
    )
)
#sunburst vala graph
fig2 = px.sunburst(df, path=['Region','Category','Segment'], values='Sales', color='Region',color_discrete_sequence= px.colors.sequential.RdBu)
fig2.update_layout(
    title={
        'text' : 'Sales according to region'
    },
    height=550,
)


#bubble graph coding
by_state1 = df.groupby(by=["State"])[["Sales","Profit","Quantity"]].max().reset_index()
by_state1["quantity_jitter"] = by_state1["Quantity"] + random.randint(-20,-5,len(by_state1)) * 0.37
fig_bub = px.scatter(by_state1, x="quantity_jitter", y="Profit",size="Sales", color="State",
                     hover_name="State", log_y=True, size_max=60,
                     color_discrete_sequence= px.colors.sequential.Turbo)
fig_bub.update_layout(
margin=dict(b=0,l=0,r=0),
    title={
        'text':"sales and profit chart according to state".upper()
    },
    xaxis={
        'title' : 'Maximum Quantity of product sale'.upper()
    },
    yaxis={
        'title' : 'profit'.upper()
    }
)

#Profit base
pro_li_based_on_profit = n_by_state[n_by_state["Profit"] < 0 ].sort_values("Profit")["State"].to_list()
sales_li_based_on_profit = n_by_state[n_by_state["Profit"] < 0 ].sort_values("Sales")["State"].to_list()

print(sales_li_based_on_profit)
print("-"*10)
print(pro_li_based_on_profit)
#Sales Base


s_l=[]
p_l=[]
i=0
for s_prof in pro_li_based_on_profit:
    j=0
    for s_sale in sales_li_based_on_profit:
        if sales_li_based_on_profit[j] == pro_li_based_on_profit[i]:
            p_l.append(i)
            s_l.append(j)

        j = j + 1

    i = i + 1

result_l=[]
for item_sales in s_l:
    j = 0
    for item_profit in p_l:
        if item_profit == item_sales:
            result_l.append(j)
            break
        j+=1

index_of_smallest_value_in_result_l = result_l.index(min(result_l))

pro_li_based_on_sales = n_by_state[n_by_state["Sales"] < 120 ].sort_values("Profit")["State"].to_list()
sales_li_based_on_sales = n_by_state[n_by_state["Sales"] < 120 ].sort_values("Sales")["State"].to_list()

s1=[]
l1=[]
i=0
for s_prof in pro_li_based_on_sales:
    j=0
    for s_sale in sales_li_based_on_sales:
        if sales_li_based_on_sales[j] == pro_li_based_on_sales[i]:
            l1.append(i)
            s1.append(j)
        j = j + 1
    i = i + 1

result_l1=[]
for item_sales in s1:
    j = 0
    for item_profit in l1:
        if item_profit == item_sales:
            result_l1.append(j)
            break
        j+=1

index_of_smallest_value_in_result_l1 = result_l1.index(min(result_l1))




app.layout = html.Div([
    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.CardDeck(id="card-deck-header",children=[
                dbc.Card([
                    dbc.CardHeader(html.H6("States Count")),
                    dbc.CardBody([
                        html.H4([
                            str(len(df["State"].unique())) + ""
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Cities Count")),
                    dbc.CardBody([
                        html.H4([
                            str(len(df["City"].unique())) + ""
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Segments Count")),
                    dbc.CardBody([
                        html.H4([
                            str(len(df["Segment"].unique())) + ""
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Category Count")),
                    dbc.CardBody([
                        html.H4([
                            str(len(df["Category"].unique())) + ""
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Sub-Category Count")),
                    dbc.CardBody([
                        html.H4([
                            str(len(df["Sub-Category"].unique())) + ""
                        ], className="card-title"),
                    ]),
                ])
            ])
        ],width={'size':10,'offset':1})
    ]),

    html.Br(),
    dbc.Row([
        dbc.Col([
            dbc.CardDeck(id="next-card-deck",children=[
                dbc.Card([
                    dbc.CardBody([
                        dcc.Loading(id="loading1",
                                    type="cube",
                                    color="#36146C",
                                    children=html.Div(
                                        [dcc.Graph(id="map-graph", figure=fig, config={'scrollZoom': False})])),
                    ],className="border border-info")
                ]),
                dbc.Card([
                    dbc.CardBody([
                        dcc.Loading(id="loading2",
                                    type="cube",
                                    color="#36146C",
                                    children=html.Div([dcc.Graph(id="sunburst-graph", figure=fig2)]))
                    ])
                ],className="border border-info"),
            ])
        ],width={'size':10,'offset':1}),
    ]),


    html.Br(),

    dbc.Row([
       dbc.Col([
           dbc.CardDeck(id="weak-card-deck",
                        children=[
                dbc.Card([
                    dbc.CardHeader(html.H6("Weak State according to Profit")),
                    dbc.CardBody([
                        html.H5([
                            n_by_state["State"].iloc[n_by_state["Profit"].idxmin()]
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Weak State according to Sales")),
                    dbc.CardBody([
                        html.H5([
                            n_by_state["State"].iloc[n_by_state["Sales"].idxmin()]
                        ], className="card-title"),
                    ]),
                ]),
                dbc.Card([
                    dbc.CardHeader(html.H6("Weak State (According To Both Sales And Profit)")),
                    dbc.CardBody([
                        html.H5([
                            "1) " + pro_li_based_on_profit[index_of_smallest_value_in_result_l],
                            html.Br(),

                            "2) " + pro_li_based_on_sales[index_of_smallest_value_in_result_l1] + ""
                        ], className="card-title"),
                    ]),
                ])
           ])
       ],width={'size':10,'offset':1})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([
            dbc.CardDeck(id="new-card-deck",
                         children=[
                            dbc.Card([
                                dbc.CardBody([
                                    dcc.Loading(id="load1",
                                        type="cube",
                                        color="#36146C",
                                        children=html.Div([dcc.Graph(id="bubble-graph",figure=fig_bub)]))
                                ])
                            ], className="border border-info")
                        ])
        ],width={'size':10,'offset':1})
    ]),

    html.Br(),

    dbc.Row([
        dbc.Col([

            dbc.CardDeck(id="btn-card-deck-srop",
                         children=[
                            dbc.Card([
                                dbc.CardHeader(html.H6("Select State")),
                                dbc.CardBody([
                                    dcc.Dropdown(id='drop1',
                                                 options=[{'label': str(i), 'value': i} for i in df['State'].unique()],
                                                 value="California",
                                                 clearable=False,
                                                 placeholder="Select State Name"
                                                 )
                                ])
                            ]),
                            dbc.Card([
                                dbc.CardHeader(html.H6("Select City")),
                                dbc.CardBody([
                                    dcc.Dropdown(id='drop2',
                                                 clearable=False,
                                                 placeholder="Select City Names",
                                                 value="San Francisco"
                                                 ),
                                ])
                            ]),
                            dbc.Card([
                                dbc.CardBody([
                                    dbc.Button("SHOW",id="btnShow",type="button",
                                                className="btn btn-info",
                                                style={'width':'100%','height':'auto','margin-top':'auto','margin-bottom':'auto'})
                                ])
                            ],body=True),
                        ]),

        ],width={'size':10,'offset':1}),
    ]),

    html.Br(),
    dbc.Row([
                dbc.Col([
            dcc.Loading(id="loading3",
                        type="cube",
                        color="#36146C",
                        children=html.Div([dcc.Graph(id="bar-graph")], className="border border-info"))
        ],width={'size':10,'offset':1})
    ]),#end this row

    html.Br(),

    dbc.Row([
        dbc.Col([

            dbc.CardDeck([
                            dbc.Card([

                                dbc.CardBody([
                                    dcc.Checklist(
                                        id="all-or-none",
                                        options=[{"label": "Select All", "value": "All"}],
                                        labelStyle={"display": "inline-block"},
                                    ),
                                    dcc.Checklist(
                                        id="my-checklist",
                                        options=[{'label':str(i),'value': str(i) } for i in df['State'].unique()],
                                        value=["California"],
                                        labelStyle={"display": "inline-block", 'margin-right':'10px'}
                                    ),
                                    html.Hr(),
                                    dbc.Button("SHOW GRAPH",id="btn_checklist",type="button",className="btn btn-info")
                                ])
                            ],body=True),
                            dbc.Card([

                                dbc.CardBody([
                                    dcc.Loading(id="load-graph",
                                                type="cube",
                                                color="#36146C",
                                                children=html.Div(
                                                    [dcc.Graph(id="bar-graph-1", style={})],
                                                    ))
                                ])
                            ],body=True),
                ])
          ],width={'size':10,'offset':1})
    ]),

    html.Br(),

])

color_bar = ['rgb(0, 102, 0)', 'rgb(255, 191, 0)','#AF0038' , 'rgb(102, 197, 204)']
@app.callback(Output("bar-graph-1","figure"),
              [Input("btn_checklist","n_clicks")],
              [State("my-checklist","value")])
def update_bar1(btn,state_checkllist):

    df_groupby_state_for_category = df.groupby(by=["State","Category"])[col].mean().reset_index()
    fig_1 = go.Figure()
    for item in state_checkllist:
        i=0
        # fig_1.up_trace()
        for cat in df_groupby_state_for_category["Category"].unique():
            fig_1.add_trace(go.Bar(
                x=[item],
                y=df_groupby_state_for_category[(df_groupby_state_for_category["State"]==item) & (df_groupby_state_for_category["Category"]==cat)]["Sales"],
                marker={
                    'color': color_bar[i]
                },
                #showlegend=False,
                legendgroup=cat,
                name=cat
            ))
            i=i+1

    names = set()
    fig_1.for_each_trace(
        lambda trace:
        trace.update(showlegend=False)
        if (trace.name in names) else names.add(trace.name))

    fig_1.update_layout(barmode="stack",
                        margin=dict( b=0, l=0, r=0),
                        showlegend=True,
                        title={
                            'text' : "comparison between Sales of each category per state".upper()
                        })
    fig_1.update_xaxes(tickangle=-90)

    return fig_1



@app.callback(Output("drop2","options"),
              [Input("drop1","value")])
def update_city_by_state(state):

    df_city = df[df["State"] == state]
    li_cities = []
    for city in df_city["City"].unique():
        li_cities.append({"label":str(city),"value":city})

    return li_cities

@app.callback(Output("bar-graph","figure"),
              [Input("btnShow","n_clicks")],
              [State("drop1","value"),
               State("drop2","value")])
def update_by_state(n_click_btn,state_name,city_name):
    if state_name and city_name:
        df_city_name = df[(df['City'] == city_name) & (df["State"] == state_name)]

        df_groupby_city = df_city_name.groupby(["Sub-Category"])[col].mean().reset_index()


        figure = go.Figure()

        df_groupby_city['text'] = df_groupby_city['Sub-Category']
        for i in df_groupby_city.index:
            if df_groupby_city['Profit'].iloc[i] < 0:
                df_groupby_city['text'].iloc[i] = str(state_name) + "<br>" + \
                                                  "Average Sales in " + str(city_name) + " " + str(df_groupby_city['Sales'].iloc[i]) + "<br>" + \
                                                  "Average Profit in " + str(city_name) + " " + str(df_groupby_city['Profit'].iloc[i]) + "(loss)<br>" + \
                                                  "Average Quantity in " + str(city_name) + " " + str(df_groupby_city['Quantity'].iloc[i])
            else:
                df_groupby_city['text'].iloc[i] = str(state_name) + "<br>" + \
                                                  "Average Sales in " + str(city_name) + " " + str(df_groupby_city['Sales'].iloc[i]) + "<br>" + \
                                                  "Average Profit in " + str(city_name) + " " + str(df_groupby_city['Profit'].iloc[i]) + "<br>" + \
                                                  "Average Quantity in " + str(city_name) + " " + str(df_groupby_city['Quantity'].iloc[i])

        for item in df_groupby_city["Sub-Category"].unique():
            figure.add_trace(go.Scatter(x=df_groupby_city[df_groupby_city["Sub-Category"] == item]["Sub-Category"],
                                    y=df_groupby_city[df_groupby_city["Sub-Category"] == item]["Profit"],
                                    text=df_groupby_city[df_groupby_city["Sub-Category"] == item]["text"],
                                    mode='markers',
                                    marker=dict(
                                        size=(df_groupby_city[df_groupby_city["Sub-Category"] == item]["Sales"]/df_groupby_city["Sales"].sum())*430,
                                    ),
                                    name=item))
        figure.update_layout(
            title={
              'text' : ""+(city_name)+" wise sub-category sales and profit chart".upper()
            },
            yaxis={
                'title': 'Profit'.upper()
            },

            xaxis={
                'title': 'Sub-Categories'.upper()
            },

            margin=dict(t=30, b=20, l=0, r=0)
        )
        figure.update_xaxes(showspikes=True)
        figure.update_yaxes(showspikes=True)
        return figure
        # return {
        #     'layout': {
        #         'title': 'Empty Bar Chart'
        #     }
        # }
    else:
        return {
            'layout':{
                'title':'Empty Bar Chart'
            }
        }


@app.callback(
    Output("my-checklist", "value"),
    [Input("all-or-none", "value")],
    [State("my-checklist", "options")],
)
def select_all_none(all_selected, options):
    all_or_none = []
    all_or_none = [option["value"] for option in options if all_selected]
    return all_or_none

if __name__ == '__main__':
    app.run_server(debug=True)