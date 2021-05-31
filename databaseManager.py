from clickhouse_driver import Client
import requests
import pandas as pd
import uuid

class databaseManager:
    def __init__(self):
        self.client = Client('localhost')
        self.migrateSchema()
        self.executeSeeding()

    # migrates table definitions to ClickHouse db
    def migrateSchema(self):
        current_tables = self.client.execute("SHOW TABLES")
        if(len(current_tables) == 0):
            self.client.execute("""
                CREATE TABLE countries (
                    id String NOT NULL,
                    name String NOT NULL,
                    alpha3Code String NOT NULL,
                    sign Int8 DEFAULT -1,

                    PRIMARY KEY(id)
                ) 
            ENGINE = CollapsingMergeTree(sign);
            """)

    # inserts seed data in ClickHouse db
    def executeSeeding(self):
        rows_countries = self.client.execute("SELECT COUNT(*) FROM countries")
        if(rows_countries[0][0] == 0):
            # country api endpoint
            URL = "https://restcountries.eu/rest/v2/all"

            # getting json object (name and alpha3Code) with list of all countries
            countries_df = pd.DataFrame.from_records(requests.get(
                url=URL).json()).filter(["name", "alpha3Code"], axis=1)

            # Adds UUID as id
            countries_df["id"] = countries_df.apply(self.generateUUID, axis=1) 

            # Inserts values into database
            self.client.execute(
                "INSERT INTO countries (name, alpha3Code, id) VALUES", countries_df.to_dict('records'))


    # Generates UUID from country name and alpha3Code to ensure each country has unique identifier
    def generateUUID(self, inputRow):
        return str(uuid.uuid3(uuid.NAMESPACE_DNS, inputRow["name"] + "##" + inputRow["alpha3Code"]))
