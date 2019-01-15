import argparse
from datetime import date, timedelta
import pandas as pd
from . import collect

def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', type=str, default="physics:astro-ph", help="Arxiv category")
    parser.add_argument('-start', type=str, default="2016-08-01", help="start date (YY-MM-DD), (default 2016-08-01) ")
    parser.add_argument('-end', type=str, default="2016-08-31", help="end date (YY-MM-DD), (default 2016-08-31) ")
    parser.add_argument('out', type=str, help="output filename (.h5)")
    parser.add_argument('-dry', action="store_true", help="dry run")
    args = parser.parse_args()

    startdate = date( *(int(s) for s in args.start.split("-")))
    enddate = date( *(int(s) for s in args.end.split("-")))

    print(startdate)
    print(enddate)

    deltatime = enddate - startdate + timedelta(1,0,0)

    PROCEED = False
    if deltatime.days > 0:
        print("# We are collecting %s days of data from %s." % (deltatime.days, args.c) )
        if deltatime.days > 365:
            print("# Range of dates is too long..")
            PROCEED = False
        else:
            print("# Preparing to download.")
            PROCEED = True

    if args.dry:
        print("# This is a dry-run only.")
        PROCEED = False

    if PROCEED:
        df = collector.harvest(arxiv=args.c, from_date=args.start, until_date=args.end)

        store = pd.HDFStore(args.out)
        store['df'] = df
        store.close()

if __name__=='__main__':
    main()
    