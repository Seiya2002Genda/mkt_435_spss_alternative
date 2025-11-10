import pandas as pd
import scipy.stats as stats
import statsmodels.api as sm
import statsmodels.formula.api as smf
import matplotlib.pyplot as plt
import seaborn as sns
import os
import pyreadstat

# ====== Step 1. Automatic File Conversion ======
print("📂 Please specify the data file (e.g., data.sav, data.xlsx, data.json, data.tsv, data.csv)")
input_file = input("Enter the file name: ").strip()

# Check if the input file exists
if not os.path.exists(input_file):
    raise FileNotFoundError(f"❌ File not found: {input_file}")

# Get file extension
ext = os.path.splitext(input_file)[1].lower()

# Let the user define output CSV file name
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

# Save as CSV
df.to_csv(output_csv, index=False, encoding="utf-8-sig")
print(f"✅ File successfully converted to CSV → {output_csv}")

# ====== Step 2. Data Preparation ======
df = pd.read_csv(output_csv)
print(f"\n🎯 Data loaded successfully ({len(df)} rows, {len(df.columns)} columns)")

# ====== Detect Gender column ======
gender_col = None
for c in df.columns:
    if "gender" in c.lower():
        gender_col = c
        break
if gender_col is None:
    raise ValueError("⚠️ No Gender column found. Please check the column names.")

groups = df[gender_col].dropna().unique()
print(f"\n🎯 Gender column detected: {gender_col} 👥 Groups: {list(groups)}")
print("=" * 90)

# ====== Show all columns ======
print("\n📋 List of variables (Select by number)\n")
for i, col in enumerate(df.columns):
    print(f"{i+1}. {col}")

# ====== Select target variables ======
selected_idx = input("\nEnter column numbers to analyze (multiple allowed, e.g., 3 5 6): ").split()
selected_vars = [df.columns[int(i)-1] for i in selected_idx if i.isdigit()]
print(f"\n🎯 Selected variables: {selected_vars}")
print("=" * 90)

# ====== Analysis Menu ======
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


# ====== Analysis Functions ======
def t_test():
    print("\n🔹【T-Test】Difference of means by Gender\n")
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            g1 = df[df[gender_col] == groups[0]][var].dropna()
            g2 = df[df[gender_col] == groups[1]][var].dropna()
            if len(g1) > 1 and len(g2) > 1:
                t, p = stats.ttest_ind(g1, g2)
                print(f"{var:<20} | T={t:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)


def anova():
    print("\n🔹【One-way ANOVA】Gender-based mean comparison\n")
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            samples = [df[df[gender_col] == g][var].dropna() for g in groups]
            if all(len(s) > 1 for s in samples):
                f, p = stats.f_oneway(*samples)
                print(f"{var:<20} | F={f:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)


def crosstab():
    print("\n🔹【Cross-tabulations】Gender × Categorical Variables\n")
    for var in selected_vars:
        if not pd.api.types.is_numeric_dtype(df[var]):
            table = pd.crosstab(df[gender_col], df[var])
            print(f"\n📊 {var}")
            print(table)
    print("-" * 80)


def chi_square():
    print("\n🔹【Chi-Square Test】Gender × Categorical Variables\n")
    for var in selected_vars:
        if not pd.api.types.is_numeric_dtype(df[var]):
            table = pd.crosstab(df[gender_col], df[var])
            chi2, p, dof, ex = stats.chi2_contingency(table)
            print(f"{var:<20} | χ²={chi2:>8.3f}, p={p:>8.4f}, {'✅ Significant' if p<0.05 else '❌ Not significant'}")
    print("-" * 80)


def correlation():
    print("\n🔹【Correlation Analysis】Correlation by Gender\n")
    numeric_vars = [v for v in selected_vars if pd.api.types.is_numeric_dtype(df[v])]
    if len(numeric_vars) < 2:
        print("⚠️ At least two numeric variables are required for correlation analysis.")
        return
    for g in groups:
        sub = df[df[gender_col] == g][numeric_vars]
        corr = sub.corr().round(2)
        print(f"\n--- {gender_col} = {g} ---")
        print(corr)
        sns.heatmap(corr, annot=True, cmap="coolwarm")
        plt.title(f"Correlation Matrix ({gender_col} = {g})")
        plt.show()


def bivariate_regression():
    print("\n🔹【Bivariate Regression】Simple linear regression\n")
    for var in selected_vars:
        if pd.api.types.is_numeric_dtype(df[var]):
            formula = f"{var} ~ C({gender_col})"
            model = smf.ols(formula, data=df).fit()
            print(f"\n📘 Model: {formula}")
            print(model.summary())
            sns.regplot(x=gender_col, y=var, data=df, ci=None)
            plt.title(f"Bivariate Regression: {var} ~ Gender")
            plt.show()


def multiple_regression():
    print("\n🔹【Multiple Regression】Multiple linear regression\n")
    numeric_vars = [v for v in selected_vars if pd.api.types.is_numeric_dtype(df[v])]
    if len(numeric_vars) < 2:
        print("⚠️ At least two numeric variables are required for multiple regression.")
        return
    dep_var = input(f"\nSelect the dependent variable {numeric_vars}: ")
    indep_vars = [v for v in numeric_vars if v != dep_var]
    formula = f"{dep_var} ~ C({gender_col}) + " + " + ".join(indep_vars)
    model = smf.ols(formula, data=df).fit()
    print(f"\n📘 Model: {formula}")
    print(model.summary())
    sns.residplot(x=model.fittedvalues, y=model.resid, lowess=True, line_kws={'color': 'red'})
    plt.title(f"Residual Plot ({dep_var})")
    plt.show()


# ====== Step 3. Run Analysis Menu ======
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
