import os
import psycopg2
from backend.service.database import get_embedding, create_db_connection

# add_test_data.py
# Write five example sentences that will be converted to embeddings
texts = [
    "I like to eat broccoli and bananas.",
    "I ate a banana and spinach smoothie for breakfast.",
    "Chinchillas and kittens are cute.",
    "My sister adopted a kitten yesterday.",
    "Look at this cute hamster munching on a piece of broccoli.",
]

embeddings = get_embedding(texts, os.getenv('EMBEDDING_MODEL'))

# Write text and embeddings to database
connection = create_db_connection()
cursor = connection.cursor()
try:
    for text, embedding in zip(texts, embeddings):
        cursor.execute(
            "INSERT INTO embeddings (embedding, text) VALUES (%s, %s)",
            (embedding, text)
        )
    connection.commit()
except (Exception, psycopg2.Error) as error:
    print("Error while writing to DB", error)
finally:
    if cursor:
        cursor.close()
    if connection:
        connection.close()