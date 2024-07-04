import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def delete_user(uuid: str):
        query = """
            MATCH (u:User {uuid: $uuid})
            DETACH DELETE u
        """
        with driver.session() as session:
            session.run(query, uuid=uuid)


def lambda_handler(event, context):
    
    resp = delete_user(
        
        uuid = event['uuid'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }