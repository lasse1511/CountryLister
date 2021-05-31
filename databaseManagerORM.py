from infi.clickhouse_orm import Database, Model, UInt16Field, StringField, MergeTree, F

from models.countries import Countries

class databaseManagerORM:
    def __init__(self):
        #Connects to db
        self.db =  Database('localhost', db_url='http://localhost:8123')
        
        # Migrates schema for models to db
        self.db.create_table(Countries)

        # Populate tables
        self.seed(self.db)

    # Executes seed function from models
    def seed(self, db):
        Countries.seed(Countries, self.db)