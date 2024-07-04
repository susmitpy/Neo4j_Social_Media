import json
import os
from neo4j import GraphDatabase

driver = GraphDatabase.driver(
            os.environ["URI"], auth=(os.environ["USERNAME"], os.environ["PASSWORD"])
        )

def follow_user(user_uuid: str, followee_uuid: str, ts: datetime):
        query = """
            MATCH (follower:User {uuid: $user_uuid})
            MATCH (followee:User {uuid: $followee_uuid})
            SET follower.following_count = follower.following_count + 1, followee.followers_count = followee.followers_count + 1
            MERGE (follower) - [f:FOLLOWS {ts:$ts}] -> (followee)
        """
        with driver.session() as session:
            session.run(
                query,
                user_uuid=user_uuid,
                followee_uuid=followee_uuid,
                ts=DateTime.from_native(ts),
            )


def lambda_handler(event, context):
    
    resp = follow_user(
        
        user_uuid = event['user_uuid'],
        
        followee_uuid = event['followee_uuid'],
        
        ts = event['ts'],
        
    )

    return {
        "statusCode": 200,
        "body": json.dumps(resp),
        "headers": {"content-type": "application/json"},
    }