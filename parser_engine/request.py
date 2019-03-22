from scrapy.http.request import Request
import json
from scrapy.http.request.form import FormRequest


class JsonRequest(Request):

    def __init__(self, *args, **kwargs):
        jsondata = kwargs.pop('jsondata', None)
        if jsondata and kwargs.get('method') is None:
            kwargs['method'] = 'POST'

        super(JsonRequest, self).__init__(*args, **kwargs)

        if jsondata:
            data = json.dumps(jsondata) if isinstance(jsondata, dict) else jsondata
            if self.method == 'POST':
                self.headers.setdefault(b'Content-Type', b'application/json')
                self._set_body(data)


class TaskRequest(dict):
    def __init__(self, url=None, method='GET', body=None, headers=None, cookies=None, meta=None, **kwargs):
        super().__init__()
        if headers is None:
            headers = {}
        if meta is None:
            meta = kwargs
        self.url = url
        self.method = method
        self.body = body
        self.headers = headers
        self.cookies = cookies
        self.meta = meta

    def __setattr__(self, key, value):
        self[key] = value

    def __getattr__(self, item):
        return self.get(item)


def make_request(url, method='GET', formdata=None, jsondata=None, headers=None, **kwargs):
    if formdata:
        return FormRequest(url=url, method=method, formdata=formdata, headers=headers, **kwargs)
    elif jsondata:
        return JsonRequest(url=url, method=method, jsondata=jsondata, headers=headers, **kwargs)
    else:
        return Request(url, method=method, headers=headers, **kwargs)
