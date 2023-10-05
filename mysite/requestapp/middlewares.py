from typing import Any
from django.http import HttpRequest, HttpResponse
from time import time

class UserRequest:

    def __init__(self) -> None:
        self.request_count = 0
        self.request_times = []

    def check_request(self):
        # время последнего запроса
        last_time = time()
        self.request_times.append(last_time) 
        # отсекаем запросы, с которых прошло больше 10 секунд
        self.request_times = [time for time in self.request_times if last_time - time <= 10]
        # кол-во записей - кол-во запросов
        self.request_count = len(self.request_times)
        # если запросов больше или равно 10, значит слишком много запросов
        if self.request_count >= 10:
            return False
        print(f'Запросов: {self.request_count} за последние 10 сек')
        return True

class ThrottlingMiddleware:

    def __init__(self, get_response) -> None:
        self.get_response = get_response
        self.request_count = 0
        self.users_requests = {}

    def __call__(self, request: HttpRequest) -> Any:
        self.request_count += 1
        ip_address = request.META.get("REMOTE_ADDR")
        if ip_address not in self.users_requests:
            self.users_requests[ip_address] = UserRequest()
        if not self.users_requests[ip_address].check_request(): 
            return HttpResponse("Слишком много запросов!!!")
        response = self.get_response(request)
        return response 
    
    def process_exception(self, request: HttpRequest, exception: Exception):
        pass