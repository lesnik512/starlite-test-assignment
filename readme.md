## Prepare virtual environment

```bash
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install pip-tools
make pip-sync
```

## Run server

```bash
make run
```

## API use-cases:
1) Show the number of impressions and clicks that occurred before the 1st of June 2017, broken down by channel and country, sorted by clicks in descending order. Hint:

URL: http://127.0.0.1:8000/api/metrics?to_date=2017-05-31&sort_direction=desc&sort_field=clicks&group_by=channel,country

2) Show the number of installs that occurred in May of 2017 on iOS, broken down by date, sorted by date in ascending order.

URL: http://127.0.0.1:8000/api/metrics?from_date=2017-05-01&to_date=2017-05-31&sort_direction=asc&sort_field=date&os=ios&group_by=date

3) Show revenue, earned on June 1, 2017 in US, broken down by operating system and sorted by revenue in descending order.

URL: http://127.0.0.1:8000/api/metrics?from_date=2017-06-01&to_date=2017-06-01&sort_direction=desc&sort_field=revenue&group_by=os

4) Show CPI and spend for Canada (CA) broken down by channel ordered by CPI in descending order. Please think carefully which is an appropriate aggregate function for CPI.

URL: http://127.0.0.1:8000/api/metrics?sort_direction=desc&sort_field=cpi&group_by=channel,country&country=CA
