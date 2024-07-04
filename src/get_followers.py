import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_followers(uuid: str):
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            MATCH (o:User)-[f:FOLLOWS]->(u)
            RETURN 
                o.uuid as `uuid`,
                o.username as `username`,
                o.full_name as `full_name`,
                o.profile_pic_url as `profile_pic_url`
        """
        with driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data


def lambda_handler(event, context):
    
    resp = get_followers(
        
        uuid = event['uuid'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }