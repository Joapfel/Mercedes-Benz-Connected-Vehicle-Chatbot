import geocoder

CLIENT_ID = '0PMQIgsjV5VLffjRXOd6QA=='
CLIENT_KEY = 'pT3N7hj94TGEoFo0DU40UE6VL3hND0rd57J-iJyb_QHyCoU9S-iVbG_jTVGfJQ6GD3AVAxvVVsFXQRvPW7P6mw=='
USER = 'test_user'

g = geocoder.ip('me')
latlong = g.latlng
LOCATION = {
  'Latitude': latlong[0],
  'Longitude': latlong[1],
}
BUFFER_SIZE = 512
