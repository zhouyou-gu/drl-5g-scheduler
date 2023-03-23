#  DRL-5G-Scheduler; Author: Zhouyou Gu (zhouyou.gu@sydney.edu.au);
#  Supervisors: Wibowo Hardjawana; Branka Vucetic;
#  This project is developed at Centre for IoT and Telecommunications at The University of Sydney,
#  under a project directly funded by Telstra Corporation Ltd., titled
#  ”Development of an Open Programmable Scheduler for LTE Networks”, from 2018 to 2019.
#  Reference: Z. Gu, C. She, W. Hardjawana, S. Lumb, D. McKechnie, T. Essery, and B. Vucetic,
#   “Knowledge-assisted deep reinforcement learning in 5G scheduler design:
#  From theoretical framework to implementation,” IEEE JSAC., to appear, 2021

import time

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly
import plotly.graph_objs as go
from dash.dependencies import Output, Input

from edge_ctrl_script.exp_process import *
from exp_src.measurement_app.udp_report_sink import udp_report_sink

now = time.time()

U = udp_report_sink()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

colors = {
    'background': '#ffffff',
    'heading': '#ff4d00',
    'text': '#111111',
    'title': '#111111'
}

HEADING_FONT_SIZE  = "60pt"
SUBTITLE_FONT_SIZE  = "30pt"
TEXT_FONT_SIZE = "20pt"

Y_RANGE = 30

