def log(data, *msgs, **kwargs):
    print("[parser engine] ", str(data), ' '.join([str(msg) for msg in msgs]), pretty_dict_str(kwargs))


def pretty_dict_str(data):
    return '\n'.join([str(k) + ':\t' + str(v) for k, v in data.items()])
