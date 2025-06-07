# import sqlite3

# conn = sqlite3.connect("users.db")

# cursor = conn.cursor()


# cursor.execute(
#     """
#     CREATE TABLE IF NOT EXISTS USERS (
#         ID INTEGER PRIMARY KEY  AUTOINCREMENT ,
#         CHAT_ID INTEGER NOT NULL ,
#         MESSAGE_ID INTEGER NOT NULL ,
#         FILE_ID TEXT ,
#         TEXT_USER TEXT ,
#         MESSAGE_TYPE TEXT,
#         COUNT_HEART INTEGER
#     )
#     """
# )

# cursor.execute(
#     """
#     CREATE TABLE proxy (
#         ID INTEGER PRIMARY KEY AUTOINCREMENT ,
#         PROXY TEXT
#     )
#                """
# )

# conn.commit()
# conn.close()
