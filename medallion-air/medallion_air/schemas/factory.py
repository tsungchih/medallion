from abc import abstractmethod
from typing import Any

from medallion_air.schemas.air_quality_tables import (
    AirQualityTableBase,
    BronzeAqiTable,
    BronzePm10Table,
    BronzePm25Table,
)
from medallion_air.typing import AirQualityTableType


class SingletonMeta(type):
    """A general purpose singleton metaclass."""

    def __init__(cls, name: str, bases: tuple[type], attrs: dict) -> None:
        """Init singleton metaclass.

        Args:
            name (str): Name of the derived class.
            bases (tuple[type]): Base types of the derived class.
            attrs (dict): Class dictionary of the derived class.
        """
        cls.__single_instance = None
        super().__init__(name, bases, attrs)

    def __call__(cls, *args: Any, **kwargs: Any) -> Any:
        """Create or reuse the singleton.

        Args:
            args (Any): Class constructor positional arguments.
            kwargs: Class constructor keyword arguments.

        Returns:
            Any: A singleton instance of the derived class.
        """
        if cls.__single_instance:
            return cls.__single_instance
        single_obj = cls.__new__(cls)
        single_obj.__init__(*args, **kwargs)
        cls.__single_instance = single_obj
        return single_obj


class TableFactoryBase:
    """Base class for table factory."""

    @abstractmethod
    def create_object(self, otype, contents):
        raise NotImplementedError("You have to implement this method.")


class AirQualityTableFactory(TableFactoryBase, metaclass=SingletonMeta):
    """Class for AirQualityTable factory."""

    table_class = {
        AirQualityTableType.AQI: BronzeAqiTable,
        AirQualityTableType.PM10: BronzePm10Table,
        AirQualityTableType.PM25: BronzePm25Table,
    }

    def create_object(self, otype: AirQualityTableType, contents: str) -> AirQualityTableBase:
        """Create a new object in terms of the given type.

        Args:
            otype (AirQualityTableType): object type

        Returns:
            AirQualityTableBase: The new object with the given type.
        """
        tclass = self.table_class[otype]

        return tclass(contents)
