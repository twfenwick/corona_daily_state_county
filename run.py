import argparse
import os

import chart_studio
import chart_studio.plotly as py
import plotly.graph_objects as go
import matplotlib.pyplot as plt
import plotly.express as px
import pandas

path_counties = '/Users/tim/code/github/nytimes/covid-19-data/us-counties.csv'
path_states = '/Users/tim/code/github/nytimes/covid-19-data/us-states.csv'

cmdln_override = True
config_d = True
config_od = False
config_logy = False

"""
When I enter county and state
Then I see a trend chart of the county infection rate

When I enter a state
Then I see a trend chart of the state infection rate 
"""


def pandafunc(state='North Carolina', county=None, deaths=False, only_deaths=False, logy=False):
    match = [state, county]
    path = path_counties if county else path_states
    df = pandas.read_csv(path)

    df = df[df['state'].isin(match)]
    if county:
        df = df[df['county'].isin(match)]
        title = f'{county} County, {state}'
    else:
        title = state

    if cmdln_override:
        only_deaths = config_od
        deaths = config_d
        logy = config_logy

    if deaths:
        count = ['cases', 'deaths']
    elif only_deaths:
        count = 'deaths'
    else:
        count = 'cases'

    new_cases = df['cases'].diff()
    new_deaths = df['deaths'].diff()

    plot_data_browser(df, title, new_cases, new_deaths)

    # basic_browser_plot(count, df, logy, title)

    # basic_local_plot(count, df, logy, title)


def plot_data_browser(df, title, new_cases, new_deaths):
    # Browser group plots:
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['cases'],
        name='Total Cases',
        marker_color='sandybrown'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=new_cases,
        name='New Cases',
        marker_color='indianred'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=df['deaths'],
        name='Deaths',
        marker_color='black'
    ))
    fig.add_trace(go.Bar(
        x=df['date'],
        y=new_deaths,
        name='New Deaths',
        marker_color='gray'
    ))
    # Here we modify the tickangle of the xaxis, resulting in rotated labels.
    fig.update_layout(title=title, barmode='overlay', xaxis_tickangle=-45)
    # fig.show()



    import plotly.io as pio
    pio.write_html(fig, file='index.html', auto_open=True)

    import chart_studio.tools as tls
    tls.get_embed('file:///Users/tim/code/bitbucket/twfenwick/corona_tracker/index.html')


def basic_local_plot(count, df, logy, title):
    # Local plots:
    df.plot(logy=logy, kind='bar', x='date', y=count, grid=True, title=title)
    plt.show()
    plt.close()


def basic_browser_plot(count, df, logy, title):
    # Browser plots:
    fig = px.bar(df, x='date', y=count, title=title, log_y=logy, barmode='overlaid')
    fig.show()


def main():
    args = parse_args()
    pull_latest_corona_data()
    pandafunc(args['state'], args['county'], args['deaths'], args['only_deaths'], args['log'])


def parse_args():
    parser = argparse.ArgumentParser(description='Show trend of infection rate per state or county.')
    parser.add_argument('-s', '--state', help='Required for any query.', required=True)
    parser.add_argument('-c', '--county', help='Optional for specific county per state.')
    parser.add_argument('-d', '--deaths', help='Add number of deaths to the bar plot.', action='store_true')
    parser.add_argument('-o', '--only-deaths', help='Show only number of deaths in the bar plot.', action='store_true')
    parser.add_argument('-l', '--log', help='Plot in logarithmic scale.', action='store_true')
    args = vars(parser.parse_args())
    return args


def pull_latest_corona_data():
    os.system('cd /Users/tim/code/github/nytimes/covid-19-data; pwd; git pull origin master')


if __name__ == '__main__':
    main()
