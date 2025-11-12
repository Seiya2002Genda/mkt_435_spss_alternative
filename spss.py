import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pyreadstat

# ====== Function: Load or Reuse Last Used File ======
def load_or_reuse_file():
    saved_file = "saved_file.csv"

    # Check if a previously used file exists
    if os.path.exists(saved_file):
        with open(saved_file, "r", encoding="utf-8") as f:
            last_used = f.read().strip()
        if last_used and os.path.exists(last_used):
            print(f"📁 Last used file detected: {last_used}")
            use_prev = input("Reuse this file? (y/n): ").strip().lower()
            if use_prev == "y":
                print(f"✅ Reusing previous file: {last_used}")
                return last_used

    # Request a new file input
    print("📂 Please specify the data file (e.g., data.sav, data.xlsx, data.json, data.tsv, data.csv)")
    input_file = input("Enter the file name: ").strip()

    if not os.path.exists(input_file):
        raise FileNotFoundError(f"❌ File not found: {input_file}")

    # Save the newly entered file path for next use
    with open(saved_file, "w", encoding="utf-8") as f:
        f.write(input_file)

    print(f"✅ Saved as last used file: {input_file}")
    return input_file


# ====== Step 1. Automatic File Conversion ======
input_file = load_or_reuse_file()
ext = os.path.splitext(input_file)[1].lower()
default_output = os.path.splitext(input_file)[0] + "_converted.csv"
output_csv = input(f"💾 Enter output CSV file name (Press Enter for default: {default_output}): ").strip()
if output_csv == "":
    output_csv = default_output

print(f"\n🔍 Loading file: {input_file}")
try:
    if ext == ".sav":
        df, meta = pyreadstat.read_sav(input_file)
    elif ext in [".xls", ".xlsx"]:
        df = pd.read_excel(input_file)
    elif ext == ".ods":
        df = pd.read_excel(input_file, engine="odf")
    elif ext == ".json":
        df = pd.read_json(input_file)
    elif ext in [".tsv", ".txt"]:
        df = pd.read_csv(input_file, sep="\t")
    elif ext == ".csv":
        df = pd.read_csv(input_file)
    else:
        raise ValueError(f"⚠️ Unsupported file format: {ext}")
except Exception as e:
    raise ValueError(f"❌ File loading error: {e}")

df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"✅ File successfully converted to CSV → {output_csv}")

# ====== Step 2. Data Preparation ======
df = pd.read_csv(output_csv)
print(f"\n🎯 Data loaded successfully ({len(df)} rows, {len(df.columns)} columns)")

# ====== Select Fixed Variable (Group Column) ======
print("\n📋 List of variables (Select FIXED variable by number)\n")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

group_idx = input("\nEnter the column number to use as FIXED variable (grouping): ").strip()
if not group_idx.isdigit():
    raise ValueError("⚠️ Invalid input. You must enter a number.")
group_col = df.columns[int(group_idx)-1]
df[group_col] = df[group_col].astype(str)
groups = df[group_col].dropna().unique().tolist()
print(f"\n🎯 Fixed variable selected: {group_col} 👥 Groups: {groups}")
print("=" * 90)

# ====== Select Variable(s) to Analyze (Changeable) ======
selected_idx = input("\nEnter column numbers to analyze (multiple allowed, e.g., 3 5 6): ").split()
selected_vars = [df.columns[int(i)-1] for i in selected_idx if i.isdigit()]
print(f"\n🎯 Changeable (analyzed) variables: {selected_vars}")
print("=" * 90)

# ====== Menu ======
def show_menu():
    print("""
================= Analysis Menu =================
1. T-Test (Difference of means between two groups)
2. One-way ANOVA (Mean differences among 3+ groups)
3. Cross-tabulations (Contingency tables)
4. Chi-Square Test (Test of independence)
5. Correlation Analysis
6. Bivariate Regression (Simple linear regression)
7. Multiple Regression (Multiple linear regression)
0. Exit
=================================================
""")

# ====== Utility Functions ======
def _valid_groups(min_k=2):
    uniq = [g for g in df[group_col].dropna().unique().tolist() if g != ""]
    return len(uniq) >= min_k, uniq

def _is_categorical(series: pd.Series) -> bool:
    return (not pd.api.types.is_numeric_dtype(series)) or series.nunique(dropna=True) <= 20

