import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def set_profile_pic_url(uuid: str, profile_pic_url: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.profile_pic_url = $profile_pic_url
        """
        with driver.session() as session:
            session.run(query, uuid=uuid, profile_pic_url=profile_pic_url).data()


def lambda_handler(event, context):
    
    resp = set_profile_pic_url(
        
        uuid = event['uuid'],
        
        profile_pic_url = event['profile_pic_url'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }