import time
import logging

import pytest
import pandas
from sqlalchemy import event

from geonature.utils.env import db
from .benchmark_generator import CLater, BenchmarkTest
from geonature.tests.test_synthese import blur_sensitive_observations

logging.basicConfig()
logger = logging.getLogger("logger-name")
logger.setLevel(logging.DEBUG)


@pytest.fixture(scope="class")
def activate_profiling_sql():
    """
    Fixture to activate profiling for SQL queries and storing query's statements and execution times in a csv file.
    """

    results_file = "sql_queries.csv"
    df = pandas.DataFrame([], columns=["Query", "Total Time [s.]"])
    df.to_csv(results_file, mode="a", header=True, index=None, sep=";")

    # @event.listens_for(Engine, "before_cursor_execute")
    def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        conn.info.setdefault("query_start_time", []).append(time.time())
        logger.debug("Start Query: %s" % statement)

    # @event.listens_for(Engine, "after_cursor_execute")
    def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
        total = time.time() - conn.info["query_start_time"].pop(-1)
        logger.debug("Query Complete!")
        logger.debug("Total Time: %f" % total)
        if statement.startswith("SELECT"):
            df = pandas.DataFrame([[statement, total]], columns=["Query", "Total Time"])
            df.to_csv(results_file, mode="a", header=False, index=None, sep=";")

    event.listen(db.engine, "before_cursor_execute", before_cursor_execute)
    event.listen(db.engine, "after_cursor_execute", after_cursor_execute)


def add_bluring_to_benchmark_test_class(benchmark_cls: type):
    """
    Add the blurring enabling fixture to all benchmark tests declared in the given class.

    Parameters
    ----------
    benchmark_cls : type
        benchmark test class
    """
    for attr in dir(benchmark_cls):
        if attr.startswith("test_"):
            b_test = getattr(benchmark_cls, attr)

            # If attribute does not corresponds to a BenchmarkTest, skip
            if not isinstance(b_test, BenchmarkTest):
                continue

            # Include blurring fixture
            kwargs = b_test.function_kwargs
            kwargs["fixtures"] = (
                kwargs["fixtures"] + [blur_sensitive_observations]
                if "fixtures" in kwargs
                else [blur_sensitive_observations]
            )
            # Recreate BenchmarkTest object including the blurring enabling fixture
            setattr(
                benchmark_cls,
                f"{attr}_with_blurring",
                BenchmarkTest(
                    b_test.function, b_test.function_args, kwargs
                )(),  # Run the test function generation while we're at it
            )
            # Generate the test function from the orginal `BenchmarkTest`s
            setattr(
                benchmark_cls,
                attr,
                b_test(),
            )


CLIENT_GET, CLIENT_POST = CLater("self.client.get"), CLater("self.client.post")
