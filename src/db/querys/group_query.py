from sqlalchemy import select

from ..model import Group
from .queryses import get_scalar, insert_data, del_data

# get user's group id
async def get_group(name_group: str) -> Group:
    result = await get_scalar(
        select(Group)
        .where(Group.name_group == name_group)
    )
    return result

# get user's group id
async def get_group_by_id(id_group: int) -> Group:
    result = await get_scalar(
        select(Group)
        .where(Group.id == id_group)
    )
    return result
            
# insert new group
async def insert_group(group: Group) -> None:
    await insert_data(group)        

# del group from DB
async def del_group(name_group: str) -> None:
    group = await get_group(name_group)
    if group is not None:
        await del_data(group)