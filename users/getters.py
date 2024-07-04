from neo4j import BoltDriver


class UserGetters:
    def __init__(self, driver: BoltDriver) -> None:

        self.driver = driver

    def get_related_users(self, uuid: str) -> list:
        """Users that are interested in the same interests as the user
        (WIP)
        """
        query = """
            MATCH (u:User) 
            WHERE u.uuid != $uuid
            RETURN
                o.uuid as `uuid`,
                o.username as `username`,
                o.full_name as `full_name`,
                o.profile_pic_url as `profile_pic_url`
            LIMIT 5
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data

    def get_followers(self, uuid: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            MATCH (o:User)-[f:FOLLOWS]->(u)
            RETURN 
                o.uuid as `uuid`,
                o.username as `username`,
                o.full_name as `full_name`,
                o.profile_pic_url as `profile_pic_url`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data

    def get_following(self, uuid: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            MATCH (o:User)<-[f:FOLLOWS]-(u)
            RETURN
                o.uuid as `uuid`,
                o.username as `username`,
                o.full_name as `full_name`,
                o.profile_pic_url as `profile_pic_url`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data

    def get_num_followers(self, uuid: str) -> int:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN u.followers_count as `count`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["count"]

    def get_num_following(self, uuid: str) -> int:
        query = f"""
            MATCH (u:User)
            WHERE u.uuid = $uuid
            LIMIT             RETURN u.following_count as `count`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["count"]

    def get_uuid_by_email(self, email: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.email = $email
            RETURN
                u.uuid as `uuid`
        """
        with self.driver.session() as session:
            data = session.run(query, email=email).data()
        return data[0]["uuid"]

    def get_uuid_by_mobile(self, mobile: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.mobile = $mobile
            RETURN
                u.uuid as `uuid`
        """
        with self.driver.session() as session:
            data = session.run(query, mobile=mobile).data()
        return data[0]["uuid"]

    def get_bio(self, uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.bio as `bio`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["bio"]

    def get_full_name(self, uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.full_name as `full_name`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["full_name"]

    def get_profile_pic_url(self, uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.profile_pic_url as `profile_pic_url`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["profile_pic_url"]

    def get_username(self, uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.username as `username`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["username"]

    def get_details(self, uuid: str) -> dict:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.uuid as `uuid`,
                u.username as `username`,
                u.full_name as `full_name`,
                u.profile_pic_url as `profile_pic_url`,
                u.bio as `bio`,
                u.followers_count as `followers_count`,
                u.following_count as `following_count`
        """
        with self.driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]
