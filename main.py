import dbrm

def main():
    # Example usage of the transfer_csv function
    dbrm.transfer_csv(
        csv_file='data/sample_data.csv',
        table_name='test_table',
        if_exists='replace',
        chunk_size=1000
    )
    print("CSV file transferred successfully.")

if __name__ == "__main__":
    main()