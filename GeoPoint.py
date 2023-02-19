from math import sin, cos, sqrt, atan2, radians
from abc import abstractmethod


class DistanceTwoGeopoints:
    # интерфейс для подсчета растояния между двумя точками. Могут быть разные методы подсчета
    # (например сторонние сервисы, а не формула)
    @staticmethod
    @abstractmethod
    def calc_distance(point1_longitude: float, point1_latitude: float, point2_longitude: float,
                      point2_latitude: float) -> float:
        pass


class MyDistanceTwoGeopoints(DistanceTwoGeopoints):
    # Подсчет расстояния по какой-то формуле из интерента
    @staticmethod
    def calc_distance(point1_longitude: float, point1_latitude: float, point2_longitude: float,
                      point2_latitude: float) -> float:
        R = 6371000.0  # радиус земли в мерах

        # перевод в радианы координат
        lat1 = radians(point1_latitude)
        lon1 = radians(point1_longitude)
        lat2 = radians(point2_latitude)
        lon2 = radians(point2_longitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1

        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c
        return distance
