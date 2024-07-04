import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def remove_profile_photo(uuid: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            REMOVE u.profile_pic_url
        """
        with driver.session() as session:
            session.run(query, uuid=uuid)


def lambda_handler(event, context):
    
    resp = remove_profile_photo(
        
        uuid = event['uuid'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }