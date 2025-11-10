# Universal CSV Analyzer (SPSS-Equivalent in Python)

A comprehensive, SPSS-style statistical analysis tool built in Python.  
It allows users to automatically convert any dataset (SPSS `.sav`, Excel `.xlsx`, `.ods`, `.json`, `.tsv`, `.csv`) into CSV format,  
and perform various statistical analyses such as **T-Test**, **ANOVA**, **Chi-Square**, **Correlation**, and **Regression** — all from the command line.

---

## 🧩 Features

| Category | Functionality | Python Equivalent |
|-----------|----------------|------------------|
| **Data Handling** | Auto-convert `.sav`, `.xlsx`, `.ods`, `.json`, `.tsv`, `.csv` → `.csv` | `pyreadstat`, `pandas` |
| **Descriptive Stats** | Display mean, std, counts, etc. | `pandas.describe()` |
| **T-Test** | Compare means between 2 gender groups | `scipy.stats.ttest_ind` |
| **ANOVA** | Compare means across 3+ groups | `scipy.stats.f_oneway` |
| **Crosstab & Chi-Square** | Test categorical relationships | `pandas.crosstab`, `scipy.stats.chi2_contingency` |
| **Correlation** | Pearson correlation by gender | `pandas.corr()` |
| **Bivariate / Multiple Regression** | Linear modeling (OLS) | `statsmodels.formula.api.ols` |

---

## 🛠️ Installation


1. Install dependencies
bash
Copy code
pip install pandas scipy statsmodels seaborn matplotlib pyreadstat openpyxl odfpy
🚀 How to Use

Step 1 — Run the analyzer
bash
Copy code
python universal_csv_analyzer_en.py

Step 2 — Input your data file
When prompted:

kotlin
Copy code
📂 Please specify the data file (e.g., data.sav, data.xlsx, data.json, data.tsv, data.csv)
Enter the file name: HS_Stressor_data_student_only_06_Clean.sav
You can also define a custom output name:

java
Copy code
💾 Enter output CSV file name (Press Enter for default: HS_Stressor_data_student_only_06_Clean_converted.csv):
→ MyDataset.csv
The script automatically converts and loads the data.

Step 3 — Select your analysis variables
All columns are listed by number.
You can select multiple variables (space-separated):

pgsql
Copy code
Enter column numbers to analyze (multiple allowed, e.g., 3 5 6):
→ 2 5 7
Step 4 — Choose an analysis
markdown
Copy code
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
Example:

pgsql
Copy code
Select an option number: 1
→ Runs T-Test by Gender for all selected numeric variables.
📊 Output Examples
T-Test / ANOVA / Chi-Square

r
Copy code
Grades               | T=   2.314, p=  0.0231, ✅ Significant
Major                | χ²=  4.876, p=  0.0276, ✅ Significant
Correlation Heatmap
Displays a gender-separated heatmap of correlations for selected numeric variables.

Regression Summary
Automatically shows full OLS output with coefficients, p-values, R², and residual plot.

🧠 Notes
The program automatically detects the column containing “Gender”.

Works with datasets in both English and multilingual column headers.

CSV is saved with UTF-8 encoding (utf-8-sig) for cross-platform compatibility.

💡 Future Development
🔹 1. Drag-and-Drop File Input
Future versions will support dragging a data file directly into the window
to automatically start the conversion and analysis.

🔹 2. GUI-Based Interface
Planned upgrade to a fully interactive GUI version (via Tkinter or Streamlit),
allowing users to select files, variables, and analysis methods visually.

👩‍💻 Author
Seiya Genda
University of Nebraska at Kearney — Department of Business & Technology
Focus: Data Analytics × Computer Science × Marketing

🧾 License
This project is released under the MIT License.
You are free to use, modify, and distribute it with attribution.
