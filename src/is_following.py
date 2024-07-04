import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def is_following(user_uuid: str, test_followee_uuid: str):
        query = """
            MATCH (u:User {uuid: $user_uuid})
            MATCH (o:User {uuid: $test_followee_uuid})
            exists( 
                (u) - [:FOLLOWS] -> (o)
            )
        """
        with driver.session() as session:
            data = session.run(
                query, user_uuid=user_uuid, test_followee_uuid=test_followee_uuid
            ).data()
        return list(data[0].values())[0]


def lambda_handler(event, context):
    
    resp = is_following(
        
        user_uuid = event['user_uuid'],
        
        test_followee_uuid = event['test_followee_uuid'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }