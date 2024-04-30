from sqlalchemy import select

from ..model import Schedule
from .queryses import get_scalar 

# get schedule_by_id
async def get_schedule_by_id(id_schedule: int) -> Schedule:
    result = await get_scalar(
        select(Schedule)
        .where(Schedule.id == id_schedule)
    )
    return result
