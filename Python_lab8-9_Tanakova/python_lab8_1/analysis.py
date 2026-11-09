import pandas as pd

df = pd.read_csv("inflation_2018_2019.csv")
df = df.rename(columns={"Inflation, consumer prices (annual %)": "Inflation"})

print("=== Базова інформація ===")
print("Розмір даних:", df.shape)
print(df.info())
print("\nОписова статистика:")
print(df.describe())

print("\nПропущені значення:")
print(df.isnull().sum())
print("Кількість дублікатів:", df.duplicated().sum())

pivot = df.pivot(index="Country", columns="Year", values="Inflation")
pivot.columns = ["Inflation_2018", "Inflation_2019"]

pivot["Diff_2019_2018"] = pivot["Inflation_2019"] - pivot["Inflation_2018"]
pivot["Pct_Change"] = (pivot["Diff_2019_2018"] / pivot["Inflation_2018"].abs()) * 100
pivot["Abs_Diff"] = pivot["Diff_2019_2018"].abs()

def get_category(val):
    if val < 0:
        return "Дефляція"
    elif val < 2:
        return "Низька (<2%)"
    elif val < 5:
        return "Помірна (2-5%)"
    elif val < 10:
        return "Висока (5-10%)"
    else:
        return "Дуже висока (≥10%)"

pivot["Category_2019"] = pivot["Inflation_2019"].apply(get_category)
pivot["Category_2018"] = pivot["Inflation_2018"].apply(get_category)

region_keywords = [
    "Africa", "Asia", "Europe", "America", "World", "income", "OECD",
    "IDA", "IBRD", "dividend", "states", "area", "Union", "Pacific",
    "Caribbean", "Fragility", "HIPC", "Least", "Middle East"
]
pivot["Is_Country"] = ~pivot.index.str.contains("|".join(region_keywords), case=False, na=False)

high_inflation = pivot[(pivot["Is_Country"]) & (pivot["Inflation_2019"] > 10)]
high_inflation = high_inflation.sort_values("Inflation_2019", ascending=False)

print("\n=== Країни з інфляцією > 10% у 2019 ===")
print(high_inflation[["Inflation_2019", "Inflation_2018", "Diff_2019_2018"]].head(10))

top10 = (
    pivot[pivot["Is_Country"]]
    .sort_values("Inflation_2019", ascending=False)
    .head(10)
)

print("\n=== Топ-10 країн за інфляцією 2019 ===")
print(top10[["Inflation_2019", "Inflation_2018", "Diff_2019_2018"]])

countries = pivot[pivot["Is_Country"]]

category_stats = countries.groupby("Category_2019").agg(
    Кількість=("Inflation_2019", "count"),
    Середня=("Inflation_2019", "mean"),
    Медіана=("Inflation_2019", "median"),
    Мін=("Inflation_2019", "min"),
    Макс=("Inflation_2019", "max")
).sort_values("Середня", ascending=False)

print("\n=== Агрегація за категоріями інфляції 2019 ===")
print(category_stats)

result = pivot.reset_index()
result.to_csv("inflation_analysis_results.csv", index=False, encoding="utf-8")

print("\nРезультати збережено у файл: inflation_analysis_results.csv")