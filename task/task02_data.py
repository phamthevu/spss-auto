import pandas as pd

def data_test (FILE_PATH, current_time):

    pass_flag = True

    log_data = ["TASK02: DATA TEST"]
    auto_scale = [1, 2, 3, 4, 5]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")

    use_column = df_metadata.loc[(df_metadata["Is_Include"]=="Yes") & ((df_metadata["Group"] != "Category")), ["Name", "Accepted_Value"]]
    list_column = list(use_column["Name"])
    
    df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data", usecols=list_column)

    # Check null
    null_cells = df_data.isna().stack()
    for (row, column), value in null_cells[null_cells].items():
        log_data.append (f"ERROR: Row {row} at column {column} has NULL value")
        pass_flag = False

    # Check value
    for col_name in list_column:
        accepted_str = accepted_str = use_column.loc[use_column["Name"] == col_name, "Accepted_Value"].iloc[0]
        accepted_list = []
        while len (accepted_str) > 0:
            if (accepted_str[0].isdigit()):
                accepted_list.append(int(accepted_str[0]))
                accepted_str = accepted_str[1:]
            else:
                accepted_str = accepted_str[1:]
        if len(accepted_str) == 0:
            accepted_list = auto_scale

        df_check = df_data[col_name]
        invalid = df_check.loc[~df_check.isin(accepted_list)]
        if invalid.size > 0:
            for index, value in invalid.items():
                log_data.append (f"ERROR: Column {col_name} at row {index} has outlier value {value}")
                pass_flag = False
       

    if pass_flag:
        log_data.append (f"PASS: No null and outlier value")

    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_data:
            f.write(str(r) + "\n")
        f.write("\n")

    return pass_flag