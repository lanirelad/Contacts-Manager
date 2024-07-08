import mysql.connector
from dotenv import load_dotenv
import os
from pymongo import MongoClient


load_dotenv()


# config connection - MySQL configuration
dbConfig = {
    
    'host': os.getenv("DB_HOST"),
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'database': None #  can't be here as the schema may not exist yet!!!   
    
}


# create the MySQL connection
def getDbConnection():
    return mysql.connector.connect(**dbConfig)


# Create the MongoDB connection
def getMongoConnection(var):
    client = MongoClient(var)
    return client.get_database()