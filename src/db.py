from sqlalchemy import create_engine, Column, String, Boolean
from sqlalchemy.orm import declarative_base, sessionmaker

DATABASE_URL = "sqlite:///./users.db"

engine = create_engine(
    DATABASE_URL, connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    email = Column(String, primary_key=True, index=True)
    password_hash = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)


def init_db():
    Base.metadata.create_all(bind=engine)
