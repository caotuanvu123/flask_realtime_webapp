from pymongo import MongoClient

# need change config
client = MongoClient('mongodb://localhost:27017/')
db = client['trading_db']

def save_data_to_mongo(collection_name, data):
    collection = db[collection_name]
    result = collection.insert_many(data) 
    return result
