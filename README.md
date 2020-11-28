# fpl
A Fantasy Premier League (FPL) dashboard which allows users to plot several key performance metrics such as [xG, xA](https://www.optasports.com/services/analytics/advanced-metrics/), and [VAPM](https://www.reddit.com/r/FantasyPL/comments/6r60fu/exploring_a_key_metric_value_added_per_1m/) against each other which allows users to obtain key insights on the statistical indicators of top players in the Premier League (EPL).

[Try out the dashboard](https://kc-fpl-dashboard.herokuapp.com/)

*Warning: The css might be buggy due in large part to css being applied to [abstractions of HTML components](https://dash.plotly.com/dash-html-components), not the components themselves.  The Dash development team recommends the use of the [Dash Enterprise Design Kit](https://plotly.com/dash/design-kit/) for styling, but the FPL dashboard only uses open-source Dash due to budget constraints...*

## Dash

The FPL Dashboard is built on Dash, a data visualization tool for Python, which in turn is built on top of Flask, React.js, and Plotly.js under the hood.

- [Dash](https://dash.plotly.com/)
- [Flask](https://flask.palletsprojects.com/en/1.1.x/tutorial/)
- [React](https://reactjs.org/tutorial/tutorial.html)
- [Plotly](https://plotly.com/javascript/getting-started/)
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

## Deployment
- Deployed on [Heroku](https://devcenter.heroku.com/articles/getting-started-with-python) via this [Dash deployment tutorial](https://dash.plotly.com/deployment).
