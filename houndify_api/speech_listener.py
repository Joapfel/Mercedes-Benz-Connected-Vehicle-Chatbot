from loguru import logger
from houndify_api.houndify import HoundListener


class SpeechListener(HoundListener):
    """
    This class handles the reaction on the Houndify audio transcription.
    """

    def __init__(self):
        super().__init__()

    @logger.catch
    def onPartialTranscript(self, transcript):
        logger.info("Partial transcript: " + transcript)

    @logger.catch
    def onFinalResponse(self, response):
        logger.info(response['AllResults'][0]['WrittenResponse'])

    @logger.catch
    def onError(self, err):
        logger.warning("Error: " + str(err))
