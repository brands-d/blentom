def deep_dict_update(a, b):
    for k, v in b.items():
        if isinstance(v, dict):
            a[k] = deep_dict_update(a.get(k, {}), v)
        else:
            a[k] = v

    return a
