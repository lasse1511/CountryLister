from infi.clickhouse_orm import Database, Model, UInt16Field, StringField, MergeTree, F
import pandas as pd
import requests
import math 

class Countries(Model):

    id = UInt16Field()
    name = StringField()
    alpha3Code = StringField()

    engine = MergeTree(order_by=('id',), partition_key=('id',), primary_key=('id',))

    def seed(self, db):
        countries = Countries.objects_in(db)
        if(countries.count() == 0):
            # country api endpoint
            URL = "https://restcountries.eu/rest/v2/all"
            
            # getting json object (name and alpha3Code) with list of all countries
            countries_df = pd.DataFrame.from_records(requests.get(url=URL).json()).filter(["name", "alpha3Code"], axis=1)
            
            # Adds id column equal to element index
            countries_df["id"] = countries_df.index + 1
            
            # Split country list into batches of 50 and inserts batch wise // Might be fixed by turning the maximum allowed partiions up, but this might affect performance
            for i in range(math.ceil(len(countries_df)/50)):
                countries_df_partial = countries_df[i*50:(i+1)*50]
                db.insert([
                    Countries(id=id, name=name, alpha3Code=alpha3Code)
                    for name, alpha3Code, id in countries_df_partial.values
                ])

