from contextlib import asynccontextmanager

from app.bd.connection import get_session

@asynccontextmanager
async def session_with_commit(commit=True) :
    session_manager = get_session()
    session = session_manager()
    try:
        yield session
        if commit:
            session.commit()

    except Exception as e:
        session.rollback()
        raise e