from medallion_air.schemas.factory import AirQualityTableFactory


def test_singleton__returns_same_instance():
    factory1 = AirQualityTableFactory()
    factory2 = AirQualityTableFactory()

    assert factory1 == factory2
