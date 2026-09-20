import pandas as pd

def cronbach (df):
    # k = number of items (columns)
    k = df.shape[1]
    
    # Calculate variance of individual items (ddof=1 for sample variance)
    item_variances = df.var(axis=0, ddof=1).sum()
    
    # Calculate variance of total scores per respondent
    total_scores_variance = df.sum(axis=1).var(ddof=1)
    
    # Apply the Cronbach's Alpha formula
    return round((k / (k - 1)) * (1 - (item_variances / total_scores_variance)), 3)


def cronbach_test (FILE_PATH, current_time):

    pass_flag = True
    log_cronbach = ["TEST04: Cronbach Test"]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")

    use_column = df_metadata.loc[(df_metadata["Is_Include"]=="Yes") & ((df_metadata["Group"] != "Category")), ["Name", "Accepted_Value"]]
    list_column = list(use_column["Name"])

    df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data", usecols=list_column)

    group_list = set(df_metadata.loc[(df_metadata["Group"] != "Category") & (df_metadata["Is_Include"]=="Yes"),"Group"])

    for group in group_list:
        item = list(df_metadata.loc[(df_metadata["Group"] == group) & (df_metadata["Is_Include"]=="Yes"), "Name"])
        df_check_all = df_data.loc[: ,item]

        cr_all = cronbach(df_check_all)
        if cr_all == 1:
            log_cronbach.append(f"ERROR: Cronbach Alpha of {group} is {cr_all}, compare")
        elif (cr_all >= 0.8) and (cr_all < 1):
            log_cronbach.append(f"PASS VERY GOOD: Cronbach Alpha of {group} is {cr_all} in range 0.8 -> 1")
        elif (cr_all >= 0.7) and (cr_all < 0.8):
            log_cronbach.append(f"PASS GOOD: Cronbach Alpha of {group} is {cr_all} in range 0.7 -> 0.8")
        elif (cr_all >= 0.6):
            log_cronbach.append(f"PASS: Cronbach Alpha of {group} is {cr_all} in range 0.6 -> 0.7")
        else:
            log_cronbach.append(f"ERROR: Cronbach Alpha of {group} is {cr_all} < 0.6")
            pass_flag = False
    # Dive into if deleted
            for remove_item in item:
                new_list = item.copy()
                new_list.remove(remove_item)
                df_check_remove = df_data.loc[: ,new_list]
                cr_remove = cronbach(df_check_remove)
                if cr_remove > 0.6:
                    log_cronbach.append(f"ADVISE: Cronbach Alpha of {group} if remove {remove_item} is {cr_remove} which > 0.6, consider to remove")
                else:
                    log_cronbach.append(f"ADVISE: Cronbach Alpha of {group} if remove {remove_item} is {cr_remove} which stll < 0.6")

    if pass_flag:
        log_cronbach.append(f"PASS: All group pass cronbach")
        
    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_cronbach:
            f.write(str(r) + "\n")
        f.write("\n")

    return pass_flag  