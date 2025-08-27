import marimo

__generated_with = "0.14.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    return (mo,)


@app.cell
def _():
    import pandas as pd
    import numpy as np
    import matplotlib.pyplot as plt
    import seaborn as sns
    from scipy.stats import skew, kurtosis, shapiro
    return kurtosis, np, pd, plt, shapiro, skew, sns


@app.cell
def _(mo):
    mo.md(r"""1.""")
    return


@app.cell
def _(pd):
    df = pd.read_csv("bank_loan.csv")
    return (df,)


@app.cell
def _(df):
    df.head()
    return


@app.cell
def _(df):
    df.info()
    return


@app.cell
def _(df):
    df.describe()
    return


@app.cell
def _(df):
    df.shape
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""2.""")
    return


@app.cell
def _(df):
    print(df.isnull().sum()[df.isnull().sum() > 0])
    return


@app.cell
def _(df):
    df_missing_cols = df[df.columns[df.isnull().any()]]
    return


@app.cell
def _(df):
    missing_percent = (df.isnull().sum() / len(df)) * 100
    print(missing_percent[missing_percent > 0])
    return


@app.cell
def _(df):
    print(df["EmploymentStatus"].value_counts(dropna=False))
    print("-" * 30)
    print(df["HomeOwnershipStatus"].value_counts(dropna=False))
    return


@app.cell
def _(df):
    print(df["NumberOfDependents"].value_counts(dropna=False).sort_index())
    print("-" * 30)
    print(df["MonthlyDebtPayments"].describe())
    print("-" * 30)
    print(df["JobTenure"].describe())
    return


@app.cell
def _(df):
    # به نظرم حتی میشه برای نامشخص یه دسته عددی تعریف کرد یا حتی با مد پرش کرد
    df["HomeOwnershipStatus"] = df["HomeOwnershipStatus"].fillna("Unknown")

    df["EmploymentStatus"] = df["EmploymentStatus"].fillna(
        df["EmploymentStatus"].mode()[0]
    )

    # با میانه پر کردم گفتم میانگین  احتمال تحت تاثیر داده های بزرگ و کوچک و پرته
    numeric_cols = ["NumberOfDependents", "MonthlyDebtPayments", "JobTenure"]
    for col in numeric_cols:
        df[col] = df[col].fillna(df[col].median())
    return


@app.cell
def _(df):
    print(df.isnull().sum()[df.isnull().sum() > 0])
    return


@app.cell(hide_code=True)
def _(mo):
    mo.md(r"""3.""")
    return


@app.cell
def _():
    # خب به نظرم قبل اینکه در رابطه با داده های پرت تصمیم بگیرم بیام و تحلیل تک متغیره انجام بدم ، اینجوری بهتر میشه تصمیم گرفت
    # میخوام یه تابع بنویسم اسم ستون رو بهش بدم اطلاعات آماری اون ستون رو برام برگردونه و متناسب با نوع داده تصمیم بگیره
    return


@app.cell
def _(kurtosis, np, pd, plt, shapiro, skew, sns):
    def univariate_analysis_godmode(series, plot=True):
        col_name = series.name

        if pd.api.types.is_numeric_dtype(series):
            median_val = series.median()
            mode_val = series.mode()[0] if not series.mode().empty else np.nan
            mean_val = series.mean()
            std_val = series.std()
            min_val = series.min()
            max_val = series.max()
            q1 = series.quantile(0.25)
            q3 = series.quantile(0.75)
            iqr = q3 - q1
            outliers = series[
                (series < q1 - 1.5 * iqr) | (series > q3 + 1.5 * iqr)
            ]

            try:
                stat, p_value = shapiro(series)
                normality = "Normal" if p_value > 0.05 else "Not Normal"
            except:
                normality = "Test Failed"

            report = {
                "count": len(series),
                "mean": mean_val,
                "median": median_val,
                "mode": mode_val,
                "std": std_val,
                "min": min_val,
                "25%": q1,
                "75%": q3,
                "max": max_val,
                "skew": skew(series),
                "kurtosis": kurtosis(series),
                "outlier_count": len(outliers),
                "normality": normality,
            }

            if plot:
                plt.figure(figsize=(12, 4))
                plt.subplot(1, 2, 1)
                sns.histplot(series, kde=True)
                plt.title(f"{col_name} - Histogram")
                plt.subplot(1, 2, 2)
                sns.boxplot(x=series)
                plt.title(f"{col_name} - Boxplot")
                plt.show()

        else:
            value_counts = series.value_counts()
            mode_val = series.mode()[0] if not series.mode().empty else np.nan
            unique_count = series.nunique()

            report = {
                "count": len(series),
                "unique": unique_count,
                "mode": mode_val,
                "value_counts": value_counts.to_dict(),
            }

            if plot:
                plt.figure(figsize=(8, 4))
                sns.countplot(x=series, order=value_counts.index)
                plt.title(f"{col_name} - Countplot")
                plt.xticks(rotation=45)
                plt.show()

        return report
    return (univariate_analysis_godmode,)


@app.cell
def _(df, univariate_analysis_godmode):
    res_num = univariate_analysis_godmode(df["MonthlyDebtPayments"])
    res_cat = univariate_analysis_godmode(df["EmploymentStatus"])
    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
