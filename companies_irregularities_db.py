import pandas
import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
conn = psycopg2.connect(
    database="vng_db", user="postgres", password="ahsumr", host="127.0.0.1", port="5432"
)
conn.autocommit = True
cursor = conn.cursor()
cursor.execute("""
    DROP TABLE IF EXISTS companies_irregularities;
""")
conn.commit()
cursor.execute("""
    create table companies_irregularities (
    id serial,
	place_api_company_name text,
	bovag_matched_name text,
	bovag_matched_name_score text,
	place_api_address text,
	bovag_matched_address text,
	bovag_matched_address_score text,
	formatted_phone_number text,
	Bovag_Matched_Telephone text,
	Bovag_Matched_Telephone_score text,
	overall_similarity_score text,
	formatted_address text,
	place_id text,
	plus_code text,
	rating text,
	reference text,
	scope text,
	types text,
	user_ratings_total text,
	business_status text,
	geometry text,
    icon text,
    icon_background_color text,
    icon_mask_base_uri text,
    opening_hours text,
    permanently_closed text,
    price_level text,
    photos text,
    kvk_search_text text,
    kvk_tradename text,
    kvk_partnership_name text,
    kvk_chamber_of_commerce text,
    kvk_establishment_no text,
    kvk_Address text,
    kvk_other text,
    Reviews text,
    poitive_reviews text,
    negative_reviews text,
    duplicate_location text,
    irregularities text,
    duplicates_found text,
    Bovag_registered text,
    KVK_found text,
    company_ratings text,
    primary key(id)
);
""")
conn.commit()
df = pandas.read_csv("final_result.csv")
for i in range(len(df)):
    insert_query = """
        INSERT INTO companies_irregularities (
        place_api_company_name, 
        bovag_matched_name, 
        bovag_matched_name_score, 
        place_api_address, 
        bovag_matched_address, 
        bovag_matched_address_score, 
        formatted_phone_number,
        Bovag_Matched_Telephone, 
        Bovag_Matched_Telephone_score, 
        overall_similarity_score, 
        formatted_address, 
        place_id, 
        plus_code, 
        rating, 
        reference, 
        scope, 
        types, 
        user_ratings_total, 
        business_status,
        geometry, 
        icon,
        icon_background_color, 
        icon_mask_base_uri, 
        opening_hours,
        permanently_closed,
        price_level, 
        photos, 
        kvk_search_text, 
        kvk_tradename, 
        kvk_partnership_name,
        kvk_chamber_of_commerce, 
        kvk_establishment_no, 
        kvk_Address, 
        kvk_other,
        Reviews, 
        poitive_reviews, 
        negative_reviews, 
        duplicate_location,
        irregularities, 
        duplicates_found, 
        Bovag_registered,
        KVK_found, 
        company_ratings
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,
        %s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s
        )
    """
    record_to_insert = (
        df.iloc[i]["place_api_company_name"], 
        df.iloc[i]["bovag_matched_name"], 
        df.iloc[i]["bovag_matched_name_score"],
        df.iloc[i]["place_api_address"], 
        df.iloc[i]["bovag_matched_address"], 
        df.iloc[i]["bovag_matched_address_score"],
        df.iloc[i]["formatted_phone_number"],
        df.iloc[i]["Bovag_Matched_Telephone"], 
        df.iloc[i]["Bovag_Matched_Telephone_score"], 
        df.iloc[i]["overall_similarity_score"],
        df.iloc[i]["formatted_address"], 
        df.iloc[i]["place_id"],
        df.iloc[i]["plus_code"],
        df.iloc[i]["rating"], 
        df.iloc[i]["reference"], 
        df.iloc[i]["scope"],
        df.iloc[i]['types'], 
        df.iloc[i]["user_ratings_total"], 
        df.iloc[i]["business_status"],
        df.iloc[i]["geometry"],
        df.iloc[i]["icon"],
        df.iloc[i]["icon_background_color"],
        df.iloc[i]["icon_mask_base_uri"],
        df.iloc[i]["opening_hours"],
        df.iloc[i]["permanently_closed"],
        df.iloc[i]["price_level"],
        df.iloc[i]["photos"],
        df.iloc[i]["kvk_search_text"],
        df.iloc[i]["kvk_tradename"],
        df.iloc[i]["kvk_partnership_name"],
        df.iloc[i]["kvk_chamber_of_commerce"],
        df.iloc[i]["kvk_establishment_no"],
        df.iloc[i]["kvk_Address"],
        df.iloc[i]["kvk_other"],
        df.iloc[i]["Reviews"],
        df.iloc[i]["poitive_reviews"],
        df.iloc[i]["negative_reviews"],
        df.iloc[i]["duplicate_location"],
        df.iloc[i]["irregularities"],
        df.iloc[i]["duplicates_found"],
        df.iloc[i]["Bovag_registered"],
        df.iloc[i]["KVK_found"],
        df.iloc[i]["company_ratings"]
    )
    cursor.execute(insert_query, record_to_insert)
conn.commit()
conn.close()
