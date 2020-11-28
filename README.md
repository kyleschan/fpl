# fpl
A Fantasy Premier League (FPL) dashboard which allows users to plot several key performance metrics against each other which allows users to obtain key insights on the statistical indicators of top players in the Premier League (EPL).

[Try out the dashboard](https://kc-fpl-dashboard.herokuapp.com/) *Warning: The css is buggy due in large part to the large number of internal dependencies, but it functions properly on alternating selections of filters...*

## Dash

The FPL Dashboard is built on Dash, a data visualization tool for Python, which in turn is built on top of Flask under the hood.

- [Dash](https://dash.plotly.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/)

## Python Web Scraper

The FPL Dashboard data was obtained using Python.  The only 3rd party packages necessary are aiohttp and understat.
All project data is in the `data` folder of the repo.

- [aiohttp](https://github.com/aio-libs/aiohttp)
- [understat](https://github.com/amosbastian/understat)
- The understat Python package scrapes data from [Understat](https://understat.com/).
## Development
- Clone repository `git clone https://github.com/kyleschan/fpl.git`
- Switch to project root directory `cd fpl`
- Install requirements `pip install -r requirements.txt`
- Run app on http://127.0.0.1:8050/ `python app.py`
