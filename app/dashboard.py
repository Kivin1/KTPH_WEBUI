import dash
import dash_html_components as html
import dash_core_components as dcc
import dash_table_experiments as dt
import pandas as pd
import io
import copy
from dash.dependencies import Input, Output, State
import base64
import random as re
import math
import os






mapbox_access_token = 'pk.eyJ1IjoiamFja2x1byIsImEiOiJjajNlcnh3MzEwMHZtMzNueGw3NWw5ZXF5In0.fk8k06T96Ml9CLGgKmk81w'  # noqa: E501

layout = dict(
    autosize=True,
    #height=300,
    font=dict(color='#696969'),
    titlefont=dict(color='#696969', size='14'),
    margin=dict(
        l=35,
        r=35,
        b=35,
        t=45
    ),

    hovermode="closest",
    #plot_bgcolor="#fff8dc",
    #paper_bgcolor="#ffdead",
    legend=dict(font=dict(size=10), orientation='h'),
    title='Satellite Overview',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        style="white",
        center=dict(
            lon=-78.05,
            lat=42.54
        ),
        zoom=10,
    )
)


app = dash.Dash()


app.layout = html.Div([

    html.Div(
    [
         html.Div(
            [
            html.Div(
                [html.P('Khoo Teck Paut Hospital - Quality Service Management',
                
                    #className='eight columns',
                 style={'color': 'white', 
                 'fontSize':'27',             
                 }
                )],
                style = {'background-color':'#696969'},
                ),

            html.Img(
                src="https://media.licdn.com/media/AAIA_wDGAAAAAQAAAAAAAA2_AAAAJGE3NDIyY2FiLWRmYTYtNDQyYS1hNTliLWNkMzFiY2ZiN2RjYw.png",
                style={
                    'height': '85',
                    'width': '225',
                    'right':'20',
                    'top':'0',
                    'position': 'absolute',
                },
            ),
            ],
            #className='row',
            style = {'background-color':'#696969'},
            ),
        
        html.Div(
            [

                html.Div(
                    [   html.P('Filter by Department:',className ='two columns'),   
                        html.P('Gender:',className ='two columns'),
                        html.P('Age:',className ='two columns'),
                        html.P('Education Level:',className ='two columns'),
                        html.P('Race:',className ='two columns'),
                    ],
                    className='row'

                    ),

                html.Div(
                    [   
                        dcc.Dropdown(
                        id='department',
                        options=[{'label':'All', 'value':'All'},
                                 {'label': 'A&E', 'value': 'A&E'},
                                 {'label': 'HFU', 'value': 'HFU'},
                                 {'label': 'AMU', 'value': 'AMU'}],
                       className ='two columns',
                       value = 'All'
                            ),

                        dcc.Dropdown(
                        id='gender',
                        options=[{'label':'All', 'value':'All'},
                                 {'label': 'Male', 'value': 'Male'},
                                 {'label': 'Female', 'value': 'Female'}],
                        value = 'All',
                        className ='two columns',
                        ),
            # {'lable': 'Youth', 'value': 'Youth(18-35)'}
                        dcc.Dropdown(
                        id='age',
                        options=[{'label':'All', 'value':'All'},
                                 {'label': 'Youth', 'value': ' Young(36-45)'},
                                 {'label': 'Middle', 'value': 'Middle Age(36-45)'},
                                 {'label': 'Senior', 'value': 'Senior(46-65)'},
                                 {'label': 'Elderly', 'value': 'Elderly(65 and above)'},
                                 ],
                        value = 'All',
                        className ='two columns',
                        ),

                        html.Div(
                            [  
                                dcc.Dropdown(
                                id='education_level',
                                options=[{'label':'All', 'value':'All'},
                                         {'label': 'PHD', 'value': 'na'},
                                         {'label': 'Mast', 'value': 'na'},
                                         {'label': 'Customize ', 'value': 'na'}],
                                value = 'All',
                                className ='two columns',

                                ),
                            ],
                            style = {'background-color':'#696969'}
                            ),


                        dcc.Dropdown(
                        id='race',
                        options=[{'label':'All', 'value':'All'},
                                 {'label': 'race', 'value': 'na'},
                                 {'label': 'Active only ', 'value': 'na'},
                                 {'label': 'Customize ', 'value': 'na'}],
                        value = 'All',
                        className ='two columns',
                        ),

                            
                         dcc.Upload(
                            id = 'analytics',
                            children=html.Div([
                                 html.Button('Select a File',style={'color':'black'})
                            ],
                        style={
                            #'width': '100%',
                            'height': '40px',
                            'lineHeight': '40px',
                            'borderWidth': '1px',
                            #'borderStyle': 'dashed',
                            'borderRadius': '5px',
                            'textAlign': 'center',
                            'color':'red'
                        },
                        className ='two columns',
                    ),)

                    ],
                    className='row',
                    ),
            ],
            style = {'background-color':'#696969',

            },
            ),

        html.Div(
            
                style = {'background-color':'#696969',
                'height':'140px',}

            ),
        ],
        style = {'background-color':'#696969',}

        ),

    html.Div(
       [ 
        html.Div(
        [
       
            html.Div(
                [
                    dcc.Graph(id = 'main_graph')
                ],
                style={'margin-top': '50px'}
                ),

            html.Div(
                [
                    dcc.Graph(id = 'ratio_complimens_complaints')
                ]
                ),

       


            html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='overallexperience_graph')
                            ],
                            className='six columns',
                            # style={'margin-top': '10'}
                        ),
                        html.Div(
                            [
                                dcc.Graph(id='recommend_graph')
                            ],
                            className='six columns',
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),
            


            html.Div(
                    [
                        html.Div(
                            [
                                dcc.Graph(id='doctor_graph')
                            ],
                            className='six columns',
                            # style={'margin-top': '10'}
                        ),
                        html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'doctor',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'doctor1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'doctor2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'doctor3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ],

                                    
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                # 'height': '270px',
                                # 'lineHeight': '40px',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top':'50px',
                                #'background':'#fff8dc',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                
                                #'textAlign': 'center',
                              
                                'padding':'10px',
                                
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='nurse_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'nurse',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'nurse1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'nurse2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'nurse3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),                
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),


            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='allied_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'allied',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'allied1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'allied2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'allied3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),


            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='environment_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'environment',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'environment1',children = 'unknown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'environment2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'environment3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                'height':'330px',
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),


            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='medication_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'medication',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'medication1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'medication2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'medication3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                'height':'330px',
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='admission_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'admission',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'admission1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'admission2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'admission3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                'height':'330px',
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),

            html.Div(
                [
                    html.Div(
                        [
                            dcc.Graph(id='care_graph')
                        ],
                        className='six columns',
                        # style={'margin-top': '10'}
                    ),
                    html.Div(
                            [
                                html.Div(
                                    [ 
                                        dcc.Markdown(
                                            id= 'care',
                                            children='Sample Feedback',
                                    ),
                                    ],
                                        style={
                                        'textAlign': 'center',}
                                    ),
                                
                                html.Div(
                                    [
                                        html.Li(id = 'care1',children = 'unknown',style={
                                        'textAlign': 'justify',
                                    }),
                                        html.Li(id = 'care2',children='unkown',style={
                                        'textAlign': 'justify',}),
                                        html.Li(id = 'care3',children='unkown',style={
                                        'textAlign': 'justify',}),
                                    ]
                                    ),
                           
                            ],
                            className='six columns',
                            style={
                                #'width': '100%',
                                'width':'fit-content',
                                'width':'-webkit-fit-content',
                                'width':'-moz-fit-content',
                                'margin-top': '50px',
                                #'background':'#fff8dc',
                                # 'lineHeight': '40px',
                                'borderWidth': '1px',
                                'borderStyle': 'dashed',
                                'borderRadius': '5px',
                                #'textAlign': 'center',
                                'height':'330px',
                                
                                'padding':'10px',
                                }
                            # style={'margin-top': '10'}
                        ),
                    ],
                    className='row'
                ),
        ],
        style = {
                # 'width':'350px'
                # 'height':'200px'
                'border': 'solid 3px', #555;
                'background-color': 'white',
                'border-color':'white',
                'box-shadow':'0 0 10px rgba(0,0,0,0.6)',
                '-moz-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                '-webkit-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                '-o-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                'margin':'20px 15px 40px 15px',}),
    ],style = {
                # 'width':'350px'
                # 'height':'200px'
                'border': 'solid 3px', #555;
                'border-color':'#C0C0C0',
                'background-color': '#C0C0C0',
                'box-shadow':'0 0 10px rgba(0,0,0,0.6)',
                '-moz-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                '-webkit-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                '-o-box-shadow': '0 0 10px  rgba(0,0,0,0.6)',
                'margin':'-100px 45px 40px 45px',}),
],style = {'background-color':'#C0C0C0'})



