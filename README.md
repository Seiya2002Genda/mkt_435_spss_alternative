# Universal CSV Analyzer (SPSS-Equivalent in Python)

A comprehensive, SPSS-style statistical analysis tool built in **Python**.
It automatically converts datasets (SPSS `.sav`, Excel `.xlsx`, `.ods`, `.json`, `.tsv`, `.csv`) into CSV format and performs key statistical analyses such as **T-Test**, **ANOVA**, **Chi-Square**, **Correlation**, and **Regression** — all from the command line.

---

## 🧩 Features

| Category                            | Functionality                                                          | Python Equivalent                                 |
| ----------------------------------- | ---------------------------------------------------------------------- | ------------------------------------------------- |
| **Data Handling**                   | Auto-convert `.sav`, `.xlsx`, `.ods`, `.json`, `.tsv`, `.csv` → `.csv` | `pyreadstat`, `pandas`                            |
| **Descriptive Stats**               | Display mean, std, count, etc.                                         | `pandas.describe()`                               |
| **T-Test**                          | Compare means between two groups                                       | `scipy.stats.ttest_ind`                           |
| **ANOVA**                           | Compare means across 3+ groups                                         | `scipy.stats.f_oneway`                            |
| **Crosstab & Chi-Square**           | Test categorical relationships                                         | `pandas.crosstab`, `scipy.stats.chi2_contingency` |
| **Correlation**                     | Pearson correlation grouped by variable                                | `pandas.corr()`                                   |
| **Bivariate / Multiple Regression** | Linear modeling (OLS)                                                  | `statsmodels.formula.api.ols`                     |

---

## 🛠️ Installation

Install dependencies:

```bash
pip install pandas scipy statsmodels seaborn matplotlib pyreadstat openpyxl odfpy
```

---

## 🚀 How to Use

### Step 1 — Run the analyzer

```bash
python spss.py
```

### Step 2 — Input your data file

When prompted:

```
📂 Please specify the data file (e.g., data.sav, data.xlsx, data.json, data.tsv, data.csv)
Enter the file name: HS_Stressor_data_student_only_06_Clean.sav
```

You can also define a custom output file name:

```
💾 Enter output CSV file name (Press Enter for default: HS_Stressor_data_student_only_06_Clean_converted.csv):
→ MyDataset.csv
```

The script automatically converts and loads your dataset.

### Step 3 — Select your analysis variables

All columns will be listed numerically.
You can select multiple variables (space-separated):

```
Enter column numbers to analyze (multiple allowed, e.g., 3 5 6):
→ 2 5 7
```

### Step 4 — Choose an analysis

```
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
```

Example:

```
Select an option number: 1
→ Runs T-Test for all selected numeric variables.
```

---

## 📊 Output Examples

### T-Test / ANOVA / Chi-Square

```
Grades               | T=   2.314, p=  0.0231, ✅ Significant
Major                | χ²=  4.876, p=  0.0276, ✅ Significant
```

### Correlation Heatmap

Displays a grouped heatmap of correlations for selected numeric variables.

### Regression Summary

Outputs a full OLS regression summary, including coefficients, p-values, R², and residual plot.

---

## 🧠 Notes

* The program allows manual selection of the **grouping variable** (fixed) and **analysis variables** (changeable).
* Works with multilingual datasets (UTF-8 encoding).
* Automatically remembers and reuses the last opened file via `saved_file.csv`.

---

## 💡 Future Development

### 🔹 Drag-and-Drop File Input

Planned support for drag-and-drop file selection to start analysis instantly.

### 🔹 GUI-Based Interface

Future GUI version (Tkinter or Streamlit) to allow visual variable selection and analysis control.

---

## 👩‍💻 Author

**Seiya Genda**
University of Nebraska at Kearney — College of Business & Technology
Focus: Data Analytics × Computer Science × Marketing

---

## 🧾 License

Released under the **MIT License**.
Free for use, modification, and distribution with attribution.
