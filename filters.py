def to_lua(obj):
    def __to_lua(obj1, depth):
        new_line = '\n' + '  ' * depth
        if isinstance(obj1, str):
            return f'"{obj1}"'
        elif isinstance(obj1, bool):
            return str(obj1).lower()
        elif isinstance(obj1, list):
            lua_items = [
                __to_lua(item, depth + 1) for item in obj1
            ]
            return ('{' +
                    f'{new_line}  ' +
                    (f",{new_line}  ".join(lua_items)) +
                    new_line + "}")
        elif isinstance(obj1, dict):
            lua_items = [
                f'["{key}"] = {__to_lua(value, depth + 1)}'
                for key, value in obj1.items()
            ]
            return ('{' +
                    f'{new_line}  ' +
                    (f",{new_line}  ".join(lua_items)) +
                    new_line + "}")
        else:
            return str(obj1)

    return __to_lua(obj, 0)


def slugify(value):
    return str(value).lower().replace(" ", "_")


def add_req(reqs, rtype, name, rrange, present=None, survives=None, quiet=None):
    _req = {"type": rtype, "name": name, "range": rrange}
    if present is not None:
        _req["present"] = present
    if survives is not None:
        _req["survives"] = present
    if quiet is not None:
        _req["quiet"] = present
    reqs.append(_req)
    return reqs
