#!/usr/bin/env bash
set -e
set -o pipefail

rm -f webrender_*.sqlite3
dbfs cp dbfs:/tdsmith/webrender_nvidia.sqlite3 .
dbfs cp dbfs:/tdsmith/webrender_amd.sqlite3 .
dbfs cp dbfs:/tdsmith/webrender_intel.sqlite3 .
python burndown.py
Rscript -e 'rmarkdown::render("dashboard.Rmd", params=list(dbname="webrender_nvidia.sqlite3"), output_file="dashboard_nvidia.html")' > rmarkdown.log 2>&1
Rscript -e 'rmarkdown::render("dashboard.Rmd", params=list(dbname="webrender_amd.sqlite3"), output_file="dashboard_amd.html")' >> rmarkdown.log 2>&1
Rscript -e 'rmarkdown::render("dashboard.Rmd", params=list(dbname="webrender_intel.sqlite3"), output_file="dashboard_intel.html")' >> rmarkdown.log 2>&1
