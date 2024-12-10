from functools import lru_cache
from database.config import db_config, engine_config
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

get_engine = lru_cache(lambda:
    create_engine(
        url = str(db_config()),
        **engine_config
    )
)
get_session = lru_cache(lambda: sessionmaker(
    bind       = get_engine(),
    autocommit = False,
    autoflush  = False,
))

def get_db():
    db: Session = get_session()
    db.expire_on_commit = True

    try:
        yield db

    except GeneratorExit:
        db.close()

        raise
    except Exception:
        db.rollback()

        raise
    except:
        db.rollback()

        raise
    else:
        db.commit()
        db.close()
