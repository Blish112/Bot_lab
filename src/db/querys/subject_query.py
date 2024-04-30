from sqlalchemy import select

from ..model import Subject
from .queryses import get_scalar

# get subject
async def get_subject(subject_id: int) -> Subject:
    result = await get_scalar(select(Subject).where(Subject.id == subject_id))
    return result
