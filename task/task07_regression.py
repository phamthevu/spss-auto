import pandas as pd
import pandas as pd
import numpy as np
import statsmodels.api as sm
from scipy.stats import zscore
from statsmodels.stats.stattools import durbin_watson
from statsmodels.stats.outliers_influence import variance_inflation_factor
from statsmodels.stats.stattools import durbin_watson
import matplotlib.pyplot as plt
import statsmodels.api as sm
import os

def regression_test (FILE_PATH, current_time):

    pass_flag = True
    log_regression = ["TASK07 Regression Test"]

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

    # Regression
    Y_list = list(set(df_metadata.loc[(df_metadata["Is_Depentdent"] == "Yes") & (df_metadata["Group"] != "Category") & (df_metadata["Is_Include"]=="Yes"),"Group"]))
    X_list = list(set(df_metadata.loc[(df_metadata["Is_Depentdent"] == "No") & (df_metadata["Group"] != "Category") & (df_metadata["Is_Include"]=="Yes"),"Group"]))

    if len(Y_list) == 0:
        log_regression.append("ERORR: Don't have Depentdent variable")
        LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

        with open(LOG_FILE, mode="a") as f:
            for r in log_regression:
                f.write(str(r) + "\n")
            f.write("\n")
        pass_flag = False
        return pass_flag

    if len(X_list) == 0:
        
        log_regression.append("ERORR: Don't have In Depentdent variable")
        LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"
        with open(LOG_FILE, mode="a") as f:
            for r in log_regression:
                f.write(str(r) + "\n")
            f.write("\n")
        pass_flag = False
        return pass_flag

    X = df_data.loc[:, X_list]
    X = sm.add_constant(X)
    Y = df_data.loc[:, Y_list]

    model = sm.OLS(Y, X).fit()

    # Unstandardized
    log_regression.append("PASS: Complete calculate Unstandardized Regression")
    log_regression.append(model.summary())

    # Check R
    r2 = model.rsquared
    adj_r2 = model.rsquared_adj

    if (r2 < 0.5) and (adj_r2 < 0.5):
        log_regression.append (f"ERROR: Unstandardized model both R-squared and Adj. R-squared less than 0.5")
        pass_flag = False
    else:
        log_regression.append (f"PASS: Unstandardized model both R-squared and Adj. R-squared more than 0.5")

    # Check F
    f_stat = model.fvalue
    f_pvalue = model.f_pvalue

    if (f_pvalue > 0.05):
        log_regression.append(f"ERROR: Unstandardized model sig of f_value = {round(f_pvalue, 3)} that more than 0.05")
        pass_flag = False
    else:
        log_regression.append(f"PASS: Unstandardized model sig of f_value = {round(f_pvalue, 3)} that less than 0.05")

    # Check DW
    dw = durbin_watson(model.resid)
    if (dw > 1) and (dw < 3):
        log_regression.append(f"PASS: Durbin_Watson index = {round(dw, 3)} in range 1 -> 3")
    else:
        log_regression.append(f"PASS: Durbin_Watson index = {round(dw, 3)} out of range 1 -> 3")
        pass_flag = False

    # Standardized
    X_st = df_data.loc[:, X_list].apply(zscore)
    X_st = sm.add_constant(X_st)
    Y_st = df_data.loc[:, Y_list].apply(zscore)

    model_st = sm.OLS(Y_st, X_st).fit()

    log_regression.append("PASS: Complete calculate Standardized Regression")
    log_regression.append(model.summary())

    # Check R
    r2_st = model_st.rsquared
    adj_r2_st = model_st.rsquared_adj

    if (r2_st < 0.5) and (adj_r2_st < 0.5):
        log_regression.append (f"ERROR: Standardized model both R-squared and Adj. R-squared less than 0.5")
        pass_flag = False
    else:
        log_regression.append (f"PASS: Standardized model both R-squared and Adj. R-squared more than 0.5")

    # Check F
    f_stat_st = model_st.fvalue
    f_pvalue_st = model_st.f_pvalue

    if (f_pvalue_st > 0.05):
        log_regression.append(f"ERROR: Standardized model sig of f_value = {round(f_pvalue_st, 3)} that more than 0.05")
        pass_flag = False
    else:
        log_regression.append(f"PASS: Standardized model sig of f_value = {round(f_pvalue_st, 3)} that less than 0.05")

    # Check DW
    dw_st = durbin_watson(model_st.resid)
    if (dw_st > 1) and (dw_st < 3):
        log_regression.append(f"PASS: Durbin_Watson index = {round(dw_st, 3)} in range 1 -> 3")
    else:
        log_regression.append(f"PASS: Durbin_Watson index = {round(dw_st, 3)} out of range 1 -> 3")
        pass_flag = False

    # Summary
    coef_table = pd.DataFrame({
    "B_Unstandardized": model.params,
    "t_Unstandardized": model.tvalues,
    "Sig._Unstandardized": model.pvalues,
    "B_Standardized": model_st.params,
    "t_Standardized": model_st.tvalues,
    "Sig._Standardized": model_st.pvalues
    }).round(3)

    log_regression.append("Summary Beta, corr and sig value of both Unstandardized and Standardized")
    log_regression.append(coef_table)

    # VIF
    vif_table = pd.DataFrame()
    vif_table["Variable"] = X.columns
    vif_table["VIF"] = [
        variance_inflation_factor(
            X.values,
            i
        )
        for i in range(X.shape[1])
    ]
    log_regression.append("VIF check")
    for x in vif_table.itertuples():
        if (x[2] < 2):
            log_regression.append (f"PASS: VIF of {x[1]} = {round(x[2], 3)} that < 2")
        elif (x[2] < 10):
            log_regression.append (f"ADVISE: VIF of {x[1]} = {round(x[2], 3)} that < 10")
        else:
            log_regression.append (f"ERROR: VIF of {x[1]} = {round(x[2], 3)} that > 10")
            pass_flag = False

    # Residual
    plt.figure()
    df_result = df_data[group].copy()
    df_result["Predicted"] = model.predict(X)
    df_result["Residual"] = model.resid
    df_result["ZPRED"] = zscore(
        df_result["Predicted"]
    )
    df_result["ZRESID"] = zscore(
        df_result["Residual"]
    )
    plt.scatter(
        df_result["ZPRED"],
        df_result["ZRESID"]
    )
    plt.axhline(
        y=0,
        linestyle="--"
    )
    plt.xlabel("ZPRED")
    plt.ylabel("ZRESID")
    plt.title("Scatter Plot of Standardized Residuals")
    file_path_residual = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}_Residual.png"
    plt.savefig(file_path_residual, dpi=300, bbox_inches="tight")
    plt.close()


    # Histogram residual
    plt.figure()
    plt.hist(
        df_result["ZRESID"],
        bins=20
    )
    plt.xlabel("ZRESID")
    plt.ylabel("Frequency")
    plt.title("Histogram of Standardized Residuals")
    file_path_histogram = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}_histogram.png"
    plt.savefig(file_path_histogram, dpi=300, bbox_inches="tight")
    plt.close()

    # Plot
    plt.figure()
    sm.qqplot(
        df_result["ZRESID"],
        line="45"
    )

    plt.title("Normal Q-Q Plot")
    file_path_plot = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}_plot.png"
    plt.savefig(file_path_plot, dpi=300, bbox_inches="tight")
    plt.close()


    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_regression:
            f.write(str(r) + "\n")
        f.write("\n")   

    return pass_flag