def fetch_main(data):
    Index= ['Jan','Feb','Mar','Apr','May','Jun','July','Aug','Sep','Oct','Nov','Dec']
    unique = list(data.Month.unique())
    index_sort = []
    for i in unique:
        for index, item in enumerate(Index):
            if i == item :
                index_sort.append(index)

                break

    index_sorted = sorted(index_sort)


    index = [Index[x] for x in index_sorted]

    compliment = []
    suggestion = []
    complaint = []
    for i in index:
            data_by_month = data[data['Month'] == i]
            dic = data_by_month['Feedback Type'].value_counts().to_dict()
            try:
                compliment.append(dic['Compliment'])
            except:
                compliment.append(0)

            try:
                suggestion.append(dic['Suggestion'])
            except:
                suggestion.append(0)
            try:
                complaint.append(dic['Complaint'])
            except:
                complaint.append(0)
    feedback = [x+y+z for x, y,z in zip(complaint, suggestion,compliment)]

    return index,compliment,suggestion,complaint,feedback


def fetch_sample(data,category):
    
    cat = data[data.iloc[:,6].isin(category)]
    title = list(cat['Feedback Title'].unique())
    left_title = []
    for i in title:
        if 'compliment' not in i.lower() and 'complimetn' not in i.lower():
            left_title.append(i)

    length = len(left_title)
    
    
    if length <= 3:
        texts = list(set(cat[cat['Feedback Title'].isin(left_title)].Situation))

    else:
        nums = []
        texts = []
        while len(nums) < 3:
            num = re.sample(range(length), 1)
            text = list(cat[cat['Feedback Title']==left_title[num[0]]].Situation)[0]

            if len(text)<= 300 and num not in nums and 'thank' not in text and 'compliment' not in text:
                texts.append(text)
                nums.append(num)
            else:
                continue

    return texts[0],texts[1],texts[2]


def update_index(df_department):
    index = (list(df_department.loc['Overall Experience']))
    Feedback = list(df_department.loc['Feedback'])
    index_update = []
    for i,item in enumerate(index):
        if math.isnan(Feedback[i]) == False:
            index_update.append(item)
    return index_update


@app.callback(Output('main_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def update_output(contents,department,gender,age,education_level,race):
    layout_individual = copy.deepcopy(layout)
    
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_individual['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)

        df_department = df[department]

        Feedback = list(df_department.loc['Feedback'])
        Compliments = list(df_department.loc['Compliments'])
        Complaints = list(df_department.loc['Complaints'])
        Suggestions = list(df_department.loc['Suggestions'])

        index_update = update_index(df_department)

        #total = compliment+suggestion+complaint+feedback
        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= Feedback[i]+100,
                # xref="x",
                # yref="y",
                text= Feedback[i],
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= Compliments[i]+100,
                xref='x',
                yref='y',
                text= Compliments[i],
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= Complaints[i]+100,
                xref='x',
                yref='y',
                text= Complaints[i],
                showarrow= False
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= Suggestions[i]+100,
                xref='x',
                yref='y',
                text= Suggestions[i],
                showarrow= False
                )
            annotations.append(annotation)
        
        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='Feedbacks',
                x=index_update,
                y=Feedback,
                line=dict(
                    shape="spline",
                    smoothing=0.5,
                    width=2,
                    color='#F78A77' #red
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Compliments',
                x=index_update,
                y=Compliments,
                line=dict(
                    shape="spline",
                    smoothing=0.5,
                    width=2,
                    color='#4B9BD2' #blue
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Complaints',
                x=index_update,
                y=Complaints,
               
                
                line=dict(
                    shape="spline",
                    smoothing=0.5,
                    width=2,
                    color='#E4E520'  #yellow
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Suggestions',
                x=index_update,
                y=Suggestions,
                
                line=dict(
                    shape="spline",
                    smoothing=0.5,
                    width=2,
                    color='#6F7979' #grey
                ),
                marker=dict(symbol='diamond-open')
            )

        ]
        layout_individual['annotations'] = annotations
    #layout_individual['yaxis'] = dict(range[,])
    layout_individual['title'] = 'Overview Of Patient Feedback Recieved'
    figure = dict(data=data, layout=layout_individual)

    return figure


@app.callback(Output('ratio_complimens_complaints', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_ratio(contents,department,gender,age,education_level,race):
    layout_ratio = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_ratio['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)

        #index,compliment,suggestion,complaint,feedback = fetch_main(df)
        df_department = df[department]
        #ratio = list(df_department.loc['Compliments Complaint Ratio'])
        index_update = update_index(df_department)
        ratio = [165.4,171.2,165.9,163.2]
    
        #ratio = [x/y for x,y in zip(compliment,complaint)]
    
        annotations = []

        for i,item in enumerate(index_update):
            annotation = dict(
                    x= item,
                    y= ratio[i]+0.2,
                    xref='x',
                    yref='y',
                    text= round(float(ratio[i]),2),
                    showarrow= False
                )
            annotations.append(annotation)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
            
                x=index_update,
                y=ratio,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_ratio['annotations'] = annotations
    layout_ratio['title'] = 'Vistors: Complaints'
    
    figure = dict(data=data, layout=layout_ratio)
    return figure

@app.callback(Output('overallexperience_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def update_output(contents,department,gender,age,education_level,race):

    layout_overallexperience = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_overallexperience['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[0])
        middle_box = list(bf.iloc[0])
        bottom_box = list(cf.iloc[0])
        target = [0.85,0.85,0.85,0.85]

        index_update = update_index(df_department)
        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text='%.2f%%' % (top_box[i] * 100),     #top_box[i],
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_overallexperience['annotations'] = annotations

    layout_overallexperience['title'] = 'Overall Experience Rating'
    figure = dict(data=data, layout=layout_overallexperience)
    return figure

@app.callback(Output('recommend_graph', 'figure'),
             [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_recommend(contents,department,gender,age,education_level,race):
    layout_recommend= copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_recommend['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]

        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[1])
        middle_box = list(bf.iloc[1])
        bottom_box = list(cf.iloc[1])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)
        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)


        data = [

            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_recommend['annotations'] = annotations
    layout_recommend['title'] = 'Recommend KTPH to others'
    figure = dict(data=data, layout=layout_recommend)
    return figure


@app.callback(Output('doctor_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_doctor(contents,department,gender,age,education_level,race): 
    layout_doctor= copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_doctor['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]

        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[2])
        middle_box = list(bf.iloc[2])
        bottom_box = list(cf.iloc[2])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        benchmark = dict(
                x= 'Feb',
                y= 0.8,
                xref="x",
                yref="y",
                text= '85%',
                showarrow= False,
                ),
        annotations.append(benchmark)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_doctor['annotations'] = annotations
    layout_doctor['title'] = "Communications With Doctors Rating"
    figure = dict(data=data, layout=layout_doctor)
    return figure

@app.callback(Output('nurse_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_nurse(contents,department,gender,age,education_level,race): 

    layout_nurse= copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_nurse['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)

        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[3])
        middle_box = list(bf.iloc[3])
        bottom_box = list(cf.iloc[3])
        target = [0.85,0.85,0.85,0.85]

        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [

            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),
            

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_nurse['annotations'] = annotations
    layout_nurse['title'] = "Communications With Nurses Rating"
    figure = dict(data=data, layout=layout_nurse)
    return figure

@app.callback(Output('allied_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_allied(contents,department,gender,age,education_level,race): 

    layout_allied= copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_allied['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)

        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[4])
        middle_box = list(bf.iloc[4])
        bottom_box = list(cf.iloc[4])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)
        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [

            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_allied['annotations'] =annotations
    layout_allied['title'] = 'Communications With Allied Health Staff Rating'
    figure = dict(data=data, layout=layout_allied)
    return figure


@app.callback(Output('environment_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_environment(contents,department,gender,age,education_level,race):  

    layout_environment = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_environment['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[6])
        middle_box = list(bf.iloc[6])
        bottom_box = list(cf.iloc[6])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_environment['annotations'] = annotations
    layout_environment['title'] = 'Environment Meals and Facilities Rating'
    figure = dict(data=data, layout=layout_environment)
    return figure


@app.callback(Output('medication_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_medications(contents,department,gender,age,education_level,race):  

    layout_medications = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_medications['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[5])
        middle_box = list(bf.iloc[5])
        bottom_box = list(cf.iloc[5])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_medications['annotations'] = annotations

    layout_medications['title'] = "Communications On Medications Rating"

    figure = dict(data=data, layout=layout_medications)
    return figure


@app.callback(Output('admission_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_admission(contents,department,gender,age,education_level,race):  

    layout_admission = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_admission['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[6])
        middle_box = list(bf.iloc[6])
        bottom_box = list(cf.iloc[6])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [
            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_admission['annotations'] =annotations

    layout_admission['title'] = "Admission Rating"

    figure = dict(data=data, layout=layout_admission)
    return figure


@app.callback(Output('care_graph', 'figure'),
              [Input('analytics', 'contents'),Input('department','value'),Input('gender','value'),Input('age','value'),
              Input('education_level','value'),Input('race','value')])   
def display_care(contents,department,gender,age,education_level,race):  

    layout_care = copy.deepcopy(layout)
    if contents is None:
        annotation = dict(
            text='No data available,Please upload data',
            x=0.5,
            y=0.5,
            align="center",
            showarrow=False,
            xref="paper",
            yref="paper"
        )
        layout_care['annotations'] = [annotation]
        data = []

    else:
        content_type, content_string = contents.split(',')
        try:
            df = pd.read_csv(io.StringIO(base64.b64decode(content_string).decode('utf-8')))
        except:
            df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
        df_department = df[department]
        af = df_department.loc['Top-box']
        bf = df_department.loc['Middle-box']
        cf = df_department.loc['Bottom-box']

        top_box = list(af.iloc[7])
        middle_box = list(bf.iloc[7])
        bottom_box = list(cf.iloc[7])
        target = [0.85,0.85,0.85,0.85]
        index_update = update_index(df_department)

        annotations = []
        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= top_box[i]+0.02,
                # xref="x",
                # yref="y",
                text= '%.2f%%' % (top_box[i] * 100),
                showarrow= False,
                # 40,ax= -0,
                # ay= -

                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= middle_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (middle_box[i] * 100),
                showarrow= False,
                ay = -100
                )
            annotations.append(annotation)

        for i, item in enumerate(index_update):
            annotation = dict(
                x= item,
                y= bottom_box[i]+0.02,
                xref='x',
                yref='y',
                text= '%.2f%%' % (bottom_box[i] * 100),
                showarrow= False
                )
            annotations.append(annotation)

        data = [

            dict(
                type='scatter',
                mode='lines+markers',
                name='target',
                x=index_update,
                y=target,
                line=dict(
                    dash = 'dot',
                    smoothing=2,
                    width=2,
                    color=('rgb(227, 23, 13)'),
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Top-box',
                x=index_update,
                y=top_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#F78A77'
                ),
                marker=dict(symbol='diamond-open')
            ),

            dict(
                type='scatter',
                mode='lines+markers',
                name='Middle-box',
                x=index_update,
                y=middle_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#4B9BD2'
                ),
                marker=dict(symbol='diamond-open')
            ),
            dict(
                type='scatter',
                mode='lines+markers',
                name='Bottom-box',
                x=index_update,
                y=bottom_box,
                line=dict(
                    shape="line",
                    smoothing=2,
                    width=2,
                    color='#E4E520'
                ),
                marker=dict(symbol='diamond-open')
            ),
        ]
        layout_care['annotations'] = annotations
    layout_care['title'] = "Patient/Family Empowerment and Care Transition Rating"

    figure = dict(data=data, layout=layout_care)
    return figure

@app.callback(Output('doctor1', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):
    layout_sample = copy.deepcopy(layout)
    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Doctor'])
    figure = dict(data=a, layout=layout_sample)
    return a

@app.callback(Output('doctor2', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Doctor'])
    return b

@app.callback(Output('doctor3', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Doctor'])
    return c


@app.callback(Output('nurse1', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Nurse'])
    return a

@app.callback(Output('nurse2', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Nurse'])
    return b

@app.callback(Output('nurse3', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Nurse'])
    return c

@app.callback(Output('allied1', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Allied Health-dietitian','Allied Health-pharmacist','Allied Health-PT/OT','Allied Health-X ray Staff'])
    return a

@app.callback(Output('allied2', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Allied Health-dietitian','Allied Health-pharmacist','Allied Health-PT/OT','Allied Health-X ray Staff'])
    return b

@app.callback(Output('allied3', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Allied Health-dietitian','Allied Health-pharmacist','Allied Health-PT/OT','Allied Health-X ray Staff'])
    return c

    
@app.callback(Output('environment1', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Environment','Meals','Facilities'])
    return a

@app.callback(Output('environment2', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Environment','Meals','Facilities'])
    return b

@app.callback(Output('environment3', 'children'),
              [Input('analytics', 'contents')]) 
def display_sample(contents):

    content_type, content_string = contents.split(',')
    df = pd.read_excel(io.BytesIO(base64.b64decode(content_string)),None)
    a,b,c = fetch_sample(df['verbatim'],['Environment','Meals','Facilities'])
    return c



app.scripts.config.serve_locally = True
app.css.append_css({'external_url': 'https://cdn.rawgit.com/plotly/dash-app-stylesheets/2d266c578d2a6e8850ebce48fdb52759b2aef506/stylesheet-oil-and-gas.css'})  # noqa: E501
#app.css.append_css({"external_url": "https://codepen.io/chriddyp/pen/bWLwgP.css"})


if __name__ == '__main__':
    app.run_server(debug=True)