# ====== Analysis Functions ======
def t_test():
    print(f"\n🔹【T-Test】Difference of means by {group_col}\n")
    ok, uniq = _valid_groups(2)
    if not ok:
        print("⚠️ Need at least 2 groups for a t-test.")
        return
    if len(uniq) != 2:
        print(f"⚠️ T-test requires exactly 2 groups, but found {len(uniq)}: {uniq}. Skipping.")
        return
    g1_label, g2_label = uniq[0], uniq[1]
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            g1 = df[df[group_col] == g1_label][var].dropna()
            g2 = df[df[group_col] == g2_label][var].dropna()
            if len(g1) > 1 and len(g2) > 1:
                t, p = stats.ttest_ind(g1, g2, equal_var=False, nan_policy='omit')
                print(f"{var:<20} | T={t:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)

def anova():
    print(f"\n🔹【One-way ANOVA】{group_col}-based mean comparison\n")
    ok, uniq = _valid_groups(2)
    if not ok:
        print("⚠️ Need at least 2 groups for ANOVA.")
        return
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            samples = [df[df[group_col] == g][var].dropna() for g in uniq]
            samples = [s for s in samples if len(s) > 1]
            if len(samples) >= 2:
                f, p = stats.f_oneway(*samples)
                print(f"{var:<20} | F={f:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)

def crosstab():
    print(f"\n🔹【Cross-tabulations】{group_col} × Categorical Variables\n")
    for var in selected_vars:
        if _is_categorical(df[var]):
            sub = df[[group_col, var]].dropna()
            if not sub.empty:
                table = pd.crosstab(sub[group_col], sub[var])
                print(f"\n📊 {var}")
                print(table)
    print("-" * 80)

def chi_square():
    print(f"\n🔹【Chi-Square Test】{group_col} × Categorical Variables\n")
    for var in selected_vars:
        if _is_categorical(df[var]):
            sub = df[[group_col, var]].dropna()
            table = pd.crosstab(sub[group_col], sub[var])
            if table.shape[0] >= 2 and table.shape[1] >= 2:
                chi2, p, dof, ex = stats.chi2_contingency(table)
                print(f"{var:<20} | χ²={chi2:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)

def correlation():
    print(f"\n🔹【Correlation Analysis】Correlation by {group_col}\n")
    numeric_vars = [v for v in selected_vars if pd.api.types.is_numeric_dtype(df[v])]
    if len(numeric_vars) < 2:
        print("⚠️ At least two numeric variables are required for correlation analysis.")
        return
    ok, uniq = _valid_groups(1)
    if not ok:
        print("⚠️ No valid groups.")
        return
    for g in uniq:
        sub = df[df[group_col] == g][numeric_vars].dropna()
        if sub.shape[0] < 2:
            continue
        corr = sub.corr().round(2)
        print(f"\n--- {group_col} = {g} ---")
        print(corr)
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title(f"Correlation Matrix ({group_col} = {g})")
        plt.show()

def bivariate_regression():
    print(f"\n🔹【Bivariate Regression】Simple linear regression by {group_col}\n")
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            formula = f"{var} ~ C({group_col})"
            model = smf.ols(formula, data=df).fit()
            print(f"\n📘 Model: {formula}")
            print(model.summary())

def multiple_regression():
    print(f"\n🔹【Multiple Regression】Multiple linear regression by {group_col}\n")
    numeric_vars = [v for v in selected_vars if pd.api.types.is_numeric_dtype(df[v])]
    if len(numeric_vars) < 2:
        print("⚠️ At least two numeric variables are required for multiple regression.")
        return
    dep_var = input(f"\nSelect the dependent variable {numeric_vars}: ").strip()
    if dep_var not in numeric_vars:
        print("⚠️ Dependent variable must be one of the listed numeric variables.")
        return
    indep_vars = [v for v in numeric_vars if v != dep_var]
    formula = f"{dep_var} ~ C({group_col}) + " + " + ".join(indep_vars)
    model = smf.ols(formula, data=df).fit()
    print(f"\n📘 Model: {formula}")
    print(model.summary())

# ====== Step 3. Run Menu ======
while True:
    show_menu()
    choice = input("Select an option number: ")
    if choice == "1":
        t_test()
    elif choice == "2":
        anova()
    elif choice == "3":
        crosstab()
    elif choice == "4":
        chi_square()
    elif choice == "5":
        correlation()
    elif choice == "6":
        bivariate_regression()
    elif choice == "7":
        multiple_regression()
    elif choice == "0":
        print("✅ Analysis finished. Exiting program.")
        break
    else:
        print("⚠️ Invalid input. Please enter a number between 0 and 7.")
