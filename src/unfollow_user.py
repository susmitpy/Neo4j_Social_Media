import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def unfollow_user(follower_uuid: str, followee_uuid: str):
        query = """
            MATCH (follower:User {uuid: $follower_uuid})
            MATCH (followee:User {uuid: $followee_uuid})
            SET follower.following_count = follower.following_count - 1, followee.followers_count = followee.followers_count - 1
            WITH follower, followee
            MATCH (follower) - [f:FOLLOWS] -> (followee)
            DELETE f
        """
        with driver.session() as session:
            session.run(query, follower_uuid=follower_uuid, followee_uuid=followee_uuid)


def lambda_handler(event, context):
    
    resp = unfollow_user(
        
        follower_uuid = event['follower_uuid'],
        
        followee_uuid = event['followee_uuid'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }