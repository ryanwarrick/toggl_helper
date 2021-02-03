import requests
from datetime import timedelta, datetime

import configparser

config = configparser.ConfigParser()
config.read('toggl_helper_config.ini')

now = datetime.now()
today_date = now.strftime('%Y-%m-%d')

params = (
    ('workspace_id', config['DEFAULT']['workspace_id']),
    ('since', today_date),
    ('until', today_date),
    ('user_agent', config['DEFAULT']['user_agent']),
)

response = requests.get('https://api.track.toggl.com/reports/api/v2/summary', params=params, auth=(config['DEFAULT']['api_token'], 'api_token'))

data = response.json()

work_milliseconds = 0
personal_milliseconds = 0

for result in data['data']:
    if result['title']['client'] == config['PRIMARY']['client_name']:
        work_milliseconds += result['time']
    elif result['title']['client'] == 'Home':
        personal_milliseconds += result['time']

work_duration = timedelta(milliseconds=work_milliseconds)
personal_duration = timedelta(milliseconds=personal_milliseconds)
total_duration = timedelta(milliseconds=work_milliseconds + personal_milliseconds)

work_hour_goals = [7, 7.5, 8, 8.5]
work_end_times = []

for work_hour_goal in work_hour_goals:
    work_end_times.append(now + (timedelta(hours=work_hour_goal)-work_duration))
    
print("##################")
print("Toggl Quick Status")
print("------------------")
print(config['PRIMARY']['client_name']+ ": " + str(work_duration))
print("Home: " + str(personal_duration))
print(". . . . . . . . .")
for work_hour_goal, work_end_time in zip(work_hour_goals, work_end_times):
    print(str(work_hour_goal) + " hrs: " + str(work_end_time.strftime('%H:%M')))
print("##################")
