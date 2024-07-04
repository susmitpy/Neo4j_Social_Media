from datetime import datetime
from utils import PropertiesDict
from neo4j import BoltDriver
from neo4j.time import DateTime
from .getters import UserGetters
from .setters import UserSetters


class UserInf(UserGetters, UserSetters):
    def __init__(self, driver: BoltDriver) -> None:

        self.driver = driver

    def create_user(self, **kwargs):
        """
        Kwargs:
            uuid (str, optional): [description]. Defaults to None.
            username (str, optional): [description]. Defaults to None.
            full_name (str, optional): [description]. Defaults to None.
            bio (str, optional): [description]. Defaults to None.
            gender (str, optional): [description]. Defaults to None.
            email (str, optional): [description]. Defaults to None.
            date_of_birth (date, optional): [description]. Defaults to None.
            mobile (str, optional): [description]. Defaults to None.
            profile_pic_url (str, optional): [description]. Defaults to None.
            token (str, optional): [description]. Defaults to None.
            created_at (datetime, optional): [description]. Defaults to None.
            updated_at (datetime, optional): [description]. Defaults to None.
            verified (bool, optional): [description]. Defaults to None.
            is_staff (bool, optional): [description]. Defaults to None.
            is_superuser (bool, optional): [description]. Defaults to None.
            coins (int, optional): [description]. Defaults to 0.
            followers_count (int, optional): [description]. Defaults to 0.
            following_count (int, optional): [description]. Defaults to 0.
        """
        user = PropertiesDict({k: v for k, v in kwargs.items() if v is not None})
        query = """
                CREATE (u:User $user)
                """
        with self.driver.session() as session:
            session.run(query, user=user)

        print("User Created")

    def delete_user(self, uuid: str):
        query = """
            MATCH (u:User {uuid: $uuid})
            DETACH DELETE u
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid)

        print("User Deleted")

    def follow_user(self, user_uuid: str, followee_uuid: str, ts: datetime):
        query = """
            MATCH (follower:User {uuid: $user_uuid})
            MATCH (followee:User {uuid: $followee_uuid})
            SET follower.following_count = follower.following_count + 1, followee.followers_count = followee.followers_count + 1
            MERGE (follower) - [f:FOLLOWS {ts:$ts}] -> (followee)
        """
        with self.driver.session() as session:
            session.run(
                query,
                user_uuid=user_uuid,
                followee_uuid=followee_uuid,
                ts=DateTime.from_native(ts),
            )

        print("User Followed")

    def is_following(self, user_uuid: str, test_followee_uuid: str):
        query = """
            MATCH (u:User {uuid: $user_uuid})
            MATCH (o:User {uuid: $test_followee_uuid})
            exists( 
                (u) - [:FOLLOWS] -> (o)
            )
        """
        with self.driver.session() as session:
            data = session.run(
                query, user_uuid=user_uuid, test_followee_uuid=test_followee_uuid
            ).data()
        return list(data[0].values())[0]

    def remove_profile_photo(self, uuid: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            REMOVE u.profile_pic_url
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid)

        print("Profile Photo Removed")

    def unfollow_user(self, follower_uuid: str, followee_uuid: str):
        query = """
            MATCH (follower:User {uuid: $follower_uuid})
            MATCH (followee:User {uuid: $followee_uuid})
            SET follower.following_count = follower.following_count - 1, followee.followers_count = followee.followers_count - 1
            WITH follower, followee
            MATCH (follower) - [f:FOLLOWS] -> (followee)
            DELETE f
        """
        with self.driver.session() as session:
            session.run(query, follower_uuid=follower_uuid, followee_uuid=followee_uuid)

        print("User unfollowed")
