# TgUserScanner

Extracts the usernames of participants from Telegram chats, channels, and DM dialogs.

## Getting started
1. Obtain `api_id` and `api_hash`.

    Go to https://my.telegram.org/apps and register any app there.

2. Install this package
    ```bash
    python3 -m pip install git+https://github.com/vlivashkin/TgUserScanner.git
    ```
    or just
    ```bash
    git clone https://github.com/vlivashkin/TgUserScanner.git
    ```
    it.

3. Examples of usage are in [examples.ipynb](examples.ipynb) notebook.

## Use cases

```python
from tguserscanner import TgUserScanner

client = TgUserScanner(username, api_id, api_hash)
await client.start()
```

### Get users of any channel with access to participants

```python
channel_url = "<channel url>"
channel_users = await client.get_participants(channel_url)
```

### Get users of a chat without access to participants (by messages in chat!)

```python
chat_url = "<chat url>"
chat_messages = await client.get_chat_messages(chat_url)
chat_users, _ = await client.get_users_of_messages(chat_messages)
```

### Get DM users, users of all your chats and channels from dialogs


```python
my_dialogs = await client.get_my_dialogs()
dialog_users, my_channels, my_chats, _ = parse_dialogs(my_dialogs)
```

#### Get users of a chat without URL

```python
chat = find_by_title("<Chat name>", my_chats)
chat_users = await client.get_participants(chat)
```

#### Get users of all your chats and channels

```python
# Chats with your close friends. Leave empty to skip
close_friends_chats = [
    "<chat title>"
]

channels_users = {}
for channel in tqdm(my_channels + my_chats):
    try:
        users = await client.get_participants(channel)
    except Exception as e:
        # print(f"{channel.title}: {e}")
        continue

    for user in users:
        if user.id in channels_users:
            channels_users[user.id].common_channels.append(channel.title)
        else:
            user.common_channels = [channel.title]
            channels_users[user.id] = user

        if channel.title in close_friends_chats:
            channels_users[user.id].has_close_friends_chat = True

channels_users = list(channels_users.values())
```

### Merge all user lists to Pandas DataFrame

```python
columns = ["first_name", "last_name", "username", "phone", "bot"]
closeness_columns = ["common_channels", "has_close_friends_chat"]
columns_with_closeness = columns + closeness_columns

united_users = unite_dfs({
    "all_channels_users": users_to_df(channels_users, custom_fields=closeness_columns)[columns_with_closeness],
    "my_dialogs": users_to_df(dialog_users)[columns],
    "channel_users": users_to_df(channel_users)[columns],
    "chat_users": users_to_df(chat_users)[columns],
})

# Filter out non-related users
united_users_filtered = united_users[
    (united_users["bot"] == False) &
    (
        (united_users["my_dialogs"] == True) |
        (united_users["channel_users"] == True) |
        (united_users["chat_users"] == True)
    )
]

# Export to Excel
united_users_filtered.to_excel("result.xlsx")
```
