from neo4j import BoltDriver


class UserSetters:
    def __init__(self, driver: BoltDriver) -> None:

        self.driver = driver

    def set_bio(self, uuid: str, bio: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.bio = $bio
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid, bio=bio).data()

    def set_full_name(self, uuid: str, full_name: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.full_name = $full_name
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid, full_name=full_name).data()

    def set_username(self, uuid: str, username: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.username = $username
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid, username=username).data()

    def set_profile_pic_url(self, uuid: str, profile_pic_url: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.profile_pic_url = $profile_pic_url
        """
        with self.driver.session() as session:
            session.run(query, uuid=uuid, profile_pic_url=profile_pic_url).data()
