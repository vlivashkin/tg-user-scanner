import json
from typing import List, Tuple, Dict, Optional

import pandas as pd
from telethon.hints import Entity
from telethon.tl.types import User, Dialog, Channel, Chat, ChatForbidden


def parse_dialogs(dialogs: List[Dialog]) -> Tuple[List[User], List[Channel], List[Chat], List[ChatForbidden]]:
    users, channels, chats, chats_forbidden = [], [], [], []
    for dialog in dialogs:
        if isinstance(dialog.entity, User):
            users.append(dialog.entity)
        elif isinstance(dialog.entity, Channel):
            channels.append(dialog.entity)
        elif isinstance(dialog.entity, Chat):
            chats.append(dialog.entity)
        elif isinstance(dialog.entity, ChatForbidden):
            chats_forbidden.append(dialog.entity)
        else:
            print(f"Unknown type: {type(dialog.entity)}")
    return users, channels, chats, chats_forbidden


def find_by_title(title: str, entities: List[Entity]) -> Entity:
    for entity in entities:
        if entity.title == title:
            return entity
    raise FileNotFoundError


def users_to_json(users: List[User], filename: str):
    users = [user.to_dict() for user in users]
    with open(filename, "w") as f:
        json.dump(users, f, default=lambda o: "<not serializable>")


def user_to_dict(user: User, custom_fields: Optional[List]) -> Dict:
    dct = user.to_dict()
    if custom_fields is not None:
        for custom_field in custom_fields:
            if hasattr(user, custom_field):
                dct[custom_field] = user.__dict__[custom_field]
    return dct


def users_to_df(users: List[User], custom_fields: Optional[List] = None) -> pd.DataFrame:
    users = [user_to_dict(user, custom_fields) for user in users]
    users = pd.DataFrame.from_records(users)
    users = users.set_index("id")
    return users


def unite_cells(cells: pd.Series) -> pd.Series:
    if len(cells) == 1:
        return cells

    result_index, result_value = None, None
    for index, value in list(cells.items()):
        result_index = index
        if result_value is None or result_value != result_value:
            result_value = value

    return pd.Series({result_index: result_value})


def unite_dfs(dfs: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    def add_source(df: pd.DataFrame, source: str):
        df[source] = True
        return df

    dfs = [add_source(df, source) for source, df in dfs.items()]
    united = pd.concat(dfs)
    united = united.groupby(united.index).agg(unite_cells).reset_index()
    united = united.set_index("id")
    return united
