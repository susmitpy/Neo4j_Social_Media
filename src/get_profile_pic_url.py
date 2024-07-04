import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_profile_pic_url(uuid: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.uuid = $uuid
            RETURN
                u.profile_pic_url as `profile_pic_url`
        """
        with driver.session() as session:
            data = session.run(query, uuid=uuid).data()
        return data[0]["profile_pic_url"]


def lambda_handler(event, context):
    
    resp = get_profile_pic_url(
        
        uuid = event['uuid'],
        
        str = event['str'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }