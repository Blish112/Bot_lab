from typing import Union
from sqlalchemy import select

from ..model import User, Group
from .group_query import get_group
from .queryses import get_scalar, insert_data, del_data

# insert new user
async def insert_user(user: User) -> None:
    await insert_data(user)

# del user from DB
async def del_user(user_id: int) -> None:
    user = await get_user(user_id=user_id)
    if user is not None:
        await del_data(user)

#----------------------------------GETS----------------------------------#

# get user from DB by tg_id
async def get_user(user_id: int) -> User:
    result = await get_scalar(select(User).where(User.tg_id == user_id))
    return result
            
# get user's is_accept
async def get_user_is_accept(user_id: int) -> bool:
    user: User = await get_user(user_id)
    if user is not None:
        return user.is_accept
    return 0

# get user's is_baned
async def get_user_is_baned(user_id: int) -> bool:
    user: User = await get_user(user_id)
    if user is not None:
        return user.is_baned
    return 0     
            
# get user's group
async def get_user_group(user_id: int) -> Union[str, None]:
    user: User = await get_user(user_id)
    if user is not None:
        result = await get_scalar(select(Group).where(Group.id == user.id_group))
        return result
    
# get try_to_acept 
async def get_user_try_to_acept(user_id: int) -> int:
    user: User = await get_user(user_id)
    if user is not None:
        return user.try_to_accept
    
# get fullname 
async def get_user_fullname(user_id: int) -> Union[str, None]:
    user: User = await get_user(user_id)
    if user is not None:
        return user.fullname
    return None
    
# get first_name 
async def get_user_first_name(user_id: int) -> Union[str, None]:
    user: User = await get_user(user_id)
    if user is not None:
        return user.first_name
    return None
    
#----------------------------------UPDS----------------------------------#

# update user's group  
async def upd_user_group(user_id: int, group_name: str) -> None:
    user: User = await get_user(user_id)
    group: Group = await get_group(group_name)
    if user is not None and group is not None:
        user.id_group = group.id
        await insert_user(user)
    
# update user's is_accept  
async def upd_user_is_accept(user_id: int, is_accept: bool) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.is_accept = is_accept
        await insert_user(user)
            
# update user's is_baned  
async def upd_user_is_baned(user_id: int, is_baned: bool) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.is_baned = is_baned
        await insert_user(user)
            
# update try_to_acept  
async def upd_user_try_to_acept(user_id: int, try_to_accept:int) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.try_to_accept = try_to_accept
        await insert_user(user)
     
# update data using  
async def upd_user_data_using(user_id: int, time) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.upd_date = time
        await insert_user(user)
        
# update fullname  
async def upd_user_fullname(user_id: int, fullname: str) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.fullname = fullname
        await insert_user(user)

# update first_name  
async def upd_user_first_name(user_id: int, first_name: str) -> None:
    user: User = await get_user(user_id)
    if user is not None:
        user.first_name = first_name
        await insert_user(user)
