from dbrm import Engine, transfer_csv

def main():
    # Example usage of the transfer_csv function
    engine = Engine.from_env()
    transfer_csv(
        csv_file="data/sample_data.csv", 
        table_name="my_table", 
        engine=engine,
        if_exists="replace"
    )
    print("CSV file transferred successfully.")

if __name__ == "__main__":
    main()