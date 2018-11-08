# https://extremely-alpha.iodide.io/notebooks/31/

import requests
from datetime import datetime, timedelta
import pandas as pd; from pandas import DataFrame, Series

meta_bug_id = 1386669
url = """https://bugzilla.mozilla.org/rest/bug?blocks={bug_id}&include_fields=id,priority,last_change_time,status,creation_time""".format(bug_id=meta_bug_id)

response = requests.get(url)
bugs = response.json()['bugs']

def extract_counts(priority, start_date='2018-01-01'):
  start = datetime.strptime(start_date, "%Y-%m-%d")
  end = datetime.today()
  day = timedelta(days=1)

  open_counts = []

  bugs_by_priority = [b for b in bugs if b['priority']==priority]

  curr_date = start

  while curr_date < end:
    open_bugs = [b for b in bugs_by_priority if datetime.strptime(b["creation_time"][0:10], "%Y-%m-%d")<=curr_date and not (b["status"] in ('RESOLVED', 'VERIFIED') and datetime.strptime(b['last_change_time'][0:10], "%Y-%m-%d")<=curr_date )]
    open_counts.append((curr_date, len(open_bugs)))
    curr_date += day

  return open_counts


def plot_burndown_matplotlib(priority, start_date='2018-01-01'):
  # usage: display(plot_burndown_matplotlib('P1'))
  open_counts = extract_counts(priority, start_date)

  open_counts_df = pd.DataFrame(open_counts,columns=['Day',priority])
  fig = open_counts_df.plot(
    kind='line',
    x='Day',
    title='{priority} open bugs'.format(priority=priority),
    legend=False
  )
  ylim = fig.get_ylim()
  fig.set_ylim([0, ylim[1]])

  return fig.figure.tight_layout()
