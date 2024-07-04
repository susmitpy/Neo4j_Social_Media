import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def get_uuid_by_email(email: str) -> str:
        query = """
            MATCH (u:User)
            WHERE u.email = $email
            RETURN
                u.uuid as `uuid`
        """
        with driver.session() as session:
            data = session.run(query, email=email).data()
        return data[0]["uuid"]


def lambda_handler(event, context):
    
    resp = get_uuid_by_email(
        
        email = event['email'],
        
        str = event['str'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }