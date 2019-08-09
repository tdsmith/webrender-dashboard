# webrender-dashboard

## What is this?

This is the repository that makes the plots that you can see at
https://metrics.mozilla.com/webrender.

## What are thooooooooooose?

Those plots compare performance metrics collected from Firefox users
using either WebRender or the default Gecko rendering engine.
Statistics are displayed build-by-build for nightly and beta channels
so that WebRender developers can understand whether the changes they're landing
are having positive or negative effects on performance.

## How are they generated?

Databricks "scheduled jobs" kick off daily.

A separate job runs for each of the graphics cards manufacturers.

Some time later, a cron job running on hala collects the results and renders these dashboards
using RMarkdown.

The cron job runs `render.sh` in this repository.

## How does the Databricks notebook work?

The [Databricks notebook][notebook] reads raw pings from telemetry-cohorts.
This is both useful, because not all of the values we care about have always been in `main_summary`,
and performant, since the number of users in the experiments is relatively small.

Crash pings are read out of `telemetry-cohorts` for the same reason.

Enrollments are read from the events dataset.

## What needs to change?

- This should be rewritten to consume data incrementally, instead of re-reading all data for all days for all builds indefinitely. "Closing" a build after two weeks is probably safe. The dashboards for each manufacturer could also share information about each other.
- Dataset access is going away before the end of 2019, so this will need to be ported to use either derived datasets or to use the new live/historical ping tables in BigQuery.

[notebook]: https://dbc-caf9527b-e073.cloud.databricks.com/#notebook/55754/command/55813
