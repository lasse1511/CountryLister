from infi.clickhouse_orm import Database, Model, Int8Field, StringField, DateTimeField, F, CollapsingMergeTree
import pandas as pd
import requests
import math 
import uuid

class Countries(Model):

    id = StringField()
    name = StringField()
    alpha3Code = StringField()
    sign = Int8Field(default=-1)
    created = DateTimeField(default=F.now())

    engine = CollapsingMergeTree('created', ('id',), 'sign')

    def seed(self, db):
        countries = Countries.objects_in(db)
        if(countries.count() == 0):
            # Country api endpoint
            URL = "https://restcountries.eu/rest/v2/all"
            
            # Getting json object (name and alpha3Code) with list of all countries
            countries_df = pd.DataFrame.from_records(requests.get(url=URL).json()).filter(["name", "alpha3Code"], axis=1)      

            # Split country list into batches of 50 and inserts batch wise // Might be fixed by turning the maximum allowed partiions up, but this might affect performance
            for i in range(math.ceil(len(countries_df)/50)):
                countries_df_partial = countries_df[i*50:(i+1)*50]
                db.insert([
                    # Generates UUID from country name and alpha3Code to ensure each country has unique identifier 
                    # Duplicate UUIDs are deleted async after insertion
                    Countries(id=str(uuid.uuid3(uuid.NAMESPACE_DNS, name+"##"+alpha3Code)), name=name, alpha3Code=alpha3Code)
                    for name, alpha3Code in countries_df_partial.values
                ])          