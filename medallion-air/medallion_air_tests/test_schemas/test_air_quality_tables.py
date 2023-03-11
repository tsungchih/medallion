import pytest

from medallion_air.schemas.air_quality_tables import (
    AirQualityTableBase,
    BronzeAqiTable,
    BronzePm10Table,
    BronzePm25Table,
)
from medallion_air.schemas.factory import AirQualityTableFactory
from medallion_air.typing import AirQualityTableType


@pytest.mark.parametrize(
    "otype, expected",
    [
        (AirQualityTableType.PM25, BronzePm25Table),
        (AirQualityTableType.PM10, BronzePm10Table),
        (AirQualityTableType.AQI, BronzeAqiTable),
    ],
)
def test_air_quality_tables__create_correct_instance(otype, expected):
    table_factory = AirQualityTableFactory()
    table_obj = table_factory.create_object(otype=otype, contents="")
    assert isinstance(table_obj, expected)


@pytest.mark.parametrize(
    "otype, contents",
    [
        (
            AirQualityTableType.PM25,
            '{"fields":[{"id":"site","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市名稱"}},{"id":"pm25","type":"text","info":{"label":"細懸浮微粒濃度"}},{"id":"datacreationdate","type":"text","info":{"label":"資料建置日期"}},{"id":"itemunit","type":"text","info":{"label":"測項單位"}}],"resource_id":"c1f31192-babd-4105-b880-a4c2e23a3276","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"78","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"site":"大城","county":"彰化縣","pm25":"18","datacreationdate":"2022-09-28 10:00","itemunit":"μg/m3"}]}',
        ),
        (
            AirQualityTableType.PM10,
            '{"fields":[{"id":"siteid","type":"text","info":{"label":"測站代碼"}},{"id":"sitename","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市"}},{"id":"itemid","type":"text","info":{"label":"測項代碼"}},{"id":"itemname","type":"text","info":{"label":"測項名稱"}},{"id":"itemengname","type":"text","info":{"label":"測項英文名稱"}},{"id":"itemunit","type":"text","info":{"label":"測項單位"}},{"id":"monitordate","type":"text","info":{"label":"監測日期"}},{"id":"concentration","type":"text","info":{"label":"數值"}}],"resource_id":"d12a1d8b-ddd8-4e3f-87bf-9c5bbd45be28","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"78","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_319?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_319?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"siteid":"85","sitename":"大城","county":"彰化縣","itemid":"4","itemname":"懸浮微粒","itemengname":"PM10","itemunit":"μg/m3","monitordate":"2022/09/30 08:00:00","concentration":"62"},{"siteid":"84","sitename":"富貴角","county":"新北市","itemid":"4","itemname":"懸浮微粒","itemengname":"PM10","itemunit":"μg/m3","monitordate":"2022/09/30 08:00:00","concentration":"16"}]}',
        ),
        (
            AirQualityTableType.AQI,
            '{"fields":[{"id":"sitename","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市"}},{"id":"aqi","type":"text","info":{"label":"空氣品質指標"}},{"id":"pollutant","type":"text","info":{"label":"空氣污染指標物"}},{"id":"status","type":"text","info":{"label":"狀態"}},{"id":"so2","type":"text","info":{"label":"二氧化硫(ppb)"}},{"id":"co","type":"text","info":{"label":"一氧化碳(ppm)"}},{"id":"o3","type":"text","info":{"label":"臭氧(ppb)"}},{"id":"o3_8hr","type":"text","info":{"label":"臭氧8小時移動平均(ppb)"}},{"id":"pm10","type":"text","info":{"label":"懸浮微粒(μg/m3)"}},{"id":"pm2.5","type":"text","info":{"label":"細懸浮微粒(μg/m3)"}},{"id":"no2","type":"text","info":{"label":"二氧化氮(ppb)"}},{"id":"nox","type":"text","info":{"label":"氮氧化物(ppb)"}},{"id":"no","type":"text","info":{"label":"一氧化氮(ppb)"}},{"id":"wind_speed","type":"text","info":{"label":"風速(m/sec)"}},{"id":"wind_direc","type":"text","info":{"label":"風向(degrees)"}},{"id":"publishtime","type":"text","info":{"label":"資料發布時間"}},{"id":"co_8hr","type":"text","info":{"label":"一氧化碳8小時移動平均(ppm)"}},{"id":"pm2.5_avg","type":"text","info":{"label":"細懸浮微粒移動平均值(μg/m3)"}},{"id":"pm10_avg","type":"text","info":{"label":"懸浮微粒移動平均值(μg/m3)"}},{"id":"so2_avg","type":"text","info":{"label":"二氧化硫移動平均值(ppb)"}},{"id":"longitude","type":"text","info":{"label":"經度"}},{"id":"latitude","type":"text","info":{"label":"緯度"}},{"id":"siteid","type":"text","info":{"label":"測站編號"}}],"resource_id":"8d2f907f-bbb4-4fdf-8f08-8eabae15da45","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"86","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"sitename":"基隆","county":"基隆市","aqi":"22","pollutant":"","status":"良好","so2":"0","co":"0.17","o3":"24.1","o3_8hr":"9.7","pm10":"8","pm2.5":"5","no2":"3.5","nox":"5.8","no":"2.3","wind_speed":"0.6","wind_direc":"78","publishtime":"2022/09/30 10:00:00","co_8hr":"0.2","pm2.5_avg":"6","pm10_avg":"12","so2_avg":"0","longitude":"121.760056","latitude":"25.129167","siteid":"1"},{"sitename":"汐止","county":"新北市","aqi":"25","pollutant":"","status":"良好","so2":"0.9","co":"0.28","o3":"16.6","o3_8hr":"4.7","pm10":"19","pm2.5":"7","no2":"15.2","nox":"25.8","no":"10.5","wind_speed":"0.9","wind_direc":"342","publishtime":"2022/09/30 10:00:00","co_8hr":"0.1","pm2.5_avg":"7","pm10_avg":"15","so2_avg":"0","longitude":"121.6423","latitude":"25.067131","siteid":"2"}]}',
        ),
    ],
)
def test_air_quality_tables__get_dataframe(otype, contents):
    table_factory = AirQualityTableFactory()
    table_obj: AirQualityTableBase = table_factory.create_object(otype=otype, contents=contents)
    table_obj.discover()
    df = table_obj.df
    row_count, col_count = df.shape

    assert row_count > 0
    assert col_count > 0


