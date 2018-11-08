# https://extremely-alpha.iodide.io/notebooks/31/
from datetime import datetime, timedelta

import pandas as pd
import requests

meta_bug_id = 1386669
url = (
    "https://bugzilla.mozilla.org/rest/bug?"
    "blocks={bug_id}&include_fields=id,priority,last_change_time,status,creation_time"
    .format(bug_id=meta_bug_id)
)

response = requests.get(url)
bugs = response.json()["bugs"]


def extract_counts(priority, start_date="2018-01-01"):
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.today()
    day = timedelta(days=1)

    open_counts = []

    bugs_by_priority = [b for b in bugs if b["priority"] == priority]

    curr_date = start

    while curr_date < end:
        open_bugs = [
            b
            for b in bugs_by_priority
            if datetime.strptime(b["creation_time"][0:10], "%Y-%m-%d") <= curr_date
            and not (
                b["status"] in ("RESOLVED", "VERIFIED")
                and datetime.strptime(b["last_change_time"][0:10], "%Y-%m-%d")
                <= curr_date
            )
        ]
        open_counts.append((curr_date, len(open_bugs)))
        curr_date += day

    return pd.DataFrame(open_counts, columns=["Day", "Count"]).assign(Priority=priority)


pd.concat(extract_counts(i) for i in ("P1", "P2", "P3")).to_csv("bugzilla.csv", index=False)
