import geocoder
import pyaudio

# jojokr94 email
#CLIENT_ID = 'ewJ4eGWCK3HBMoEx-ZrawA=='
#CLIENT_KEY = 'sP62N_We1I4APdEm39cADJrjYVWalAvmWYk2pt7n9sN7yveGyfvl_zXXL3OBTpVjHKZH-csxn4Rt-CDYmgfq2Q=='
#CLIENT_ID = '0PMQIgsjV5VLffjRXOd6QA=='
#CLIENT_KEY = 'pT3N7hj94TGEoFo0DU40UE6VL3hND0rd57J-iJyb_QHyCoU9S-iVbG_jTVGfJQ6GD3AVAxvVVsFXQRvPW7P6mw=='

# kreamer_johannes email
CLIENT_ID = 'I5cAetj1DYOtuFOD5b2Xhg=='
CLIENT_KEY = 'RaCWbrvhhUNiI6F63IDHkQUTyEudWkas4KkoAGCT72b4BlU93AnbmBcNWzh70Xi_FEmNbvnQgRBTO7Ex6WIPYA=='

USER = 'test_user'

g = geocoder.ip('me')
latlong = g.latlng
REQUEST_INFO = {
  'Latitude': latlong[0],
  'Longitude': latlong[1],
  #'StoredGlobalPagesToMatch': ["connected-car"],
  'PartialTranscriptsDesired': True,
  'ResponseAudioVoice': 'Richard',
  'ResponseAudioShortOrLong': 'Short'
}

# audio settings
BUFFER_SIZE = 512
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
CHUNK = 1024
RECORD_SECONDS = 5
