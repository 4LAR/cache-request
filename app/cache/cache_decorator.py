import time
import datetime
import threading
from functools import wraps
from globals import *

THREAD_CACHE = None

################################################################################
#
#   Данный декортаор совместим с другими декараторами
#
# Аргументы:
#   secure     - (флаг) ставим True если запрос требует авторизации
#   life_hours - (число) сколько часов будет хранится закешированный ответ
#
#
# Пример применения:
#   @cache.cache_decorator(secure=True, life_hours=12)
#   @deco.try_decorator
#   def test(...):
#     ...
#     return ...
#
#   Для корректной работы в основном файле проекта надо выполнить функцию
# <<thread_cache_lifetime>>, она запустит поток который удаляет элементы
# у которых истёк срок жизни
#
################################################################################

# декторатор кеширования
def cache_decorator(secure=False, life_hours=24):
    def decorator(func):
        @wraps(func)
        async def inner_function(*args, **kwargs):
            # заходим в нужные разделы БД
            database = MONGODB_CLIENT[MONGODB_DATABASE]
            collection = database[MONGODB_COLLECTION_CACHE]

            # если есть авторизация, то добавляем ещё в аргументы
            fixed_kwargs = {**kwargs, "credentials": kwargs['credentials'].credentials} if secure else kwargs

            # проверяем делал ли пользователь такой запрос
            # и возвращаем результат если он уже был
            search_result = collection.find_one({"function": func.__name__, "args": fixed_kwargs})
            if search_result:
                return search_result['result']

            # выполняем функцию
            result = await func(*args, **kwargs)

            # сохраняем результат функции
            collection.insert_one({
                "function": func.__name__,
                "args": fixed_kwargs,
                "result": result,
                "time": datetime.datetime.now() + datetime.timedelta(hours=life_hours)
            })
            return result

        return inner_function

    return decorator

################################################################################

# запускает поток для проверки на срок жизни
def thread_cache_lifetime():
    def loop_lifetime():
        database = MONGODB_CLIENT[MONGODB_DATABASE]
        collection = database[MONGODB_COLLECTION_CACHE]
        while True:
            # result = collection.find_one({"time": {'$lt': datetime.datetime.now()}})
            # print(result)
            collection.delete_many({"time": {'$lt': datetime.datetime.now()}})
            time.sleep(1)

    THREAD_CACHE = threading.Thread(target=loop_lifetime, daemon=True)
    THREAD_CACHE.start()
