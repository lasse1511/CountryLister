import argparse as ap
import pandas as pd
import databaseManagerORM as dbORM
import prettytable
from io import StringIO
import pycountry
import click 

from models.countries import Countries

# Passing command line arguments
@click.command()
@click.option("--sort-order", help="The sort order of the list of countries.")
def main(sort_order):
    # Checks the value of sort_order in order to avoid malicious attempts
    if (sort_order == None):
        sort_order = input("No sort order specified. Please enter a sort order (valid option are (CI): \"asc\" or \"desc\"): ")
    sort_order = sort_order.lower()
    if (not sort_order in ['asc', 'desc']):
        raise ValueError("Please enter a valid value for sort_order. Valid option are (CI): \"asc\" or \"desc\"")
    elif (sort_order == 'asc'):
        sort_order = ''
    else:
        sort_order = '-'
        
    # Connection, migration and seeding to db
    dbManager = dbORM.databaseManagerORM()

    # Select data from table countries and load into pandas dataframe
    queryRows = []
    for row in Countries.objects_in(dbManager.db).order_by(sort_order + 'name'):
        queryRows.append([row.name, row.alpha3Code])
    countries_df = pd.DataFrame.from_records(queryRows)

    #Convert column ISO3 to ISO2 format
    countries_df[1] = countries_df[1].apply(convert_ISO3_to_ISO2)

    # Renaming column of df to fit the description
    countries_df = countries_df.rename(columns = {0: 'Country name', 1: 'ISO2'}, inplace = False)

    # Print the results using PrettyTable
    output = StringIO()
    countries_df.to_csv(output)
    output.seek(0)
    pt = prettytable.from_csv(output)
    print(pt)

def convert_ISO3_to_ISO2(iso3_code):
    try:
        return pycountry.countries.get(alpha_3=iso3_code).alpha_2
    except:
        return "--"


if __name__ == "__main__": 
    main()