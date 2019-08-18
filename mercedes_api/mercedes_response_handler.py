import jmespath
from loguru import logger


class MercedesResponseHandler:

    @classmethod
    @logger.catch
    def on_mercedes_indent(cls, car, mercedes, vehicle_id):
        keys = car.keys()
        vehicle_part = ''
        res = None
        user_result = None
        if 'tires' in keys:
            if car['tires'] == 'information':
                res = mercedes.get_tires_pressure(vehicle_id)
                vehicle_part = 'tires'

        elif 'doors' in keys:
            if car['doors'] == 'information':
                res = mercedes.get_doors_status(vehicle_id)
                vehicle_part = 'doors'
            else:
                res = mercedes.set_doors_status(vehicle_id, car['doors'])
                user_result = MercedesResponseHandler.json_command_response_readable('doors', res, car['doors'])

        elif 'location' in keys:
            if car['location'] == 'information':
                res = mercedes.get_location(vehicle_id)
                vehicle_part = 'location'

        elif 'odometer' in keys:
            if car['odometer'] == 'information':
                res = mercedes.get_odometer_information(vehicle_id)
                vehicle_part = 'odometer'

        elif 'fuel' in keys:
            if car['fuel'] == 'information':
                res = mercedes.get_fuel_level(vehicle_id)
                vehicle_part = 'fuel'

        elif 'charge' in keys:
            if car['charge'] == 'information':
                res = mercedes.get_state_of_charge(vehicle_id)
                vehicle_part = 'charge'

        return res, vehicle_part, user_result

    @classmethod
    @logger.catch
    def json_command_response_readable(cls, vehicle_part, res, command):

        readable = 'Sorry, this request is not supported yet by the Mercedes-Benz API'
        if vehicle_part == 'doors':
            status = jmespath.search('status', res)
            if status == 'INITIATED':
                if command == 'LOCK':
                    readable = f'Your cars doors are locked now.'
                elif command == 'UNLOCK':
                    readable = f'Your cars doors are unlocked now.'
            else:
                readable = 'Sorry, the command could not be executed. Please try again.'

        return readable

    @classmethod
    @logger.catch
    def json_information_response_readable(cls, res, vehicle_part):

        readable = 'Sorry, this request is not supported yet by the Mercedes-Benz API'
        if vehicle_part == 'tires':
            unit = jmespath.search('tirepressurefrontleft.unit', res)
            front_left = jmespath.search('tirepressurefrontleft.value', res)
            front_right = jmespath.search('tirepressurefrontright.value', res)
            rear_left = jmespath.search('tirepressurerearleft.value', res)
            rear_right = jmespath.search('tirepressurerearright.value', res)
            readable = f'Your tires have the following pressure values: \n' \
                       f'Front left: {str(front_left)} {unit} \n' \
                       f'Front right: {str(front_right)} {unit} \n ' \
                       f'Rear left: {str(rear_left)} {unit} \n' \
                       f'Rear right: {str(rear_right)} {unit} \n'

        elif vehicle_part == 'doors':
            all_status = jmespath.search('*.value', res)
            open_doors_count = len([open_door for open_door in all_status if open_door == 'OPEN'])
            unlocked_doors_count = len([unlocked_door for unlocked_door in all_status if unlocked_door == 'UNLOCKED'])
            if open_doors_count == 0 and unlocked_doors_count == 0:
                readable = 'All doors are closed and locked.'
            elif open_doors_count != 0 and unlocked_doors_count == 0:
                readable = f'{open_doors_count} doors are open.'
            elif open_doors_count == 0 and unlocked_doors_count != 0:
                readable = f'{unlocked_doors_count} doors are unlocked.'
            else:
                readable = f'{open_doors_count} doors are open and ' \
                           f'{unlocked_doors_count} doors are unlocked.'

        elif vehicle_part == 'location':
            latitude = jmespath.search('latitude.value', res)
            lonitude = jmespath.search('longitude.value', res)
            # TODO: turn this into an actual address
            readable = f'Your car is at latitude: {latitude} and ' \
                       f'longitude: {lonitude}.'

        elif vehicle_part == 'odometer':
            print(res)
            unit = jmespath.search('distancesincereset.unit', res)
            dist_since_reset = jmespath.search('distancesincereset.value', res)
            dist_since_start = jmespath.search('distancesincestart.value', res)
            print(unit)
            print(dist_since_reset)
            print(dist_since_start)
            dist_total = jmespath.search('odometer.value', res)
            readable = f'You have driven {dist_since_start} {unit} since you started, \n' \
                       f'since the last reset you drove {dist_since_reset} {unit}, \n' \
                       f'and you drove {dist_total} {unit} in total.'

        elif vehicle_part == 'fuel':
            unit = jmespath.search('fuellevelpercent.unit', res)
            fuel_level = jmespath.search('fuellevelpercent.value', res)
            readable = f'Your cars fuel level is at {fuel_level} {unit}.'

        elif vehicle_part == 'charge':
            unit = jmespath.search('stateofcharge.unit', res)
            charge_state = jmespath.search('stateofcharge.value', res)
            readable = f'Your cars state of charge is at {charge_state} {unit}.'

        return readable
