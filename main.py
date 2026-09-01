from task.task01_import import import_test
from task.task02_data import data_test
from task.task03_descriptive import descriptive_test
from task.task04_cronbach import cronbach_test
from task.task05_efa import efa_test
from task.task06_pearson import peason_test
from task.task07_regression import regression_test
import shutil
from pathlib import Path
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

ROOT_FOLDER = Path("D:/Desktop/Research/Automate/SPSS_Auto/Data")
IN_PATH = ROOT_FOLDER / "IN"

files = list(IN_PATH.glob("*.xlsx"))

for file in files:
    current_time = datetime.now().strftime("%Y%m%d_%H%M%S")
    FILE_NAME = file.stem
    FILE_PATH = str(file)
    SLOT_LOG_FOLDER = (
        ROOT_FOLDER
        / "OUT"
        / FILE_NAME
        / f"{FILE_NAME}_{current_time}"
    )
    SLOT_LOG_FOLDER.mkdir(parents=True, exist_ok=True)

    print(f"RUNNING {FILE_NAME} FILE AT {current_time}")
    step = 0
    if import_test(FILE_PATH, current_time):
        step = step + 1
        if data_test(FILE_PATH, current_time):
            step = step + 1
            if descriptive_test(FILE_PATH, current_time):
                step = step + 1
                if cronbach_test(FILE_PATH, current_time):
                    step = step + 1
                    if efa_test(FILE_PATH, current_time):
                        step = step + 1
                        if peason_test(FILE_PATH, current_time):
                            step = step + 1
                            if regression_test(FILE_PATH, current_time):
                                step = step + 1
    if step == 7:
        print (f"COMPLETED {FILE_NAME} FILE WITH 7/7 STEP SUCCESSFULLY")
    else:
        print (f"{FILE_NAME} FILE FAIL AT STEP {step+1}/7")
    ARCHIVE_PATH = f"{ROOT_FOLDER}/Archive/{FILE_NAME}_{current_time}.xlsx"
    shutil.move(FILE_PATH,ARCHIVE_PATH)
    
