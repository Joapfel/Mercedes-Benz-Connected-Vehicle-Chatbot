"""
Python wrapper for Mercedes-Benz API Connected Vehicle
https://developer.mercedes-benz.com/apis/connected_vehicle_experimental_api/demo

tryout access-token: a1b2c3d4-a1b2-a1b2-a1b2-a1b2c3d4e5f6
tryout vehicle-id: 1234567890ABCD1234
"""
import requests
import json
from loguru import logger

BASE_URL = 'https://api.mercedes-benz.com/experimental/connectedvehicle_tryout/v1'


class MercedesCvApi:

    __slots__ = '_authorization_token', '_headers'

    def __init__(self, authorization_token):
        self._authorization_token = authorization_token
        self._headers = {'Accept': 'application/json',
                         'Authorization': f'Bearer {authorization_token}'}

    @logger.catch
    def get_vehicles_information(self) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_vehicle_information(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_tires_pressure(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/tires',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_doors_status(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/doors',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def set_doors_status(self, vehicle_id: str, command: str) -> json:
        r = requests.post(url=f'{BASE_URL}/vehicles/{vehicle_id}/doors',
                          headers=self._headers,
                          json={'command': command})
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_location(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/location',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_odometer_information(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/odometer',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_fuel_level(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/fuel',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()

    @logger.catch
    def get_state_of_charge(self, vehicle_id: str) -> json:
        r = requests.get(url=f'{BASE_URL}/vehicles/{vehicle_id}/stateofcharge',
                         headers=self._headers)
        r.raise_for_status()
        return r.json()