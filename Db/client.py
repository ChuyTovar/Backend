from pymongo import MongoClient

#!Base de datos local
#db_client = MongoClient().local

#!Base de datos en la nube
db_client = MongoClient("mongodb+srv://test:test@cluster0.ingrqvf.mongodb.net/?appName=Cluster0").test