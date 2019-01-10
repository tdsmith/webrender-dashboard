#!/usr/bin/env bash
set -e
set -o pipefail

rm -f webrender.sqlite3 webrender_nvidia.sqlite3
# dbfs cp dbfs:/tdsmith/webrender.sqlite3 .
dbfs cp dbfs:/tdsmith/webrender_nvidia.sqlite3 .
python burndown.py
Rscript -e 'rmarkdown::render("dashboard.Rmd")' > rmarkdown.log 2>&1
# Rscript -e 'rmarkdown::render("dashboard.Rmd", params=list(dbname="webrender_nvidia.sqlite3"), output_file="dashboard_nvidia.html")' > rmarkdown.log 2>&1
