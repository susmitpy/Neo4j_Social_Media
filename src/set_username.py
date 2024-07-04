import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def set_username(uuid: str, username: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.username = $username
        """
        with driver.session() as session:
            session.run(query, uuid=uuid, username=username).data()


def lambda_handler(event, context):
    
    resp = set_username(
        
        uuid = event['uuid'],
        
        username = event['username'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }