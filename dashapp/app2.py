import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from sqlalchemy_utils import database_exists, create_database
from datetime import datetime as dt
import pandas as pd
import psycopg2
import json

'''
Dash website that queries Timescale.
'''

# Custom CSS styles are stored in assets/heroic-assets.css
app = dash.Dash(__name__, static_folder='assets')
app.scripts.config.serve_locally=True
app.css.config.serve_locally=True
app.config.suppress_callback_exceptions = True

# Settings for psycopg Timescale connector
user = 'postgres'
host = '0.0.0.0'
dbname = 'pages'
con = None
con = psycopg2.connect(database = dbname, user = user, password='password', host='localhost')


app.layout = html.Div([
    html.Div(dcc.Location(id='url', refresh=False)),
    html.Div([
	dcc.Link('Home', className = 'header-button', href = '/'),
        html.A('About', href = 'https://github.com/thecolorkeo/InsightWiki', target = '_blank', className = 'header-button'),
        dcc.Link('Contact', className = 'header-button', href = '/contact'),
        html.A('Resume', href = 'https://rawcdn.githack.com/thecolorkeo/Resume/ab63fb2f799f3b78fac5c71f5f47360b1dfca3c3/Keo_Chan_Final.pdf', \
	    target = '_blank', className = 'header-button'),
        dcc.Link('EditWindow', className = 'header-button', href = '/', style = {'float': 'right', 'class': 'active'})
    ], className = 'app-header'),
    html.Div(id='page-content'),
])


# Query for index page figure
sql_query_0 = "SELECT CAST(time AS DATE), count(*) as frequency FROM revs " \
    + "WHERE time BETWEEN '2018-10-01' AND '2018-12-31' GROUP BY CAST(time AS DATE)"
query_results_0 = pd.read_sql_query(sql_query_0, con)
revs_0 = []
for i in range(0,query_results_0.shape[0]):
    revs_0.append(dict(time=query_results_0.iloc[i]['time'], frequency=query_results_0.iloc[i]['frequency']))

index_page = html.Div([
    html.Div('Edit Window by Keo Chan', className = 'page-title', style = {'text-align': 'center'}),
    html.Div([
        dcc.Link(html.Button('MOST EDITS IN 2018: InternetArchiveBot', className = 'button1'), href = '/page-1'),
        dcc.Link(html.Button('MOST EDITS IN 2018 (non-bot): Ser Amantio di Nicolao', className = 'button1'), href = '/page-2'),
        dcc.Link(html.Button('EDIT FREQUENCY BY USER', className = 'button1'), href = '/page-3'),
        dcc.Link(html.Button('EDIT LENGTH BY USER', className = 'button1'), href = '/page-4'),
    ], style = {'text-align': 'center'}),
    html.Br(),
    html.Div([
        dcc.Graph(
	    id='example0',
            figure={
                'data': [{'x': query_results_0['time'], 'y': query_results_0['frequency'], 'type': 'line', 'name': 'Users'}],
                'layout': {
                    'title': 'Most recent 3 months of sitewide edits',
		    'titlefont': {'size': 60},
		    'yaxis': {'tickfont': {'size': 30}},
                    'xaxis': {
                       'type': 'date',
                       'tickformat': '%Y-%m-%d',
                       'tickmode': 'linear',
		       'automargin': True,
                       'dtick': 86400000.0 * 7, #one day * n
		       'tickfont': dict(size=30),
              	    },
                }
            }, className = 'graph',
        )
    ]),
])


