import requests
from loguru import logger
import uuid
import b_keys_headers as bkh
import json
import datetime




def put_command(ajdiki: list):  # Allegro put command

    allegroUUID = uuid.uuid4()
    url = 'https://api.allegro.pl/sale/offer-publication-commands/'
    url += str(allegroUUID)

    publicateCommand = {
        "publication": {"action": "END"},
        "offerCriteria": [{

            "offers": [],
            "type": "CONTAINS_OFFERS"

        }]
    }

    for ajdi in ajdiki:
        publicateCommand['offerCriteria'][0]['offers'].append({"id": ajdiki})

    pub = requests.put(url=url, json=publicateCommand)
    updateStatus = pub.status_code
    updateContent = pub.content

    if updateStatus >= 300:
        # TODO: logger
        logger.error(
            f'Publicate error: Response code -> {updateStatus} Content -> {updateContent}')
        # post_logs()
    else:
        logger.success(
            f'Command publicated successfully. Response code -> {updateStatus}')

def get_command_report(allegroUUID):  # Allegro get command report

        fails = {}

        repUrl = f'https://api.allegro.pl/sale/offer-modification-commands/{allegroUUID}/tasks'
        getReport = requests.get(url=repUrl).json()

        for report in getReport['tasks']:

            if report['errors'] != []:
                fails[report['offer']['id']] = []

                for error in report['errors']:
                    fails[report['offer']['id']].append(error)

        if fails == {}:
            logger.success('OFFERS UPDATED SUCCESSFULLY')
            return True
        else:
            logger.warning('OFFERS UPDATED WITH ERRORS')
            return fails
            




