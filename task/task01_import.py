import pandas as pd

def import_test(FILE_PATH, current_time):
    pass_flag = True

    log_import = ["TASK01: IMPORT TEST"]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    # Read data
    try:
        df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data")
        nrow = df_data.shape[0]
        ncol = df_data.shape[1]
        if nrow == 0:
            log_import.append ("ERROR: Import Data sheet unsucccessfully")
            log_import.append ("No row found")
            pass_flag = False
        elif ncol == 0:
            log_import.append ("ERROR: Import Data sheet unsucccessfully")
            log_import.append ("No column found")
            pass_flag = False
        else:
            log_import.append ("PASS: Import Data sheet succcessfully")
            log_import.append (f"Data sheet has {nrow} row and {ncol} column".format(nrow, ncol))
            log_import.append ("Preview Data sheet")
            log_import.append (df_data.head(3))
    except ValueError as e:
        log_import.append ("ERROR: Import Data sheet unsucccessfully")
        log_import.append ("No Data Sheet found")
        pass_flag = False


    # Read Metadata
    try:
        df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")
        mnrow = df_metadata.shape[0]
        mncol = df_metadata.shape[1]
        mcol_list = df_metadata.columns
        if mnrow == 0:
            log_import.append ("ERROR: Import Metadata sheet unsucccessfully")
            log_import.append ("No row found")
            pass_flag = False
        elif mncol == 0:
            log_import.append ("ERROR: Import Metadata sheet unsucccessfully")
            log_import.append ("No column found")
            pass_flag = False
        else:
            log_import.append ("PASS: Import Metadata sheet succcessfully")
            log_import.append (f"Metadata sheet has {nrow} row and {ncol} column".format(nrow, ncol))
            log_import.append ("Preview Metadata sheet")
            log_import.append (df_metadata.head(3))
    except ValueError as e:
        log_import.append ("ERROR: No Metadata Sheet found")
        pass_flag = False

    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_import:
            f.write(str(r) + "\n")
        f.write("\n")

    return pass_flag