page_1_layout = html.Div([
    html.Div('Most Edits in 2018', className='page-title'),
    html.Div(id='page-1-content'), html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range-1',
        min_date_allowed=dt(2001, 1, 15),
        max_date_allowed=dt.today(),
	start_date=dt(2018, 1, 1),
        end_date=dt(2018, 12, 31),
	day_size=60,
    ),
    html.Div('Click on one of the bars to see more statistics', style = {'font-size': '3vh'}), html.Br(),
    html.Div(id='output-container-date-picker-range-1'), html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range-1.1',
        min_date_allowed=dt(2001, 1, 15),
        max_date_allowed=dt.today(),
        start_date=dt(2001, 1, 1),
        end_date=dt(2018, 12, 31),
        day_size=60,
    ),
    html.Div(id='click_output'), html.Br(),
])
# Callback for first date picker
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range-1', 'children'),
    [dash.dependencies.Input('my-date-picker-range-1', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-1', 'end_date')])
def page_1_output(start_date, end_date):
    sql_query = "SELECT username, count(*) as frequency FROM revs WHERE lower(username) IS NOT NULL AND time BETWEEN "
    if start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query = sql_query + start_date_string + " AND " + end_date_string \
	    + " GROUP BY username ORDER BY count(*) DESC LIMIT 10;"
    query_results = pd.read_sql_query(sql_query,con)
    revs = []
    for i in range(0,query_results.shape[0]):
        revs.append(dict(username=query_results.iloc[i]['username'], frequency=query_results.iloc[i]['frequency']))
    if len(sql_query) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
	           id='example1',
	           figure={
	               'data': [{'x': query_results['username'], 'y': query_results['frequency'], \
			   'type': 'bar', 'name': 'Users'}],
	               'layout': {'title': 'Number of edits per user',
                           'titlefont': {'size': 60},
                           'yaxis': {'tickfont': {'size': 30}},
                           'xaxis': {'tickfont': {'size': 30}, 'automargin': True},
		       }

	           }, className = 'graph',
	)
# Callback for click event on graph 1
@app.callback(
    dash.dependencies.Output('click_output', 'children'),
    [dash.dependencies.Input('example1', 'clickData'),
     dash.dependencies.Input('my-date-picker-range-1.1', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-1.1', 'end_date')])
def clicked_1(clickData, start_date, end_date):
    value = clickData['points'][0]['x']
    sql_query = "SELECT CAST(time AS DATE), count(*) as frequency FROM revs WHERE lower(username) = lower('"
    if value is not None and start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query = sql_query + str(value) + "') AND time BETWEEN " + start_date_string + " AND " + end_date_string \
            + " GROUP BY CAST(time as DATE);"
    query_results=pd.read_sql_query(sql_query,con)
    revs = []
    for i in range(0,query_results.shape[0]):
        revs.append(dict(time=query_results.iloc[i]['time'], frequency=query_results.iloc[i]['frequency']))
    if len(sql_query) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
                    id='example1.1',
                    figure={
                        'data': [{'x': query_results['time'], 'y': query_results['frequency'], \
                            'type': 'line', 'name': 'Users'}],
                        'layout': {
                            'title': 'Frequency of edits by ' + str(value) + ' by date',
                            'titlefont': {'size': 60},
                            'yaxis': {'tickfont': {'size': 30}},
                            'xaxis': {
                               'type': 'date',
                               'tickformat': '%Y-%m-%d',
                               'tickmode': 'linear',
                               'tickfont': {'size': 30},
                               'automargin': True,
                               'dtick': 86400000.0*59 #one day * x
                            }
                        }
                    }, className = 'graph',
                )


page_2_layout = html.Div([
    html.Div('Most Edits in 2018 (without bots)', className='page-title'),
    html.Div(id='page-2-content'), html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range-2',
        min_date_allowed=dt(2001, 1, 15),
        max_date_allowed=dt.today(),
        start_date=dt(2018, 1, 1),
        end_date=dt(2018, 12, 31),
        day_size=60,
    ),
    html.Div('Click on one of the bars to see more statistics', style = {'font-size': '3vh'}), html.Br(),
    html.Div(id='output-container-date-picker-range-2'), html.Br(),
    html.Div('Adjust the time window with the date picker at the top of the page', style = {'font-size': '2vh'}), html.Br(),
    html.Div(id='click_output_2'),
])
# Callback for initial page load from date picker
@app.callback(
    dash.dependencies.Output('output-container-date-picker-range-2', 'children'),
    [dash.dependencies.Input('my-date-picker-range-2', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-2', 'end_date')])
def page_2_output(start_date, end_date):
    sql_query_2 = "SELECT username, count(*) as frequency FROM revs WHERE lower(username) NOT LIKE '%bot%' AND time BETWEEN "
    if start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query_2 = sql_query_2 + start_date_string + " AND " + end_date_string \
	    + " GROUP BY username ORDER BY count(*) DESC LIMIT 10;"
    query_results_2=pd.read_sql_query(sql_query_2,con)
    revs_2 = []
    for i in range(0,query_results_2.shape[0]):
        revs_2.append(dict(username=query_results_2.iloc[i]['username'], frequency=query_results_2.iloc[i]['frequency']))
    if len(sql_query_2) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
                id='example-2',
                figure={
                    'data': [{'x': query_results_2['username'], 'y': query_results_2['frequency'], \
			'type': 'bar', 'name': 'Users'}],
                    'layout': {'title': 'Number of edits per user',
                        'titlefont': {'size': 60},
                        'yaxis': {'tickfont': {'size': 30}},
                        'xaxis': {'tickfont': {'size': 30}, 'automargin': True},
                    }
                }, className = 'graph',
        )
# Callback for click event on graph 2
@app.callback(
    dash.dependencies.Output('click_output_2', 'children'),
    [dash.dependencies.Input('example-2', 'clickData'),
     dash.dependencies.Input('my-date-picker-range-2', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-2', 'end_date')])
def clicked_2(clickData, start_date, end_date):
    value = clickData['points'][0]['x']
    sql_query = "SELECT CAST(time AS DATE), count(*) as frequency FROM revs WHERE lower(username) = lower('"
    if value is not None and start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query = sql_query + str(value) + "') AND time BETWEEN " + start_date_string + " AND " + end_date_string \
            + " GROUP BY CAST(time as DATE);"
    query_results=pd.read_sql_query(sql_query,con)
    revs = []
    for i in range(0,query_results.shape[0]):
        revs.append(dict(time=query_results.iloc[i]['time'], frequency=query_results.iloc[i]['frequency']))
    if len(sql_query) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
                    id='example-2.1',
                    figure={
                        'data': [{'x': query_results['time'], 'y': query_results['frequency'], \
                            'type': 'line', 'name': 'Users'}],
                        'layout': {
                            'title': 'Frequency of edits by ' + str(value) + ' by date',
                            'titlefont': {'size': 60},
                            'yaxis': {'tickfont': {'size': 30}},
                            'xaxis': {
                               'type': 'date',
                               'tickformat': '%Y-%m-%d',
                               'tickmode': 'linear',
                               'tickfont': {'size': 30},
                               'automargin': True,
                               'dtick': 86400000.0*59 #one day * x
                            }
                        }
                    }, className = 'graph',
                )


page_3_layout = html.Div([
    html.Div('Frequency of edits by user', className='page-title'),
    html.Div(id='page-3-content'), html.Br(),
    dcc.Input(id='name-picker-3', type='text', value='Ser Amantio Di Nicolao', style = {'font-size': '4vh'}), html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range-3',
        min_date_allowed=dt(2001, 1, 15),
        max_date_allowed=dt.today(),
        start_date=dt(2018, 10, 1),
        end_date=dt(2018, 12, 31),
        day_size=60,
    ),
    html.Div(id='output-container-3'), html.Br(),
])
@app.callback(
    dash.dependencies.Output('output-container-3', 'children'),
    [dash.dependencies.Input('name-picker-3', 'value'),
     dash.dependencies.Input('my-date-picker-range-3', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-3', 'end_date')])
def page_3_output(value, start_date, end_date):
    sql_query_3 = "SELECT CAST(time AS DATE), count(*) as frequency FROM revs WHERE lower(username) = lower('"
    if value is not None and start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query_3 = sql_query_3 + str(value) + "') AND time BETWEEN " + start_date_string + " AND " + end_date_string \
	    + " GROUP BY CAST(time as DATE);"
    query_results_3=pd.read_sql_query(sql_query_3,con)
    revs_3 = []
    for i in range(0,query_results_3.shape[0]):
        revs_3.append(dict(time=query_results_3.iloc[i]['time'], frequency=query_results_3.iloc[i]['frequency']))
    if len(sql_query_3) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
	            id='example3',
	    	    figure={
	                'data': [{'x': query_results_3['time'], 'y': query_results_3['frequency'], \
			    'type': 'line', 'name': 'Users'}],
	                'layout': {
	                    'title': 'Frequency of edits by ' + str(value) + ' by date',
                            'titlefont': {'size': 60},
                            'yaxis': {'tickfont': {'size': 30}},
                            'xaxis': {
	                       'type': 'date',
	                       'tickformat': '%Y-%m-%d',
	                       'tickmode': 'linear',
			       'tickfont': {'size': 30},
			       'automargin': True,
	                       'dtick': 86400000.0*7 #one day * x
	                    }
			}
	            }, className = 'graph',
	        )


page_4_layout = html.Div([
    html.Div('Length of pages edited by user', className='page-title'),
    html.Div(id='page-4-content'), html.Br(),
    dcc.Input(id='name-picker-4', type='text',value='Ser Amantio Di Nicolao', style = {'font-size': '4vh'}), html.Br(),
    dcc.DatePickerRange(
        id='my-date-picker-range-4',
        min_date_allowed=dt(2001, 1, 15),
        max_date_allowed=dt.today(),
        start_date=dt(2018, 10, 1),
        end_date=dt(2018, 12, 31),
        day_size=60,
    ),
    html.Div(id='output-container-4'), html.Br(),
])
@app.callback(
    dash.dependencies.Output('output-container-4', 'children'),
    [dash.dependencies.Input('name-picker-4', 'value'),
     dash.dependencies.Input('my-date-picker-range-4', 'start_date'),
     dash.dependencies.Input('my-date-picker-range-4', 'end_date')])
def page_4_output(value, start_date, end_date):
    sql_query_4 = "SELECT LENGTH(text) as length, count(*) as frequency FROM revs WHERE lower(username) = lower('"
    if value is not None and start_date is not None and end_date is not None:
        start_date = dt.strptime(start_date, '%Y-%m-%d')
        start_date_string = start_date.strftime("'%Y-%m-%d'")
        end_date = dt.strptime(end_date, '%Y-%m-%d')
        end_date_string = end_date.strftime("'%Y-%m-%d'")
        sql_query_4 = sql_query_4 + str(value) + "') AND time BETWEEN " + start_date_string + " AND " + end_date_string \
	    + " GROUP BY LENGTH(text);"
    query_results_4=pd.read_sql_query(sql_query_4,con)
    revs_4 = []
    for i in range(0,query_results_4.shape[0]):
        revs_4.append(dict(username=query_results_4.iloc[i]['length'], frequency=query_results_4.iloc[i]['frequency']))
    if len(sql_query_4) == 0:
        return 'Select a date to see it displayed here'
    else:
        return dcc.Graph(
                    id='example4',
                    figure={
                        'data': [{'x': query_results_4['length'], 'y': query_results_4['frequency'], \
			    'type': 'bar', 'name': 'Users'}],
                        'layout': {
                            'title': 'Length of edits by ' + str(value),
			    'titlefont': {'size': 60},
                            'xaxis': {'title': 'Number of characters in article',
				      'titlefont': {'size': 30},
				      'tickfont': {'size': 30}},
			    'yaxis': {'title': 'Number of edits',
				      'titlefont': {'size': 30},
				      'tickfont': {'size': 30}},
                        }
                    }, className = 'graph',
                )

contact_layout = html.Div([
    html.Div('Keo Chan | Data Engineer', className='page-title'), html.Br(),
    html.Div("Like my page? I'm looking for a job. Contact me at:", className='page-text'), html.Br(),
    html.Div('keozchan@gmail.com', className='page-text'), html.Br(),
    html.Div(html.A('linkedin.com/in/keozchan', href = 'https://linkedin.com/in/keozchan', target = '_blank'), \
	     className='page-text',
             style = {'font-size': '2vh'}), html.Br(),
    html.Div(html.A('Or take a look at my github.', href = 'https://github.com/thecolorkeo/InsightWiki', target = '_blank'), \
	     className='page-text'),
             html.Br(),
])


# Pagenav callback
@app.callback(dash.dependencies.Output('page-content', 'children'),
              [dash.dependencies.Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/page-1':
        return page_1_layout
    elif pathname == '/page-2':
        return page_2_layout
    elif pathname == '/page-3':
        return page_3_layout
    elif pathname == '/page-4':
        return page_4_layout
    elif pathname == '/contact':
	return contact_layout
    else:
        return index_page



# Run with `sudo python app2.py` for port 80
if __name__ == '__main__':
    app.run_server(debug=True, host='0.0.0.0', port=80)
