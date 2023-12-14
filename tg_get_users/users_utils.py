import json
from typing import List

import pandas as pd
from telethon.tl.types import User


def users_to_json(users: List[User], filename: str):
    users = [user.to_dict() for user in users]
    with open(filename, "w") as f:
        json.dump(users, f, default=lambda o: "<not serializable>")


def users_to_df(users: List[User]) -> pd.DataFrame:
    users = [user.to_dict() for user in users]
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


def unite_df(left: pd.DataFrame, right: pd.DataFrame) -> pd.DataFrame:
    """
    Unites two dataframes of users. Deduplicates by user id and filling empty values from duplicates.
    """
    united = pd.concat((left, right))
    united = united.groupby(united.index).agg(unite_cells).reset_index()
    united = united.set_index("id")
    return united
