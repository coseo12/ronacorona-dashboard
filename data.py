import pandas as pd

conditions = ["confirmed", "deaths", "recovered"]


def dropdown_options(df):
    return df.sort_values("Country_Region").reset_index()[
        "Country_Region"]


def daily_totals_df():
    daily_df = pd.read_csv("data/daily_report.csv")
    totals_df = daily_df[["Confirmed", "Deaths",
                          "Recovered"]].sum().reset_index(name="count")
    totals_df = totals_df.rename(columns={"index": "condition"})
    return totals_df


def daily_countries_df():
    daily_df = pd.read_csv("data/daily_report.csv")
    countries_df = daily_df[["Country_Region",
                             "Confirmed", "Deaths", "Recovered"]]
    countries_df = countries_df.groupby(
        "Country_Region").sum().sort_values(by="Confirmed", ascending=False).reset_index()
    return countries_df


def make_global_df():
    def make_df(condition):
        time_df = pd.read_csv(f"data/time_{condition}.csv")
        time_df = time_df.drop(["Province/State", "Country/Region",
                                "Lat", "Long"], axis=1).sum().reset_index(name=condition)
        time_df = time_df.rename(columns={"index": "date"})
        return time_df

    final_df = None

    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df


def make_country_df(country):
    def make_df(condition):
        time_df = pd.read_csv(f"data/time_{condition}.csv")
        time_df = time_df.loc[time_df["Country/Region"] == country]
        time_df = time_df.drop(columns=[
                               "Province/State", "Country/Region", "Lat", "Long"]).sum().reset_index(name=condition)
        time_df = time_df.rename(columns={"index": "date"})
        return time_df
    final_df = None
    for condition in conditions:
        condition_df = make_df(condition)
        if final_df is None:
            final_df = condition_df
        else:
            final_df = final_df.merge(condition_df)
    return final_df