class DDRLWebInterface(dash.Dash):
    def __init__(self, name, external_stylesheets=external_stylesheets):
        super(DDRLWebInterface, self).__init__(name, external_stylesheets=external_stylesheets,
                                               assets_folder=os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                                                          'assets'))
        print(self.config)
        self.layout = \
            html.Div(
                style={'backgroundColor': colors['background'], 'width': '100%', 'height': '100%', 'max-width': 'none'},
                className="container", children=[
                    html.Div(style={'backgroundColor': colors['background'], 'width': '95%', 'height': '100%',
                                    'max-width': 'none'}, className="container", children=[
                        html.H1(
                            children='Real-Time Deep Reinforcement Learning',
                            style={
                                'textAlign': 'center',
                                'color': colors['heading'],
                                'font-size': HEADING_FONT_SIZE,
                            }
                        ),
                        html.H1(
                            children='for Per-Millisecond Scheduling in 5G',
                            style={
                                'textAlign': 'center',
                                'color': colors['heading'],
                                'font-size': HEADING_FONT_SIZE,
                            }
                        ),
                        # html.H2(
                        #     children='Presented by Zhouyou Gu',
                        #     style={
                        #         'textAlign': 'center',
                        #         'color': colors['title'],
                        #         'font-size': SUBTITLE_FONT_SIZE,
                        #     }
                        # ),
                        # html.H1(
                        #     children='Paper: Knowledge-assisted Deep Reinforcement Learning in 5G Scheduler Design: From Theoretical Framework to Implementation',
                        #     style={
                        #         'textAlign': 'center',
                        #         'color': colors['title'],
                        #         'font-size': SUBTITLE_FONT_SIZE,
                        #     }
                        # ),
                        html.H2(
                            children='Centre for IoT and Telecommunications, EIE, USYD',
                            style={
                                'textAlign': 'center',
                                'color': colors['title'],
                                'font-size': SUBTITLE_FONT_SIZE,
                            }
                        ),
                        html.H2(
                            children='In Collaboration with Telstra Corporation Ltd.',
                            style={
                                'textAlign': 'center',
                                'color': colors['title'],
                                'font-size': SUBTITLE_FONT_SIZE,
                            }
                        ),
                        html.Button('Experiment Setup', id='b_exp_setup', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        html.Div(style={'backgroundColor': colors['background'], 'width': '100%', 'height': '100%',
                                        'max-width': 'none'}, className="container", children=html.Img(style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['text'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '100%',
                        }, src=self.get_asset_url('ddrl.png'))),
                        html.Button('Start Sync', id='b_start_sync', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Textarea(
                            id='text_sync',
                            rows=25,
                            disabled=True,
                            readOnly=True,
                            placeholder='Time Sync Information',
                            value='Time Sync Information',
                            contentEditable=False,
                            style={'width': '100%',
                                   'height': '500px',
                                   'backgroundColor': colors['background'],
                                   'font-size': TEXT_FONT_SIZE,
                                   'color': colors['text'],
                                   },
                        ),
                        html.Button('Start Controller', id='b_start_controller', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Textarea(
                            id='text_controller',
                            rows=25,
                            disabled=True,
                            readOnly=True,
                            placeholder='Controller Information',
                            value='Controller Information',
                            contentEditable=False,
                            style={'width': '100%',
                                   'height': '500px',
                                   'backgroundColor': colors['background'],
                                   'font-size': TEXT_FONT_SIZE,
                                   'color': colors['text'],
                                   },
                        ),
                        html.Button('Start Cellular Network', id='b_start_edge', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Textarea(
                            id='text_edge',
                            rows=25,
                            disabled=True,
                            readOnly=True,
                            placeholder='Edge Information',
                            value='Edge Information',
                            contentEditable=False,
                            style={'width': '100%',
                                   'height': '500px',
                                   'backgroundColor': colors['background'],
                                   'font-size': TEXT_FONT_SIZE,
                                   'color': colors['text'],
                                   },
                        ),
                        html.Button('Start Ping', id='b_start_ping', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Textarea(
                            id='text_ping',
                            rows=25,
                            disabled=True,
                            readOnly=True,
                            placeholder='Pinging information',
                            value='Pinging information',
                            contentEditable=False,
                            style={'width': '100%',
                                   'height': '500px',
                                   'backgroundColor': colors['background'],
                                   'font-size': TEXT_FONT_SIZE,
                                   'color': colors['text'],
                                   },
                        ),
                        html.Button('Start Test', id='b_start_test', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Textarea(
                            id='text_test',
                            rows=25,
                            disabled=True,
                            readOnly=True,
                            placeholder='Test information',
                            value='Test information',
                            contentEditable=False,
                            style={'width': '100%',
                                   'height': '500px',
                                   'backgroundColor': colors['background'],
                                   'font-size': TEXT_FONT_SIZE,
                                   'color': colors['text'],
                                   },
                        ),
                        html.Button('Real-time Latency', id='b_measure', style={
                            'textAlign': 'center',
                            'font-size': SUBTITLE_FONT_SIZE,
                            'color': colors['title'],
                            'display': 'inline-block',
                            'width': '100%',
                            'height': '150px',
                        }),
                        dcc.Graph(id='live-graph-0', animate=False),
                        dcc.Graph(id='live-graph-1', animate=False),
                        dcc.Interval(
                            id='graph-update-10',
                            interval=1 * 10
                        ),
                        dcc.Interval(
                            id='graph-update-100',
                            interval=1 * 100
                        ),
                        dcc.Interval(
                            id='graph-update-500',
                            interval=1 * 500
                        ),
                        dcc.Interval(
                            id='graph-update-1000',
                            interval=1 * 1000
                        ),
                    ]), ])


app = DDRLWebInterface('Test', external_stylesheets)


@app.callback(Output('live-graph-0', 'figure'),
              [Input('graph-update-500', 'n_intervals')])
def update_graph_scatter(input_data):
    r = U.get_report()
    x = []
    y = []
    if len(r)>0:
        for u in r[0]:
            x.append(u[0] - now)
            y.append(float(u[1]) / 1e6)

    data = plotly.graph_objs.Scatter(
        x=x,
        y=y,
        name='Scatter',
        mode='lines+markers'
    )
    x_min = 0
    if len(x) > 0:
        x_min = x[0]

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[x_min, time.time() - now]),
                                                yaxis=dict(range=[0, Y_RANGE]),
                                                plot_bgcolor=colors['background'],
                                                paper_bgcolor=colors['background'],
                                                font={'color': colors['text'],
                                                      'size': 30
                                                      },
                                                xaxis_title="Test time (s)",
                                                yaxis_title="User 1 Latency (ms)",
                                                margin=dict(l=100)
                                                )}


@app.callback(Output('live-graph-1', 'figure'),
              [Input('graph-update-500', 'n_intervals')])
def update_graph_scatter(input_data):
    r = U.get_report()
    x = []
    y = []
    if len(r)>1:
        for u in r[1]:
            x.append(u[0] - now)
            y.append(float(u[1]) / 1e6)

    data = plotly.graph_objs.Scatter(
        x=x,
        y=y,
        name='Scatter',
        mode='lines+markers'
    )
    x_min = 0
    if len(x) > 0:
        x_min = x[0]

    return {'data': [data], 'layout': go.Layout(xaxis=dict(range=[x_min, time.time() - now]),
                                                yaxis=dict(range=[0, Y_RANGE]),
                                                plot_bgcolor=colors['background'],
                                                paper_bgcolor=colors['background'],
                                                font={'color': colors['text'],
                                                      'size': 30
                                                      },
                                                xaxis_title="Test time (s)",
                                                yaxis_title="User 2 Latency (ms)",
                                                margin=dict(l=100)
                                                )}


@app.callback(Output('b_start_sync', 'children'),
              [Input('b_start_sync', 'n_clicks')])
def update_text(input_data):
    print(input_data)
    if input_data and input_data > 0:
        run_sync.toggle_run()

    if run_sync.started:
        return 'Time Sync Started'
    else:
        return 'Time Sync Stopped'


@app.callback(Output('text_sync', 'value'),
              [Input('graph-update-500', 'n_intervals')])
def update_text(input_data):
    return run_sync.readlines()


@app.callback(Output('b_start_controller', 'children'),
              [Input('b_start_controller', 'n_clicks')])
def update_text(input_data):
    print(input_data)
    if input_data and input_data > 0:
        run_controller.toggle_run()

    if run_controller.started:
        return 'Controller Started'
    else:
        return 'Controller Stopped'


@app.callback(Output('text_controller', 'value'),
              [Input('graph-update-500', 'n_intervals')])
def update_text(input_data):
    return run_controller.readlines()


@app.callback(Output('b_start_edge', 'children'),
              [Input('b_start_edge', 'n_clicks')])
def update_text(input_data):
    print(input_data)
    if input_data and input_data > 0:
        edge_run.toggle_run()
    if edge_run.started:
        return 'Cellular Network Started'
    else:
        return 'Cellular Network Stopped'


@app.callback(Output('text_edge', 'value'),
              [Input('graph-update-100', 'n_intervals')])
def update_text(input_data):
    return edge_run.readlines()


@app.callback(Output('b_start_ping', 'children'),
              [Input('b_start_ping', 'n_clicks')])
def update_text(input_data):
    print(input_data)
    if input_data and input_data > 0:
        edge_ping.toggle_run()
    if edge_ping.started:
        return 'Ping Started'
    else:
        return 'Ping Stopped'


@app.callback(Output('text_ping', 'value'),
              [Input('graph-update-500', 'n_intervals')])
def update_text(input_data):
    return edge_ping.readlines()


@app.callback(Output('b_start_test', 'children'),
              [Input('b_start_test', 'n_clicks')])
def update_text(input_data):
    print(input_data)
    if input_data and input_data > 0:
        edge_one_way_latency_lte.toggle_run()

    if input_data and input_data > 0 and edge_one_way_latency_lte.started:
        global now
        now = time.time()

    if edge_one_way_latency_lte.started:
        return 'Latency Test Started'
    else:
        return 'Latency Test Stopped'


@app.callback(Output('text_test', 'value'),
              [Input('graph-update-500', 'n_intervals')])
def update_text(input_data):
    return edge_one_way_latency_lte.readlines()


if __name__ == '__main__':
    U.start()
    app.run_server(port=8080, host='0.0.0.0')
