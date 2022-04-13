import logging
from datetime import date, timedelta

import click

from arxiv_collector import collector
from arxiv_collector.constants import MAX_NUMBER_OF_DAYS
from arxiv_collector.constants import Default as DEFAULT

logging.basicConfig(level="INFO")
logger = logging.getLogger(__name__)


def clean_date(x: str) -> date:
    return date(*(int(s) for s in x.split("-")))


@click.command()
@click.argument("out_file", help="output filename (.parquet or .csv)")
@click.option("--start", type=str, default=DEFAULT.START_DATE, help=f"Start date (default: {DEFAULT.START_DATE}")
@click.option("--end", type=str, default=DEFAULT.END_DATE, help=f"END date (default: {DEFAULT.END_DATE}")
@click.option("-c", "--cat", type=str, default=DEFAULT.CATEGORY, help="Arxiv category")
@click.option("--dry-run/--no-dry-run", default=False, help="Dry run")
def main(out_file, start, end, cat, dry_run):

    startdate = clean_date(start)
    enddate = clean_date(end)

    logger.info(startdate)
    logger.info(enddate)

    deltatime = enddate - startdate + timedelta(1, 0, 0)

    PROCEED = False
    if deltatime.days > 0:
        logger.info("We are collecting %s days of data from %s." % (deltatime.days, cat))
        if deltatime.days > MAX_NUMBER_OF_DAYS:
            raise ValueError("Range of dates is too long..")

        logger.info("Preparing to download.")
        PROCEED = True

    if dry_run:
        logger.info("This is a dry-run only.")
        PROCEED = False

    if PROCEED:
        df = collector.harvest(arxiv=cat, from_date=start, until_date=end)

        if ".csv" in out_file:
            df.to_csv(out_file)
        elif ".parquet" in out_file:
            df.to_parquet(out_file)
        else:
            raise ValueError("Output file must be either csv or parquet.")


if __name__ == "__main__":
    main()
