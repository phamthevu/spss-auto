import pandas as pd
from factor_analyzer import FactorAnalyzer
import matplotlib.pyplot as plt
from factor_analyzer.factor_analyzer import (
    calculate_kmo,
    calculate_bartlett_sphericity
)

def efa_test (FILE_PATH, current_time):

    pass_flag = True
    log_efa = ["TASK05: EFA Test"]

    a = FILE_PATH.find('IN')+3
    b = FILE_PATH.find('.xlsx')
    FILE_NAME = FILE_PATH[a:b]
    LOG_FOLDER = f"{FILE_PATH[:a-3]}OUT\{FILE_NAME}"

    df_metadata = pd.read_excel(io=FILE_PATH, sheet_name="Metadata")

    use_column = df_metadata.loc[(df_metadata["Is_Include"]=="Yes") & ((df_metadata["Group"] != "Category")), ["Name", "Accepted_Value"]]
    list_column = list(use_column["Name"])

    df_data = pd.read_excel(io=FILE_PATH, sheet_name="Data", usecols=list_column)

    # KMO
    try:
        kmo_all, kmo_model = calculate_kmo(df_data)
        kmo_model = round(kmo_model, 3)
        if kmo_model >= 0.5:
            log_efa.append(f"PASS: KMO all variable = {kmo_model} which > 0.5")
        else:
            log_efa.append(f"ERROR: KMO all variable = {kmo_model} which < 0.5")
            pass_flag = False
    except ValueError as e:
            log_efa.append(f"ERROR: Can not compute KMO, due to {e}")
            pass_flag = False

    # KMO each variable
    kmo_table = pd.DataFrame({"Variable": df_data.columns,"KMO": kmo_all, })

    for v in kmo_table.itertuples():
        if v[2] > 0.5:
              log_efa.append(f"PASS: KMO of {v[1]} = {round(v[2], 3)} that >= 0.5")
        else:
            log_efa.append(f"ERROR: KMO of {v[1]} = {round(v[2], 3)} that < 0.5")

    # Bartlett's Test
    chi_square, p_value = calculate_bartlett_sphericity(df_data)
    chi_square = round(chi_square, 3)
    p_value = round(p_value, 3)
    if p_value < 0.05:
         log_efa.append(f"PASS: chi_square = {chi_square} and p_value = {p_value} that < 0.5")
    else:
         log_efa.append(f"ERROR: chi_square = {chi_square} and p_value = {p_value} that > 0.5")
         pass_flag = False

    # Factor
    fa_test = FactorAnalyzer(rotation=None)
    fa_test.fit(df_data) 

    eigenvalues, vectors = fa_test.get_eigenvalues()

    count = 0
    for i in eigenvalues:
         if i > 1:
              count = count + 1
    log_efa.append(f"ADVISE: Eigenvalues show that should have {count} factor")

    plt.plot(
        range(1, len(eigenvalues) + 1),
        eigenvalues,
        marker="o"
    )
    plt.axhline(
        y=1,
        linestyle="--"
    )

    plt.xlabel("Factor")
    plt.ylabel("Eigenvalue")
    plt.title("Scree Plot")
    # plt.show()

    # EFA + Varimax
    fa = FactorAnalyzer(
        n_factors=count,
        rotation="varimax"
    )

    fa.fit(df_data)

    loadings = pd.DataFrame(
        fa.loadings_,
        index=df_data.columns,
        columns=[x+1 for x in range(count)]
    )

    n = df_data.shape[0]
    visible = 1
    if n > 350:
        visible = 0.3
    elif n > 250:
        visible = 0.35
    elif n > 200:
        visible = 0.4
    elif n > 150:
        visible = 0.45
    elif n > 120:
        visible = 0.5
    elif n > 100:
        visible = 0.55
    elif n > 85:
        visible = 0.6
    elif n > 70:
        visible = 0.65
    elif n > 65:
        visible = 0.7
    elif n > 50:
        visible = 0.75
    else:
        visible = 0.5

    loadings_display = loadings.copy()
    loadings_display = loadings_display.where(
        loadings_display.abs() >= visible,
        ""
    )
    log_efa.append("EFA Rotated Component Matrix")
    log_efa.append(loadings_display)

    LOG_FILE = f"{LOG_FOLDER}\{FILE_NAME}_{current_time}\LOG_{FILE_NAME}_{current_time}.txt"

    with open(LOG_FILE, mode="a") as f:
        for r in log_efa:
            f.write(str(r) + "\n")
        f.write("\n")

    return pass_flag