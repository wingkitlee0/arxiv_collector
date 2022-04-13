import datetime
import logging
import time

# python 3
import urllib.error
import xml.etree.ElementTree as ET
from urllib.request import urlopen

import pandas as pd

logger = logging.getLogger(__name__)

pd.set_option("mode.chained_assignment", "warn")


OAI = "{http://www.openarchives.org/OAI/2.0/}"
ARXIV = "{http://arxiv.org/OAI/arXiv/}"
BASE_URL = "http://export.arxiv.org/oai2?verb=ListRecords"


def get_arxiv_url(arxiv: str, from_date: str, until_date: str) -> str:
    return f"{BASE_URL}&from={from_date}&until={until_date}&metadataPrefix=arXiv&set={arxiv}"


def harvest(arxiv="physics:astro-ph", from_date="2016-08-01", until_date="2016-08-31") -> pd.DataFrame:
    """
    input: arxiv is the "set" defined in http://export.arxiv.org/oai2?verb=ListSets
    """

    url = get_arxiv_url(arxiv, from_date, until_date)

    while True:
        logger.info("fetching %s", url)
        try:
            response = urlopen(url)

        except urllib.error.HTTPError as e:
            if e.code == 503:
                to = int(e.hdrs.get("retry-after", 30))
                logger.info("Got 503. Retrying after {0:d} seconds.".format(to))

                time.sleep(to)
                continue

            else:
                raise

        xml = response.read()

        root = ET.fromstring(xml)

        dfs: list[pd.DataFrame] = []
        for record in root.find(OAI + "ListRecords").findall(OAI + "record"):
            # arxiv_id = record.find(OAI + "header").find(OAI + "identifier")
            meta = record.find(OAI + "metadata")
            info = meta.find(ARXIV + "arXiv")
            created = info.find(ARXIV + "created").text
            created = datetime.datetime.strptime(created, "%Y-%m-%d")
            categories = info.find(ARXIV + "categories").text
            authors = info.find(ARXIV + "authors").findall(ARXIV + "author")

            # first author only
            keyname = authors[0].find(ARXIV + "keyname").text if authors[0].find(ARXIV + "keyname") is not None else ""
            forenames = (
                authors[0].find(ARXIV + "forenames").text if authors[0].find(ARXIV + "forenames") is not None else ""
            )
            first_author = f"{keyname} {forenames}"

            # if there is more than one DOI use the first one
            # often the second one (if it exists at all) refers
            # to an eratum or similar
            doi = info.find(ARXIV + "doi")
            if doi is not None:
                doi = doi.text.split()[0]

            contents = {
                "title": info.find(ARXIV + "title").text,
                "id": info.find(ARXIV + "id").text,  # arxiv_id.text[4:],
                "abstract": info.find(ARXIV + "abstract").text.strip(),
                "created": created,
                "categories": categories.split(),
                "doi": doi,
                "first_author": first_author,
            }

            df = pd.DataFrame(contents)
            dfs.append(df)

        df_all = pd.concat(dfs, ignore_index=True)

        # The list of articles returned by the API comes in chunks of
        # 1000 articles. The presence of a resumptionToken tells us that
        # there is more to be fetched.
        token = root.find(OAI + "ListRecords").find(OAI + "resumptionToken")
        if token is None or token.text is None:
            break

        else:
            url = f"{BASE_URL}&resumptionToken={token.text}"
    logger.info("fetching finished.")
    return df_all
