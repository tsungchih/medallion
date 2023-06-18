import pendulum
from dagster import HourlyPartitionsDefinition

hourly_partitions_def = HourlyPartitionsDefinition(
    start_date=pendulum.now().subtract(months=1).format(fmt="YYYY-MM-DD-HH:mm"),
    timezone="Asia/Taipei",
)
