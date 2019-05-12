from datetime import datetime
from typing import Any, List

from sqlalchemy import (JSON, Column, DateTime, ForeignKey, Integer, String,
                        create_engine)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.orm.attributes import flag_modified

from notify_run_server.model import (NoSuchChannel, NotifyModel,
                                     generate_channel_id)
from notify_run_server.params import DB_URI

Base = declarative_base()  # type: Any


class Channel(Base):
    __tablename__ = 'channel'

    id = Column(String, primary_key=True)
    created = Column(DateTime)
    meta = Column(JSON)
    subscriptions = Column(JSON)
    messages = relationship('Message')


class Message(Base):
    __tablename__ = 'message'

    id = Column(Integer, primary_key=True)
    channel_id = Column(String, ForeignKey('channel.id'))
    messageTime = Column(DateTime)
    message = Column(String)
    data = Column(JSON)
    result = Column(JSON)

    channel = relationship('Channel', back_populates='messages')


class SqlNotifyModel(NotifyModel):
    def __init__(self):
        engine = create_engine(DB_URI, echo=False)
        Base.metadata.create_all(engine)
        self._sessionmaker = sessionmaker(bind=engine)

    def register_channel(self, meta: dict) -> str:
        session = self._sessionmaker()

        channel = Channel(
            id=generate_channel_id(),
            created=datetime.now(),
            meta=dict(),
            subscriptions=dict(),
        )

        session.add(channel)
        session.commit()
        return channel.id

    def add_subscription(self, channel_id: str, subscription: dict):
        session = self._sessionmaker()

        channel = session.query(Channel).get(channel_id)
        if channel is None:
            raise NoSuchChannel(channel_id)

        channel.subscriptions[subscription['id']
                              ] = subscription['subscription']
        flag_modified(channel, 'subscriptions')
        session.commit()

    def get_channel(self, channel_id: str):
        session = self._sessionmaker()

        channel = session.query(Channel).get(channel_id)
        if channel is None:
            raise NoSuchChannel(channel_id)

        return {
            'channelId': channel.id,
            'created': channel.created,
            'meta': channel.meta,
            'subscriptions': channel.subscriptions,
        }

    def get_messages(self, channel_id: str) -> List[dict]:
        session = self._sessionmaker()
        messages = session.query(Message).filter_by(
            channel_id=channel_id).order_by(Message.messageTime.desc())[:10]
        return [{
            'message': message.message,
            'time': message.messageTime,
            'result': message.result,
        } for message in messages]

    def put_message(self, channel_id: str, message: str, data: dict, result: list):
        session = self._sessionmaker()

        message = Message(
            channel_id=channel_id,
            messageTime=datetime.now(),
            message=message,
            data=data,
            result=result,
        )
        session.add(message)
        session.commit()
