import logging
import pytest
from geonature.tests.benchmarks import *
from geonature.tests.test_pr_occhab import stations

from .benchmark_generator import BenchmarkTest, CLater

logging.basicConfig()
logger = logging.getLogger("logger-name")
logger.setLevel(logging.DEBUG)

from .utils import CLIENT_GET, CLIENT_POST


@pytest.mark.usefixtures("client_class", "temporary_transaction")
class TestBenchmarkOcchab:

    test_get_station = BenchmarkTest(
        CLIENT_GET,
        [CLater("""url_for("occhab.get_station", id_station=8)""")],
        dict(user_profile="user", fixtures=[stations]),
    )()
