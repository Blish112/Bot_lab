from typing import Union

from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError 

from ..model import Class
from .queryses import get_scalars

# get classes by weekday and num_group
async def get_classes(weekday: int, num_group: int) -> Union[Class, None]:
    result = await get_scalars(
        select(Class)
        .where(Class.weekday == weekday & Class.id_group == num_group)
    )
    return result

# TODO: переписать на другой вид запросов    
# get classes by weekday and num_group for chec
async def get_classes_chec(weekday: int, num_group: int) -> Union[Class, None]:
    result = await get_scalars(
        select(Class)
        .where(Class.weekday == weekday)
        .where(Class.id_group == num_group)
        .where(Class.numerator == True)
    )
    return result

# TODO: переписать на другой вид запросов    
# get classes by weekday and num_group for num
async def get_classes_znam(weekday: int, num_group: int) -> Union[Class, None]:
    result = await get_scalars(
        select(Class)
        .where(Class.weekday == weekday)
        .where(Class.id_group == num_group)
        .where(Class.numerator == False)
    )
    return result