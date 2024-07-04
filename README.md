# Neo4j DB for social media app 
DB Migration and Lambda Function Creator

This repository was created to:  
1. Migrate data from mysql database to Neo4j database (`migration.py`)

2. During local development, getters, setters were created in Object Oriented fashion under `users/` directory. When there was a requirement, to shift this functionality to aws lambda, `gen_funcs_files.py` was created which uses a jinja template to generate the individual lambda function files and write to `src/` directory to speed up the process.