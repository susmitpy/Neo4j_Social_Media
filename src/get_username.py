import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_username(uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.username as `username`
        """
        with driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["username"]


def lambda_handler(event, context):
    
    resp = get_username(
        
        uuid = event['uuid'],
        
        str = event['str'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }