import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def create_user(**kwargs):
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
        with driver.session() as session:
            session.run(query, user=user)


def lambda_handler(event, context):
    
    resp = create_user(
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }