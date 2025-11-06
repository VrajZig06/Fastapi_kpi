from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# SQLALCHEMY_DATABASE_URL = f"postgresql://<username>:<password>@<ip-address/hostname>/<database_name>"

QA_DB_URL = "postgresql://postgres:ztlab141@localhost/fastapi_kpi"

engine = create_engine(QA_DB_URL)

SessionLocal = sessionmaker(autoflush=False,autocommit=False,bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()  # ✅ always close, even if there was an error
