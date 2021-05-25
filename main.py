import argparse as ap
import pandas as pd
from clickhouse_driver import Client


if __name__ == "__main__":

    # Passing command line arguments
    parser = ap.ArgumentParser(
        description="This app lists countries in specified order")
    parser.add_argument("--sort-order", metavar="S",
                        type=str, help="The sort order", default="asc")
    args = parser.parse_args()

    if (not args.sort_order in ["asc", "desc"]):
        raise Exception("Please specify a valid sort order")

    
    print("OLLLLLEH", args.sort_order)
    input("WAIT")
