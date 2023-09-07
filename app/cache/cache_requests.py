import time
import threading
import requests
import json

class Cache_requests():
    """

    """
    def __init__(self, based_url, timeout=3, ping_url="/ping", ping_delay=5, collection=None):
        self.based_url = based_url
        self.ping_url = ping_url
        self.timeout = timeout
        self.ping_delay = ping_delay
        self.collection = collection
        self.status = True

        # запуск потока пингующего внешний сервер
        self.ping_thread = threading.Thread(
            target = self.ping_loop,
            daemon = True
        )
        self.ping_thread.start()

    # отправка запроса на сервер
    def send(self, method="POST", url="", data={}, headers={}, cache=True):
        kwargs = {
            "method": method,
            "url": url,
            "data": data,
            "headers": headers
        }

        # находим уже существующий запрос в бд
        search_result = None
        if cache and self.collection != None:
            search_result = self.collection.find_one(kwargs)

        # если сервер жив, то отправляем запрос
        if self.status:
            # запрос
            r = requests.request(
                method,
                url = self.based_url + url,
                data = data,
                headers = headers
            )
            r.encoding = 'utf-8'

            # обработка запроса с отлавливанием ошибок
            try:
                response = r.json()

                # сохранем запрос в бд, если он прошёл успешно
                if cache and self.collection != None:
                    self.collection.delete_many(kwargs)
                    id = self.collection.insert_one({
                        **kwargs,
                        "response": response
                    })

                return response

            except Exception as e:
                raise Exception("RESPONSE: " + r.text)

        else:
            # если сервер заболел, то отпраляем то что в кэше, или ошибку
            if search_result:
                return search_result['response']

            else:
                raise Exception("RESPONSE: External server down. No cache")

    # отправка запроса на сервер (пинг)
    def _ping(self):
        try:
            r = requests.get(self.based_url + self.ping_url)
            return True

        except:
            return False

    # цикл понга сервера
    def ping_loop(self):
        while True:
            self.status = self._ping()
            time.sleep(self.ping_delay)

    # полчить текущий статус внешнего сервера
    def get_status(self):
        return self.status