@pytest.mark.parametrize(
    "otype, contents",
    [
        (
            AirQualityTableType.PM25,
            '{"fields":[{"id":"site","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市名稱"}},{"id":"pm25","type":"text","info":{"label":"細懸浮微粒濃度"}},{"id":"datacreationdate","type":"text","info":{"label":"資料建置日期"}},{"id":"itemunit","type":"text","info":{"label":"測項單位"}}],"resource_id":"c1f31192-babd-4105-b880-a4c2e23a3276","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"78","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_02?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"site":"大城","county":"彰化縣","pm25":"18","datacreationdate":"2022-09-28 10:00","itemunit":"μg/m3"}]}',
        ),
        (
            AirQualityTableType.PM10,
            '{"fields":[{"id":"siteid","type":"text","info":{"label":"測站代碼"}},{"id":"sitename","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市"}},{"id":"itemid","type":"text","info":{"label":"測項代碼"}},{"id":"itemname","type":"text","info":{"label":"測項名稱"}},{"id":"itemengname","type":"text","info":{"label":"測項英文名稱"}},{"id":"itemunit","type":"text","info":{"label":"測項單位"}},{"id":"monitordate","type":"text","info":{"label":"監測日期"}},{"id":"concentration","type":"text","info":{"label":"數值"}}],"resource_id":"d12a1d8b-ddd8-4e3f-87bf-9c5bbd45be28","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"78","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_319?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_319?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"siteid":"85","sitename":"大城","county":"彰化縣","itemid":"4","itemname":"懸浮微粒","itemengname":"PM10","itemunit":"μg/m3","monitordate":"2022/09/30 08:00:00","concentration":"62"},{"siteid":"84","sitename":"富貴角","county":"新北市","itemid":"4","itemname":"懸浮微粒","itemengname":"PM10","itemunit":"μg/m3","monitordate":"2022/09/30 08:00:00","concentration":"16"}]}',
        ),
        (
            AirQualityTableType.AQI,
            '{"fields":[{"id":"sitename","type":"text","info":{"label":"測站名稱"}},{"id":"county","type":"text","info":{"label":"縣市"}},{"id":"aqi","type":"text","info":{"label":"空氣品質指標"}},{"id":"pollutant","type":"text","info":{"label":"空氣污染指標物"}},{"id":"status","type":"text","info":{"label":"狀態"}},{"id":"so2","type":"text","info":{"label":"二氧化硫(ppb)"}},{"id":"co","type":"text","info":{"label":"一氧化碳(ppm)"}},{"id":"o3","type":"text","info":{"label":"臭氧(ppb)"}},{"id":"o3_8hr","type":"text","info":{"label":"臭氧8小時移動平均(ppb)"}},{"id":"pm10","type":"text","info":{"label":"懸浮微粒(μg/m3)"}},{"id":"pm2.5","type":"text","info":{"label":"細懸浮微粒(μg/m3)"}},{"id":"no2","type":"text","info":{"label":"二氧化氮(ppb)"}},{"id":"nox","type":"text","info":{"label":"氮氧化物(ppb)"}},{"id":"no","type":"text","info":{"label":"一氧化氮(ppb)"}},{"id":"wind_speed","type":"text","info":{"label":"風速(m/sec)"}},{"id":"wind_direc","type":"text","info":{"label":"風向(degrees)"}},{"id":"publishtime","type":"text","info":{"label":"資料發布時間"}},{"id":"co_8hr","type":"text","info":{"label":"一氧化碳8小時移動平均(ppm)"}},{"id":"pm2.5_avg","type":"text","info":{"label":"細懸浮微粒移動平均值(μg/m3)"}},{"id":"pm10_avg","type":"text","info":{"label":"懸浮微粒移動平均值(μg/m3)"}},{"id":"so2_avg","type":"text","info":{"label":"二氧化硫移動平均值(ppb)"}},{"id":"longitude","type":"text","info":{"label":"經度"}},{"id":"latitude","type":"text","info":{"label":"緯度"}},{"id":"siteid","type":"text","info":{"label":"測站編號"}}],"resource_id":"8d2f907f-bbb4-4fdf-8f08-8eabae15da45","__extras":{"api_key":"e8dd42e6-9b8b-43f8-991e-b3dee723a52d"},"include_total":true,"total":"86","resource_format":"object","limit":"1000","offset":"0","_links":{"start":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc","next":"/api/v2/aqx_p_432?api_key=e8dd42e6-9b8b-43f8-991e-b3dee723a52d&limit=1000&format=json&sort=ImportDate desc&offset=1000"},"records":[{"sitename":"基隆","county":"基隆市","aqi":"22","pollutant":"","status":"良好","so2":"0","co":"0.17","o3":"24.1","o3_8hr":"9.7","pm10":"8","pm2.5":"5","no2":"3.5","nox":"5.8","no":"2.3","wind_speed":"0.6","wind_direc":"78","publishtime":"2022/09/30 10:00:00","co_8hr":"0.2","pm2.5_avg":"6","pm10_avg":"12","so2_avg":"0","longitude":"121.760056","latitude":"25.129167","siteid":"1"},{"sitename":"汐止","county":"新北市","aqi":"25","pollutant":"","status":"良好","so2":"0.9","co":"0.28","o3":"16.6","o3_8hr":"4.7","pm10":"19","pm2.5":"7","no2":"15.2","nox":"25.8","no":"10.5","wind_speed":"0.9","wind_direc":"342","publishtime":"2022/09/30 10:00:00","co_8hr":"0.1","pm2.5_avg":"7","pm10_avg":"15","so2_avg":"0","longitude":"121.6423","latitude":"25.067131","siteid":"2"}]}',
        ),
    ],
)
def test_air_quality_tables__get_metadata(otype, contents):
    table_factory = AirQualityTableFactory()
    table_obj: AirQualityTableBase = table_factory.create_object(otype=otype, contents=contents)
    table_obj.discover()
    metadata = table_obj.metadata

    assert metadata.get("row_count") > 0
    assert metadata.get("col_count") > 0
