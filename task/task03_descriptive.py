import pandas as pd

def descriptive_test (FILE_PATH, current_time):

    pass_flag = True
    log_descriptive = ["TASK03: Descriptive Test"]
    auto_scale = [1, 2, 3, 4, 5]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")

    use_column = df_metadata.loc[(df_metadata["Is_Include"]=="Yes") & ((df_metadata["Group"] != "Category")), ["Name", "Accepted_Value"]]
    list_column = list(use_column["Name"])

    df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data", usecols=list_column)

    # Descriptive
    for col_name in list_column:
        mean = round(df_data[col_name].describe()["mean"], 3)
        std = round(df_data[col_name].describe()["std"], 3)
        if (mean >= 3) and (std <= 2):
            log_descriptive.append(f"PASS: Column {col_name} has mean = {mean} >= 3 and std = {std} <= 2")
        elif mean < 3:
            log_descriptive.append(f"ERROR: Column {col_name} has mean < 3 that {mean}")
            pass_flag = False
        elif std > 2:
            log_descriptive.append(f"ERROR: Column {col_name} has std > 2 that {std}")
            pass_flag = False

    if pass_flag:
        log_descriptive.append(f"PASS: All column pass descriptive")
        
    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_descriptive:
            f.write(str(r) + "\n")
        f.write("\n")


    return pass_flag