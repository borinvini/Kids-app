import requests
import json
from kivy.network.urlrequest import UrlRequest
from kivy.app import App
from functools import partial

class ApiClient:
    def __init__(self, base_url="http://localhost:8000/api/"):
        self.base_url = base_url
        self.token = None
        self.headers = {
            'Content-Type': 'application/json',
        }
    
    def set_token(self, token):
        self.token = token
        self.headers['Authorization'] = f'Token {token}'
    
    def login(self, username, password, success_callback, error_callback):
        url = f"{self.base_url}auth/token/"
        data = {
            'username': username,
            'password': password
        }
        
        def on_success(req, result):
            self.token = result['token']
            self.headers['Authorization'] = f'Token {self.token}'
            success_callback(result)
        
        UrlRequest(
            url, 
            req_headers=self.headers,
            req_body=json.dumps(data),
            on_success=on_success,
            on_error=error_callback,
            on_failure=error_callback
        )
    
    def get_child_data(self, child_id, success_callback, error_callback):
        url = f"{self.base_url}children/{child_id}/"
        
        UrlRequest(
            url, 
            req_headers=self.headers,
            on_success=partial(self._handle_response, callback=success_callback),
            on_error=error_callback,
            on_failure=error_callback
        )
    
    def get_tasks(self, child_id, success_callback, error_callback):
        url = f"{self.base_url}tasks/?child_id={child_id}"
        
        UrlRequest(
            url, 
            req_headers=self.headers,
            on_success=partial(self._handle_response, callback=success_callback),
            on_error=error_callback,
            on_failure=error_callback
        )
    
    def update_task(self, task_id, data, success_callback, error_callback):
        url = f"{self.base_url}tasks/{task_id}/"
        
        UrlRequest(
            url, 
            req_headers=self.headers,
            req_body=json.dumps(data),
            method='PATCH',
            on_success=partial(self._handle_response, callback=success_callback),
            on_error=error_callback,
            on_failure=error_callback
        )
    
    def toggle_task_complete(self, task_id, success_callback, error_callback):
        url = f"{self.base_url}tasks/{task_id}/toggle_complete/"
        
        UrlRequest(
            url, 
            req_headers=self.headers,
            method='POST',
            on_success=partial(self._handle_response, callback=success_callback),
            on_error=error_callback,
            on_failure=error_callback
        )
    
    def _handle_response(self, req, result, callback):
        callback(result)