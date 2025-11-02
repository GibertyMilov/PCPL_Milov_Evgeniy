def field(items, *args):
    if not items:
        return

    assert len(args) > 0, "Должен быть передан хотя бы один аргумент"

    if len(args) == 1:
        key = args[0]
        for item in items:
            if isinstance(item, dict) and key in item and item[key] is not None:
                yield item[key]
    else:
        for item in items:
            if not isinstance(item, dict):
                continue

            result = {}
            for key in args:
                if key in item and item[key] is not None:
                    result[key] = item[key]

            if result:
                yield result