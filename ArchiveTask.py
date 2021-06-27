import TaskExecutor
import requests
import b_keys_headers as bkh
import time


class Archiwum(TaskExecutor.TaskExecutor):
    def processTask(self, taskData):
        allegro_id = taskData['offerId']
        account = taskData['keyName']


        headers = bkh.get_headers(account)

        offerURL = "https://api.allegro.pl/sale/offers/" + str(allegro_id)

        resp = requests.get(offerURL, headers=headers)

        respStat = resp.status_code

        if respStat != 200:

            startError = f"Nie można rozpocząć: {allegro_id} Nie masz dostępu do tego zasobu. Kod odpowiedzi: {respStat}"
            self.logError(startError)

            return False

        respJson = resp.json()
        try:
            external_id = respJson['external']['id']

        except Exception:

            info = f"Brak SKU. ID: {allegro_id}"
            self.logWarning(info)

            return False

        if external_id == "ARCHIWUM":

            info = f"Aukcja od dawna zarchiwizowana. ID: {allegro_id}"
            self.logInfo(info)
            return True

        respJson['external']['id'] = "ARCHIWUM"

        putter = requests.put(offerURL, json=respJson, headers=headers)
        putStat = putter.status_code
        putCont = putter.content

        if putStat == 200:
            # SUCCESS
            info = f"Sukces: {allegro_id}"

            return True
        else:
            # ERROR
            info =f"Nie można rozpocząć: {allegro_id} Kod odpowiedzi: {respStat}"

            if respStat == 403:
                info = f"Nie można rozpocząć: {allegro_id} Powód: Nieprawidłowe konto."
                
            self.logError(info)
            return False


while True:
    try:
        runner = Archiwum("ALLEGRO", "archiwum")
        runner.run()
        time.sleep(5)
    except:
        print('Connection error')
