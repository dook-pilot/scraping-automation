import pandas
import psycopg2
conn = psycopg2.connect(
    database="vng_db", user="postgres", password="ahsumr", host="127.0.0.1", port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS bovag;
""")
conn.commit()
cursor.execute("""
    create table bovag (
    id serial,
	company_name varchar(255),
	street_address text,
    city_address text,
    telephone varchar(255),
    email varchar(255),
    websiteurl varchar(255),
    ul text,
    tags text,
    primary key (id)
);
""")
conn.commit()
df = pandas.read_csv("bovag_dataset.csv")
for i in range(len(df)):
    insert_query = """
        INSERT INTO bovag (
        company_name, street_address, city_address, telephone, email, websiteurl, ul,
        tags)
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
    """
    record_to_insert = (
        df.iloc[i]["company_name"], df.iloc[i]["Street_Address"], df.iloc[i]["City_Address"],
        df.iloc[i]["Telephone"], df.iloc[i]["email"], df.iloc[i]["websiteurl"],
        df.iloc[i]["ul"], df.iloc[i]["tags"])
    cursor.execute(insert_query, record_to_insert)
conn.commit()
conn.close()
