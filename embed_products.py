import json
import pandas as pd
import mysql.connector
from sklearn.feature_extraction.text import TfidfVectorizer

# Load CSV
df = pd.read_csv("products.csv")

# Generate embeddings
vectorizer = TfidfVectorizer(stop_words="english")
vectors = vectorizer.fit_transform(df["product_name"])

# MySQL connection
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="products_db"
)
cursor = conn.cursor()

insert_query = """
INSERT INTO products_vectors (product_id, product_name, vector)
VALUES (%s, %s, %s)
"""

for i, row in df.iterrows():
    vector = vectors[i].toarray()[0].tolist()
    cursor.execute(
        insert_query,
        (int(row["product_id"]), row["product_name"], json.dumps(vector))
    )

conn.commit()
cursor.close()
conn.close()

print("Embeddings stored in MySQL")
