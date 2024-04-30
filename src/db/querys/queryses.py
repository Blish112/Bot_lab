from sqlalchemy.exc import SQLAlchemyError 

from ..model import ansyc_ssesion

# using scalars to get
async def get_scalars(stmt):
    async with ansyc_ssesion() as session:
        try:
            result = await session.scalars(stmt)
            return result
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()

# using scalar to get
async def get_scalar(stmt):
    async with ansyc_ssesion() as session:
        try:
            result = await session.scalar(stmt)
            return result
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()

# inser data to DB
async def insert_data(stmt):
    async with ansyc_ssesion() as session:
        try:
            async with session.begin():
                session.add(stmt)
                await session.flush()
                await session.refresh(stmt)
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()

# del data from DB
async def del_data(stmt):
    async with ansyc_ssesion() as session:
        try:
            async with session.begin():
                await session.delete(stmt)
                await session.commit()
        except SQLAlchemyError as e:
            error = str(e.__cause__)
            await session.rollback()
            raise RuntimeError(error) from e
        finally:
            await session.close()