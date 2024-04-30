from typing import Union
from sqlalchemy import select

from ..model import Numerator
from .queryses import get_scalar, insert_data

# get now numerator
async def get_numerator(id_numerator: int) -> Union[bool, None]:
    result: Numerator = await get_scalar(
        select(Numerator)
        .where(Numerator.id == id_numerator)
    )
    if result is not None:
        return result
    return None
            
# insert new numerator
async def insert_numerator(numerator: Numerator) -> None:
    await insert_data(numerator)
        
# update numerator  
async def upd_numerator(id_numerator: int, value: bool) -> None:
    numerator: Numerator = await get_numerator(id_numerator)
    numerator.what_is_now = value
    await insert_numerator(numerator)