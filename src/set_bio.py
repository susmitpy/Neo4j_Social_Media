import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def set_bio(uuid: str, bio: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.bio = $bio
        """
        with driver.session() as session:
            session.run(query, uuid=uuid, bio=bio).data()


def lambda_handler(event, context):
    
    resp = set_bio(
        
        uuid = event['uuid'],
        
        bio = event['bio'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }