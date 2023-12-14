import logging
from typing import List, Tuple, Union

from telethon import TelegramClient
from telethon.hints import Entity
from telethon.tl.functions.channels import GetFullChannelRequest
from telethon.tl.functions.messages import GetHistoryRequest
from telethon.tl.types import User, Channel, Message, Dialog
from tqdm.auto import tqdm

log = logging.getLogger(__name__)


class TgGetUsers:
    def __init__(self, username, api_id, api_hash):
        self.username = username
        self.api_id = api_id
        self.api_hash = api_hash

        # https://github.com/LonamiWebs/Telethon/issues/4051#issuecomment-1491747149
        self.client = TelegramClient(username, api_id, api_hash, system_version="4.16.30-vxVLIVASHKIN")

    async def start(self):
        await self.client.start()

    async def get_my_dialogs(self) -> List[Dialog]:
        dialogs = await self.client.get_dialogs()
        return dialogs

    async def get_participants(self, entity: Union[Entity, str]) -> List[User]:
        user_list = await self.client.get_participants(entity=entity)
        return user_list

    async def get_chat_messages(self, channel_url: str) -> List[Message]:
        # https://github.com/amiryousefi/telegram-analysis/blob/master/ChannelMessages.py

        channel = await self.client.get_entity(channel_url)

        offset_id = 0
        limit = 100
        all_messages = []
        total_messages = 0
        total_count_limit = 0

        while True:
            log.info("Current Offset ID is:", offset_id, "; Total Messages:", total_messages)
            history = await self.client(
                GetHistoryRequest(
                    peer=channel,
                    offset_id=offset_id,
                    offset_date=None,
                    add_offset=0,
                    limit=limit,
                    max_id=0,
                    min_id=0,
                    hash=0,
                )
            )
            if not history.messages:
                break
            messages = history.messages
            for message in messages:
                all_messages.append(message)
            offset_id = messages[len(messages) - 1].id
            total_messages = len(all_messages)
            if total_count_limit != 0 and total_messages >= total_count_limit:
                break

        return all_messages

    async def get_users_of_messages(self, messages: List[Message]) -> Tuple[List[User], List[Channel]]:
        user_ids = set()
        channel_ids = set()
        for message in messages:
            if hasattr(message.from_id, "user_id"):
                user_id = message.from_id.user_id
                user_ids.add(user_id)
            elif hasattr(message.from_id, "channel_id"):
                channel_id = message.from_id.channel_id
                channel_ids.add(channel_id)
            else:
                log.info(f"Skip: {message.from_id}")

        users = []
        for user_id in tqdm(user_ids, "Users info"):
            try:
                user = await self.client.get_entity(user_id)
                users.append(user)
            except Exception as e:
                log.info(f"User {user_id}: {e}")

        channels = []
        for channel_id in tqdm(channel_ids, desc="Channels info"):
            try:
                channel = await self.client(GetFullChannelRequest(channel_id))
                channels.append(channel)
            except Exception as e:
                log.info(f"Channel {channel_id}: {e}")

        return users, channels
