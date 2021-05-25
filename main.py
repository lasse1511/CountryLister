import argparse as ap
import pandas as pd
import databaseManager as db
import prettytable
from io import StringIO
import pycountry

def convert_ISO3_to_ISO2(iso3_code):
    print(iso3_code)
    try:
        return pycountry.countries.get(alpha_3=iso3_code).alpha_2
    except:
        return "--"


if __name__ == "__main__":
    # Passing command line arguments
    parser = ap.ArgumentParser(
        description="This app lists countries in specified order")
    parser.add_argument("--sort-order", metavar="S",
                        type=str, help="The sort order", default="asc")
    args = parser.parse_args()

    if (not args.sort_order in ["asc", "desc"]):
        raise Exception("Please specify a valid sort order")
    sort_order = args.sort_order

    # Connection, migration and seeding to db
    dbManager = db.databaseManager()

    # Select data from table countries and load into pandas dataframe
    countries_df = pd.DataFrame.from_records(dbManager.client.execute("""
        SELECT 
            name,
            alpha3Code
        FROM countries
        ORDER BY name """ + sort_order))

    #Convert column ISO3 to ISO2 format
    countries_df[1] = countries_df[1].apply(convert_ISO3_to_ISO2)
    # print(countries_df[1])
    # input("")


    # Renaming column of df to fit the description
    countries_df = countries_df.rename(columns = {0: 'Country name', 1: 'ISO2'}, inplace = False)

    # print(countries_df)
    # Print the results using PrettyTable
    output = StringIO()
    countries_df.to_csv(output)
    output.seek(0)
    pt = prettytable.from_csv(output)
    print(pt)
    # print("OLLLLLEH", args.sort_order)
    # input("WAIT")
