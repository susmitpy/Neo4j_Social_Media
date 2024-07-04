class Conn:
    USERNAME = "neo4j"
    PASSWORD = "neo4"
    URI = "bolt://10.0.1.242:7687"


class Config:
    conn = Conn()
