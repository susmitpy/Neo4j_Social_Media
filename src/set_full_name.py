import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def set_full_name(uuid: str, full_name: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            SET
                u.full_name = $full_name
        """
        with driver.session() as session:
            session.run(query, uuid=uuid, full_name=full_name).data()


def lambda_handler(event, context):
    
    resp = set_full_name(
        
        uuid = event['uuid'],
        
        full_name = event['full_name'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }