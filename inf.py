from config import Config

from users.user_inf import UserInf

import datetime
from neo4j import BoltDriver, GraphDatabase


class Inf:
    def __init__(self) -> None:

        self.driver: BoltDriver = GraphDatabase.driver(
            Config.conn.URI, auth=(Config.conn.USERNAME, Config.conn.PASSWORD)
        )
        self.user_inf = UserInf(self.driver)


if __name__ == "__main__":
    inf = Inf()
    # Delete existing users
    inf.user_inf.delete_user(uuid="123")
    inf.user_inf.delete_user(uuid="456")

    # Create Susmit
    inf.user_inf.create_user(
        uuid="123",
        full_name="Susmit",
        created_at=datetime.datetime(2021, 12, 17, 14, 26, 30),
        updated_at=datetime.datetime(2021, 12, 17, 14, 26, 30),
        date_of_birth=datetime.date(2000, 1, 3),
    )

    # Create Rounak
    inf.user_inf.create_user(
        uuid="456",
        full_name="Rounak",
        created_at=datetime.datetime(2021, 12, 17, 14, 26, 30),
        updated_at=datetime.datetime(2021, 12, 17, 14, 26, 30),
        date_of_birth=datetime.date(2000, 1, 1),
    )

    # Whether Susmit follows Rounak
    print(inf.user_inf.is_following("123", "456"))

    # Susmit follows Rounak
    inf.user_inf.follow_user("123", "456", datetime.datetime(2021, 12, 10, 14, 26, 30))

    # Whether Susmit follows Rounak
    print(inf.user_inf.is_following("123", "456"))

    print("Followers of Rounak: ", end="")
    print(inf.user_inf.get_followers("456"))

    # Unfollow Rounak
    inf.user_inf.unfollow_user("123", "456")
    print(inf.user_inf.get_followers("456"))

    print("Profile pic of Susmit: ", end="")
    print(inf.user_inf.get_profile_pic_url("123"))

    inf.user_inf.set_profile_pic_url("123", "this is a profile pic url")

    print("Profile pic of Susmit: ", end="")
    print(inf.user_inf.get_profile_pic_url("123"))

    inf.driver.close()
