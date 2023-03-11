import pandas as pd
from dagster import build_op_context

from medallion_air.assets.gold.air_quality import gold_aqi_with_pm_asset

pm25_test_data = [
    {
        "site": "基隆",
        "county": "基隆市",
        "pm25": "31",
        "event_time": "2022/10/05 08:00:00",
    },
    {
        "site": "汐止",
        "county": "新北市",
        "pm25": "0",
        "event_time": "2022/10/05 08:00:00",
    },
    {
        "site": "萬里",
        "county": "新北市",
        "pm25": "21",
        "event_time": "2022/10/05 08:00:00",
    },
]

pm10_test_data = [
    {
        "site": "基隆",
        "county": "基隆市",
        "event_time": "2022/10/05 08:00:00",
        "pm10": "33",
    },
    {
        "site": "汐止",
        "county": "新北市",
        "event_time": "2022/10/05 08:00:00",
        "pm10": "32",
    },
    {
        "site": "萬里",
        "county": "新北市",
        "event_time": "2022/10/05 08:00:00",
        "pm10": "25",
    },
]

aqi_test_data = [
    {
        "site": "基隆",
        "county": "基隆市",
        "aqi": "28",
        "event_time": "2022/10/05 08:00:00",
    },
    {
        "site": "汐止",
        "county": "新北市",
        "aqi": "25",
        "event_time": "2022/10/05 08:00:00",
    },
    {
        "site": "萬里",
        "county": "新北市",
        "aqi": "25",
        "event_time": "2022/10/05 08:00:00",
    },
]


def test_gold__gold_aqi_with_pm_asset():
    ctx = build_op_context()
    astype_dict = {
        "site": "str",
        "county": "str",
        "pm25": "float32",
        "pm10": "float32",
        "aqi": "float32",
        "event_time": "datetime64[ns]",
    }

    silver_pm25_df = pd.DataFrame(pm25_test_data)
    silver_pm10_df = pd.DataFrame(pm10_test_data)
    silver_aqi_df = pd.DataFrame(aqi_test_data)

    for col in astype_dict:
        if col in silver_pm25_df.columns:
            silver_pm25_df[col] = silver_pm25_df[col].astype(astype_dict[col])
        if col in silver_pm10_df.columns:
            silver_pm10_df[col] = silver_pm10_df[col].astype(astype_dict[col])
        if col in silver_aqi_df.columns:
            silver_aqi_df[col] = silver_aqi_df[col].astype(astype_dict[col])

    # df = df[result_cols]
    # df = df.astype(astype_dict)

    gold_aqi_with_pm_df = gold_aqi_with_pm_asset(ctx, silver_pm25_df, silver_pm10_df, silver_aqi_df)
    df: pd.DataFrame = gold_aqi_with_pm_df.value

    assert df.shape[0] > 0
    assert df.shape[1] > 0
