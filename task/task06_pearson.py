import pandas as pd
from scipy.stats import pearsonr

def peason_test (FILE_PATH, current_time):

    pass_flag = True
    log_peason = ["Task06: Peason Test"]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")

    use_column = df_metadata.loc[(df_metadata["Is_Include"]=="Yes") & ((df_metadata["Group"] != "Category")), ["Name", "Accepted_Value"]]
    list_column = list(use_column["Name"])

    df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data", usecols=list_column)

    group_list = set(df_metadata.loc[(df_metadata["Group"] != "Category") & (df_metadata["Is_Include"]=="Yes"),"Group"])

    # Compute group by using mean
    for group in group_list:
        item = list(df_metadata.loc[(df_metadata["Group"] == group) & (df_metadata["Is_Include"]=="Yes"), "Name"])
        df_data[group] = df_data[item].mean(axis=1).round(3)

    dic = {}

    for groupA in group_list:
        dic[groupA] = {}

        for groupB in group_list:
            r, p = pearsonr(
                df_data[groupA],
                df_data[groupB]
            )

            r = round(r, 3)
            p = round(p, 3)

            dic[groupA][groupB] = (r, p)

    df_corr = pd.DataFrame(dic).T

    log_peason.append ("PASS: Peason Correlation maxtrix compute successfully with peason, p_value")
    log_peason.append(df_corr)

    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_peason:
            f.write(str(r) + "\n")
        f.write("\n") 

    return pass_flag