# arxiv_collector

## Introduction

This is a basic python package to systematically download meta-data (abstracts, etc) from the Arxiv (www.arxiv.org) using the OAI API (https://arxiv.org/help/bulk_data). The use of arxiv.org is subject to their data access policy (please read https://arxiv.org/help/robots).

## Example

We need specify the start and end dates for abstract and the category (default is phyiscs:astro-ph). For example, the command

```
python collect.py 2015astroph.h5 -start 2015-01-01 -end 2015-12-31
```

downloads all Astro-ph abstracts appears in 2015 and save it in Pandas' HDF5 format. Note that the date is the latest modification date, which may be different from the original date of submission.

Download abstracts for a single year takes around 20 minutes or more.

## About
Author: Wing-Kit Lee (wingkitlee0@outlook.com)

