import json
from neo4j import BoltDriver, GraphDatabase

class Conn:
    USERNAME = "neo4j"
    PASSWORD = ""
    URI = ""
    
driver = GraphDatabase.driver(
            Conn.URI, auth=(Conn.USERNAME, Conn.PASSWORD)
        )

def lambda_handler(event, context):
    
    query = """
        MATCH (u:User {username: 'adityaraj_singh_'})
        MATCH (o:User)-[f:FOLLOWS]-(u)
        RETURN 
            o.uuid as `uuid`,
            o.username as `username`,
            o.full_name as `full_name`,
            o.profile_pic_url as `profile_pic_url`

    """
    with driver.session() as session:
        data = session.run(query).data()

    return {
        'statusCode': 200,
        'body': json.dumps(data)
    }
