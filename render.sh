#!/usr/bin/env bash
set -e
set -o pipefail

rm webrender.sqlite3
dbfs cp dbfs:/tdsmith/webrender.sqlite3 .
python burndown.py
Rscript -e 'rmarkdown::render("dashboard.Rmd")' > rmarkdown.log 2>&1
