import luigi
import pickle
from datetime import date
from datetime import timedelta
from src.utils import constants
from src.utils import unittests
from src.pipeline.aequitas_task import AequitasTask
from src.utils.general import *
from luigi.contrib.postgres import CopyToTable

## PYTHONPATH='.' luigi --module src.pipeline.aequitas_test_task TestAequitasTask --ingesta consecutiva --year 2021 --month 05 --day 03
