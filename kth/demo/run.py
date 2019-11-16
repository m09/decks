from contextlib import contextmanager
import logging
import time

from IPython.core.display import display, HTML
from pandas import DataFrame
import pymysql

logger = logging.getLogger("run")


@contextmanager
def no_logs():
    level = logger.level
    logger.setLevel(logging.WARN)
    try:
        yield None
    finally:
        logger.setLevel(level)

def _query(query, host="localhost", port=3306, user="root", passwd=""):
    conn = pymysql.connect(host=host, port=port, user=user, passwd=passwd, db="mysql")

    start = time.time()
    cursor = conn.cursor()
    cursor.execute(query)
    end = time.time()

    logger.info("done in %.2f seconds" % (end - start))
    return cursor


def display_html(html):
    display(HTML(html))


def _flatten(sequence):
    if len(sequence) == 1:
        return sequence[0]
    return sequence


def run(query):
    """Query gitbase. Return a tuple of the resulting SQL table columns."""
    return _flatten(tuple(zip(*_query(query))))


def run_one(query):
    return _flatten(_query(query).fetchone())


def run_and_print(query):
    data = []
    cursor = _query(query)
    for line in cursor:
        data.append(list(line))
    display(DataFrame(data, columns=[i[0] for i in cursor.description]))
