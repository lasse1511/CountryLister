from clickhouse_driver import Client
import requests
import pandas as pd

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
                    id Int16 NOT NULL,
                    name String NOT NULL,
                    alpha3Code String NOT NULL,
                    PRIMARY KEY(id)
                ) 
            ENGINE = MergeTree;
            """)

    # inserts seed data in ClickHouse db
    def executeSeeding(self):
        rows_countries = self.client.execute("SELECT COUNT(*) FROM countries")
        if(rows_countries[0][0] == 0):
            # country api endpoint
            URL = "https://restcountries.eu/rest/v2/all"

            # getting json object (name and alpha3Code) with list of all countries
            countries_df = pd.DataFrame.from_records(requests.get(url=URL).json()).filter(["name", "alpha3Code"], axis=1)

            # Adds id column equal to element index
            countries_df["id"] = countries_df.index + 1
            # Inserts values into database
            self.client.execute("INSERT INTO countries (name, alpha3Code, id) VALUES", countries_df.to_dict('records'))
