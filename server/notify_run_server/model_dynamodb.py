from datetime import datetime
from typing import List

import boto3
import dateutil.parser
from boto3.dynamodb.conditions import Key

from notify_run_server.model import (NoSuchChannel, NotifyModel,
                                     generate_channel_id)
from notify_run_server.params import CHANNEL_TABLE, MESSAGE_TABLE


class DynamodbNotifyModel(NotifyModel):
    def __init__(self):
        dynamodb = boto3.resource('dynamodb')
        self._message_table = dynamodb.Table(MESSAGE_TABLE)
        self._channel_table = dynamodb.Table(CHANNEL_TABLE)

    def register_channel(self, meta: dict) -> str:
        channel_id = generate_channel_id()
        self._channel_table.put_item(Item={
            'channelId': channel_id,
            'created': str(datetime.now()),
            'meta': meta,
            'subscriptions': {},
        })
        return channel_id

    def add_subscription(self, channel_id: str, subscription: dict):
        subscription_id = subscription['id']
        self._channel_table.update_item(
            Key={'channelId': channel_id},
            UpdateExpression='SET #s.#k = :new_sub',
            ExpressionAttributeNames={
                '#s': 'subscriptions',
                '#k': subscription_id,
            },
            ExpressionAttributeValues={
                ':new_sub': subscription['subscription']
            }
        )

    def get_channel(self, channel_id: str):
        result = self._channel_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id)
        )
        if result['Count'] != 1:
            raise NoSuchChannel(channel_id)
        return result['Items'][0]

    def _check_valid_channel(self, channel_id: str) -> bool:
        result = self._channel_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id)
        )
        return result['Count'] > 0

    def _assert_valid_channel(self, channel_id: str):
        if not self._check_valid_channel(channel_id):
            raise NoSuchChannel(channel_id)

    def get_messages(self, channel_id: str) -> List[dict]:
        self._assert_valid_channel(channel_id)
        result = self._message_table.query(
            KeyConditionExpression=Key('channelId').eq(channel_id),
            ScanIndexForward=False,
            Limit=10,
        )
        items = result['Items']
        return [
            {
                'message': item['message'],
                'time': dateutil.parser.parse(item['messageTime']),
                'result': item.get('result', None),
            } for item in items]

    def put_message(self, channel_id: str, message: str, data: dict, result: list):
        self._message_table.put_item(
            Item={
                'channelId': channel_id,
                'messageTime': str(datetime.now()),
                'message': message,
                'data': data,
                'result': result,
            })
