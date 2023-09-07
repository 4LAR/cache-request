
async def test(name: str):
    return "Hello %s" % name
    # return "{ОбщийМодуль.МобильноеУстройство.Модуль(8854)}: Значение не является значением объектного типа (ref)"

async def div(a: int, b: int):
    return {"result": a / b}
