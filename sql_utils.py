from typing import List, Dict

from sqlalchemy import create_engine, select, insert, func, Text, BigInteger, DateTime, ForeignKey
from sqlalchemy.orm import Session, DeclarativeBase, mapped_column, relationship
from config import DB_USER, DB_PASSWORD, DB_HOST, DB_PORT, DB_NAME

engine = create_engine(f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
                       pool_size=20, max_overflow=-1)


class Base(DeclarativeBase):
    pass


class Channel(Base):
    __tablename__ = "channels"

    id = mapped_column(BigInteger, primary_key=True, nullable=False)
    chat_id = mapped_column(BigInteger, unique=True, nullable=False)
    username = mapped_column(Text)
    listed_at = mapped_column(DateTime(timezone=True), default=func.clock_timestamp(), nullable=False)


class Boost(Base):
    __tablename__ = "boosts"

    id = mapped_column(BigInteger, primary_key=True)
    channel_id = mapped_column(BigInteger, ForeignKey("channels.id"), nullable=False)
    check_time = mapped_column(DateTime(timezone=True), default=func.clock_timestamp(), nullable=False)
    boosts_count = mapped_column(BigInteger, default=0, nullable=False)
    level = mapped_column(BigInteger, default=0, nullable=False)
    left_to_level_up = mapped_column(BigInteger, default=0, nullable=False)

    channel = relationship("Channel", backref="boosts")


async def add(model, params: List[Dict]):
    session = Session(engine)

    session.execute(
        insert(model),
        params
    )

    session.commit()


async def get(model, param: str | None, value: int | str | None):
    session = Session(engine)

    match model.__tablename__:
        case "channels":
            match param:
                case "id":
                    param = Channel.id
                case "chat_id":
                    param = Channel.chat_id
                case "username":
                    param = Channel.username

            if param is not None:
                query = select(Channel).where(param == value)
                result = session.execute(query)

                channel = result.scalar()

                return channel
            else:
                query = select(Channel)
                result = session.execute(query)

                return result.scalars()
        case "boosts":
            match param:
                case "channel_id":
                    param = Boost.channel_id

            query = select(Boost).where(param == value).order_by(Boost.check_time.desc())
            result = session.execute(query)

            boosts = result.scalars()

            return boosts
