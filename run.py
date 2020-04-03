import argparse

import matplotlib.pyplot as plt
import pandas

path_counties = '/Users/tim/code/github/nytimes/covid-19-data/us-counties.csv'
path_states = '/Users/tim/code/github/nytimes/covid-19-data/us-states.csv'

cmdln_override = False
config_d = False
config_od = False
config_logy = True

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

    df.plot(logy=logy, kind='bar', x='date', y=count, grid=True, title=title)
    plt.show()
    plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Show trend of infection rate per state or county.')
    parser.add_argument('-s', '--state', help='Required for any query.', required=True)
    parser.add_argument('-c', '--county', help='Optional for specific county per state.')
    parser.add_argument('-d', '--deaths', help='Add number of deaths to the bar plot.', action='store_true')
    parser.add_argument('-o', '--only-deaths', help='Show only number of deaths in the bar plot.', action='store_true')
    parser.add_argument('-l', '--log', help='Plot in logarithmic scale.', action='store_true')
    args = vars(parser.parse_args())

    pandafunc(args['state'], args['county'], args['deaths'], args['only_deaths'], args['log'])
