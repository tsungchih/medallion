from enum import Enum

from dagster_pandera import pandera_schema_to_dagster_type

import medallion_air.typing.bronze as bronze
import medallion_air.typing.gold as gold
import medallion_air.typing.silver as silver


class AirQualityTableType(Enum):
    PM25 = 1
    PM10 = 2
    AQI = 3


BronzePm25TableSchemaType = pandera_schema_to_dagster_type(bronze.BronzePm25TableSchema)
BronzePm10TableSchemaType = pandera_schema_to_dagster_type(bronze.BronzePm10TableSchema)
BronzeAqiTableSchemaType = pandera_schema_to_dagster_type(bronze.BronzeAqiTableSchema)


SilverPm25TableSchemaType = pandera_schema_to_dagster_type(silver.SilverPm25TableSchema)
SilverPm10TableSchemaType = pandera_schema_to_dagster_type(silver.SilverPm10TableSchema)
SilverWindTableSchemaType = pandera_schema_to_dagster_type(silver.SilverWindTableSchema)
SilverAqiTableSchemaType = pandera_schema_to_dagster_type(silver.SilverAqiTableSchema)
SilverAirAvgTableSchemaType = pandera_schema_to_dagster_type(silver.SilverAvgTableSchema)
SilverAirTableSchemaType = pandera_schema_to_dagster_type(silver.SilverAirTableSchema)

GoldAqiWithPmSchemaType = pandera_schema_to_dagster_type(gold.GoldAqiWithPmSchema)
GoldAirWithAvgSchemaType = pandera_schema_to_dagster_type(gold.GoldAirWithAvgSchema)
