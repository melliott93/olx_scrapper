import re
import time
from datetime import datetime
from datetime import date

last_added_time = datetime.now()
today = date.today()
link = 'dzisiaj o 12:37'
match = re.match(r'''dzisiaj''',link)
if match:
    time_str = re.findall(r'\d+:\d+',link)
    time_added = datetime.strptime(str(time_str), "['%H:%M']").time()
    final_time = datetime.combine(date.today(), time_added)
    if last_added_time < final_time:
        print('Send message')
    else:
        print('Skip')

