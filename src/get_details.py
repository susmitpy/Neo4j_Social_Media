import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_details(uuid: str) -> dict:
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
        with driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]


def lambda_handler(event, context):
    
    resp = get_details(
        
        uuid = event['uuid'],
        
        dict = event['dict'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }