import requests
from dataclasses import dataclass
from GeoPoint import MyDistanceTwoGeopoints, DistanceTwoGeopoints


class ApiManager:
    # Базовый класс для Managers
    def __init__(self, url: str):
        self.url = url

    @property
    def url(self) -> str:
        return self.__url

    @url.setter
    def url(self, url: str) -> None:
        self.__url = url


@dataclass
class Vehicle:
    id: int
    name: str
    model: str
    year: int
    color: str
    price: int
    latitude: float
    longitude: float

    def __str__(self):
        # для датаклассов str и repr определены, но для соотвествия примеру переопределяю
        return f'<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>'

    def __repr__(self):
        return f'<Vehicle: {self.name} {self.model} {self.year} {self.color} {self.price}>'


class VehicleManager(ApiManager):
    vehicles_adress = '/vehicles'
    calc_distance_behavior: DistanceTwoGeopoints = MyDistanceTwoGeopoints()  # способ подсчета растояния

    def get_vehicles(self) -> list[Vehicle]:
        # получить список всех автомобилей

        r = requests.get(
            self.url + VehicleManager.vehicles_adress).json()  # r список всех автомобилей в виде list[dict]
        vehicles_list = [Vehicle(**vehicle) for vehicle in r]  # создаем list[vehicle] из всех vehicle
        return vehicles_list

    def filter_vehicles(self, params: dict) -> list[Vehicle]:
        # получить список всех автомобилей подходящих по параметрам

        filter_list = []
        vehicle_list = self.get_vehicles()
        for vehicle in vehicle_list:
            if params.items() <= vehicle.__dict__.items():  # если параметры входят в vehicle с теми же значениями
                filter_list.append(vehicle)
        return filter_list

    def get_vehicle(self, vehicle_id: int) -> Vehicle:
        # получение одного vehicle по id

        vehicle = requests.get(
            self.url + VehicleManager.vehicles_adress + f'/{vehicle_id}').json()  # отправляе запрос с id и получаем dict
        return Vehicle(**vehicle)

    def add_vehicle(self, vehicle: Vehicle) -> None:
        # добавить новое vehicle

        requests.post(self.url + VehicleManager.vehicles_adress, json=vehicle.__dict__)

    def update_vehicle(self, vehicle: Vehicle) -> None:
        # обновить vehicle на сервере по id

        requests.put(self.url + VehicleManager.vehicles_adress + f'/{vehicle.id}', json=vehicle.__dict__)

    def delete_vehicle(self, id: int) -> None:
        # удалить vehicle по id

        requests.delete(self.url + VehicleManager.vehicles_adress + f'/{id}')

    def get_distance(self, id1: int, id2: int) -> float:
        # Получаем оба id
        # Взовращаем расстояние между двумя vehicle по id
        # получаем 2 vehicle
        vehicle1 = self.get_vehicle(id1)
        vehicle2 = self.get_vehicle(id2)
        # возвращаем растояние между ними
        return self.calc_distance_behavior.calc_distance(vehicle1.longitude, vehicle1.latitude, vehicle2.longitude,
                                                         vehicle2.latitude)

    def get_nearest_vehicle(self, id: int) -> Vehicle:
        # получить близжайший vehicle по id

        vehicle1 = self.get_vehicle(id)
        # Получаем словарь вида {Расстояние до vehicle с входным id: vehicle от которого посчитано расстояние}
        all_distance = {
            self.calc_distance_behavior.calc_distance(vehicle1.longitude, vehicle1.latitude, vehicle2.longitude,
                                                      vehicle2.latitude): vehicle2 for vehicle2 in self.get_vehicles()
            if
            vehicle2.id != id}

        # возвращаем vehicle с минимальным расстоянием
        return all_distance[min(all_distance.keys())]

        # в примере с запросами при id=1 возвращает <Vehicle Kia Sorento 2019 30000>
        # Хотя <Vehicle: Tesla Model 3 2019 white 60000> находмтся ближе (636762.4848697741 против 623774.7599488093)
