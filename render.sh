#!/usr/bin/env bash
set -e
set -o pipefail

rm webrender.sqlite3
dbfs cp dbfs:/tdsmith/webrender.sqlite3 .
Rscript -e 'rmarkdown::render("dashboard.Rmd")' > rmarkdown.log 2>&1
