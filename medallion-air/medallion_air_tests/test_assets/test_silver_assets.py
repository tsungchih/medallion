import pandas as pd
from dagster import Output, build_op_context

from medallion_air.assets.silver.air_quality import (
    silver_aqi_multi_asset,
    silver_pm10_asset,
    silver_pm25_asset,
)
from medallion_air.schemas.air_quality_tables import AirQualityTableBase
from medallion_air.schemas.factory import AirQualityTableFactory
from medallion_air.typing import AirQualityTableType

pm25_test_data = [
    {
        "site": "麥寮",
        "county": "雲林縣",
        "pm25": "31",
        "datacreationdate": "2022-09-28 14:00",
        "itemunit": "μg/m3",
    },
    {
        "site": "關山",
        "county": "臺東縣",
        "pm25": "0",
        "datacreationdate": "2022-09-28 14:00",
        "itemunit": "μg/m3",
    },
    {
        "site": "馬公",
        "county": "澎湖縣",
        "pm25": "",
        "datacreationdate": "2022-09-28 14:00",
        "itemunit": "μg/m3",
    },
]

pm10_test_data = [
    {
        "siteid": "48",
        "sitename": "橋頭",
        "county": "高雄市",
        "itemid": "4",
        "itemname": "懸浮微粒",
        "itemengname": "PM10",
        "itemunit": "μg/m3",
        "monitordate": "2022/09/28 14:00:00",
        "concentration": "33",
    },
    {
        "siteid": "47",
        "sitename": "美濃",
        "county": "高雄市",
        "itemid": "4",
        "itemname": "懸浮微粒",
        "itemengname": "PM10",
        "itemunit": "μg/m3",
        "monitordate": "2022/09/28 14:00:00",
        "concentration": "32",
    },
    {
        "siteid": "46",
        "sitename": "臺南",
        "county": "臺南市",
        "itemid": "4",
        "itemname": "懸浮微粒",
        "itemengname": "PM10",
        "itemunit": "μg/m3",
        "monitordate": "2022/09/28 14:00:00",
        "concentration": "25",
    },
]

aqi_test_data = """{"fields":[{"id":"sitename","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市"}},{"id":"aqi","type":"text","info":{"label":"空氣品質指標"}},{"id":"pollutant","type":"text","info":{"label":"空氣污染指標物"}},{"id":"status","type":"text","info":{"label":"狀態"}},{"id":"so2","type":"text","info":{"label":"二氧化硫(ppb)"}},{"id":"co","type":"text","info":{"label":"一氧化碳(ppm)"}},{"id":"o3","type":"text","info":{"label":"臭氧(ppb)"}},{"id":"o3_8hr","type":"text","info":{"label":"臭氧8小時移動平均(ppb)"}},{"id":"pm10","type":"text","info":{"label":"懸浮微粒(μg/m3)"}},{"id":"pm2.5","type":"text","info":{"label":"細懸浮微粒(μg/m3)"}},{"id":"no2","type":"text","info":{"label":"二氧化氮(ppb)"}},{"id":"nox","type":"text","info":{"label":"氮氧化物(ppb)"}},{"id":"no","type":"text","info":{"label":"一氧化氮(ppb)"}},{"id":"wind_speed","type":"text","info":{"label":"風速(m/sec)"}},{"id":"wind_direc","type":"text","info":{"label":"風向(degrees)"}},{"id":"publishtime","type":"text","info":{"label":"資料發布時間"}},{"id":"co_8hr","type":"text","info":{"label":"一氧化碳8小時移動平均(ppm)"}},{"id":"pm2.5_avg","type":"text","info":{"label":"細懸浮微粒移動平均值(μg/m3)"}},{"id":"pm10_avg","type":"text","info":{"label":"懸浮微粒移動平均值(μg/m3)"}},{"id":"so2_avg","type":"text","info":{"label":"二氧化硫移動平均值(ppb)"}},{"id":"longitude","type":"text","info":{"label":"經度"}},{"id":"latitude","type":"text","info":{"label":"緯度"}},{"id":"siteid","type":"text","info":{"label":"測站編號"}}],"resource_id":"8d2f907f-bbb4-4fdf-8f08-8eabae15da45","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"86","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"sitename":"基隆","county":"基隆市","aqi":"26","pollutant":"","status":"良好","so2":"0","co":"0.18","o3":"19","o3_8hr":"8.1","pm10":"11","pm2.5":"8","no2":"3.5","nox":"6.3","no":"2.8","wind_speed":"2.8","wind_direc":"95","publishtime":"2022/10/01 10:00:00","co_8hr":"0.2","pm2.5_avg":"8","pm10_avg":"12","so2_avg":"0","longitude":"121.760056","latitude":"25.129167","siteid":"1"},{"sitename":"汐止","county":"新北市","aqi":"26","pollutant":"","status":"良好","so2":"0.9","co":"0.19","o3":"22.8","o3_8hr":"5.9","pm10":"9","pm2.5":"9","no2":"6.5","nox":"10","no":"3.5","wind_speed":"1.5","wind_direc":"32","publishtime":"2022/10/01 10:00:00","co_8hr":"0.2","pm2.5_avg":"8","pm10_avg":"14","so2_avg":"0","longitude":"121.6423","latitude":"25.067131","siteid":"2"},{"sitename":"萬里","county":"新北市","aqi":"18","pollutant":"","status":"良好","so2":"0.9","co":"0.12","o3":"19.3","o3_8hr":"9.8","pm10":"18","pm2.5":"5","no2":"3.9","nox":"7.9","no":"3.9","wind_speed":"2.9","wind_direc":"58","publishtime":"2022/10/01 10:00:00","co_8hr":"0.1","pm2.5_avg":"5","pm10_avg":"14","so2_avg":"0","longitude":"121.689881","latitude":"25.179667","siteid":"3"}]}"""

table_factory = AirQualityTableFactory()


def test_silver_pm25_asset():
    ctx = build_op_context()
    df = pd.DataFrame(data=pm25_test_data)
    out: Output[pd.DataFrame] = silver_pm25_asset(ctx, df)
    assert out.value.shape[0] > 0


def test_silver_pm10_asset():
    ctx = build_op_context()
    df = pd.DataFrame(data=pm10_test_data)
    out: Output[pd.DataFrame] = silver_pm10_asset(ctx, df)
    assert out.value.shape[0] > 0


def test_silver_aqi_multi_asset():
    aqi_table: AirQualityTableBase = table_factory.create_object(
        AirQualityTableType.AQI, aqi_test_data
    )
    ctx = build_op_context()
    aqi_table.discover()
    wind_df, aqi_df, air_df, air_avg_df = silver_aqi_multi_asset(ctx, aqi_table.df)

    assert wind_df.value.shape[0] > 0
    assert aqi_df.value.shape[0] > 0
    assert air_df.value.shape[0] > 0
    assert air_avg_df.value.shape[0] > 0
