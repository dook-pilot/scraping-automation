import pandas
import psycopg2
conn = psycopg2.connect(
    database="vng_db", user="postgres", password="ahsumr", host="127.0.0.1", port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS place_api;
""")
conn.commit()
cursor.execute("""
    create table place_api (
    id serial,
	business_status varchar(50),
	geometry text,
	icon text,
	icon_background_color varchar(20),
	icon_mask_base_uri text,
	name varchar(255),
	opening_hours text,
	photos text,
	place_id varchar(255),
	plus_code text,
	rating float,
	reference varchar(255),
	scope varchar(30),
	types text,
	user_ratings_total varchar(255),
	vicinity text,
	permanently_closed varchar(20),
	price_level varchar(255),
	formatted_phone_number varchar(255),
	formatted_address text,
    primary key(id)
);
""")
conn.commit()
df = pandas.read_csv("place_api_companies.csv")
for i in range(len(df)):
    insert_query = """
        INSERT INTO place_api (
        business_status, geometry, icon, icon_background_color, name, opening_hours, photos,
        place_id, plus_code, rating, reference, scope, types, user_ratings_total, vicinity, 
        permanently_closed, price_level, formatted_phone_number, formatted_address
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """
    record_to_insert = (
        df.iloc[i]["business_status"], df.iloc[i]["geometry"], df.iloc[i]["icon"],
        df.iloc[i]["icon_background_color"], df.iloc[i]["name"], df.iloc[i]["opening_hours"],
        df.iloc[i]["photos"], df.iloc[i]["place_id"], df.iloc[i]["plus_code"],
        df.iloc[i]["rating"], df.iloc[i]["reference"], df.iloc[i]["scope"],
        df.iloc[i]["types"], df.iloc[i]["user_ratings_total"], df.iloc[i]["vicinity"],
        df.iloc[i]['permanently_closed'], df.iloc[i]["price_level"], df.iloc[i]["formatted_phone_number"],
        df.iloc[i]["formatted_address"]
    )
    cursor.execute(insert_query, record_to_insert)
conn.commit()
conn.close()
