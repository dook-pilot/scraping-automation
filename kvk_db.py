import pandas
import psycopg2
conn = psycopg2.connect(
    database="vng_db", user="postgres", password="ahsumr", host="127.0.0.1", port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS kvk;
""")
conn.commit()
cursor.execute("""
    create table kvk (
    id serial,
	search_text varchar(255),
	existing_trade_name text,
    partnership_name text,
    chamber_of_commerce text,
    establishment_no varchar(255),
    address text,
    other text,
    primary key (id)
);
""")
conn.commit()
df = pandas.read_csv("kvk_scrapped_data.csv")
for i in range(len(df)):
    insert_query = """
        INSERT INTO kvk (
        search_text, existing_trade_name, partnership_name, chamber_of_commerce, 
        establishment_no, address, other)
        VALUES (%s,%s,%s,%s,%s,%s,%s)
    """
    record_to_insert = (
        df.iloc[i]["search_text"], df.iloc[i]["existing_trade_name"], df.iloc[i]["partnership_name"],
        df.iloc[i]["chamber_of_commerce"], df.iloc[i]["establishment_no"], df.iloc[i]["address"],
        df.iloc[i]["other"])
    cursor.execute(insert_query, record_to_insert)
conn.commit()
conn.close()
