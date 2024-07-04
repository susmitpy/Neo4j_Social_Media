import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_num_followers(uuid: str) -> int:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN u.followers_count as `count`
        """
        with driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["count"]


def lambda_handler(event, context):
    
    resp = get_num_followers(
        
        uuid = event['uuid'],
        
        int = event['int'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }