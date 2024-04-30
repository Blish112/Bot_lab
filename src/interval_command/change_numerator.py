from db.querys.numerator_query import get_numerator, upd_numerator

async def change_numerator():
    numerator = await get_numerator(id_numerator=1)
    await upd_numerator(id_numerator=1, value=False if numerator.what_is_now else True)
    