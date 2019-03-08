from six.moves.urllib.parse import urljoin, urlencode
from scrapy.http.request import Request
from scrapy.utils.python import to_bytes, is_listlike
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


def _urlencode(seq, enc):
    values = [(to_bytes(k, enc), to_bytes(v, enc))
              for k, vs in seq
              for v in (vs if is_listlike(vs) else [vs])]
    return urlencode(values, doseq=True)


def make_request(url, method='GET', formdata=None, jsondata=None, headers=None, **kwargs):
    if formdata:
        return FormRequest(url=url, method=method, formdata=formdata, headers=headers, **kwargs)
    elif jsondata:
        return JsonRequest(url=url, method=method, jsondata=jsondata, headers=headers, **kwargs)
    else:
        return Request(url, method=method, headers=headers, **kwargs)
