import os
from database import get_embedding, create_db_connection

# test_search.py
text = "Did anyone adopt a cat this weekend?"
embedding = get_embedding(text, os.getenv('EMBEDDING_MODEL'))

connection = create_db_connection()
cursor = connection.cursor()
try:
    cursor.execute(f"""
        SELECT text,  1 - (embedding <=> '{embedding}') AS cosine_similarity
        FROM embeddings
        ORDER BY cosine_similarity desc
        LIMIT 3
    """)
    for r in cursor.fetchall():
        print(f"Text: {r[0]}; Similarity: {r[1]}")

except Exception as error:
    print("Error..", error)
finally:
    cursor.close()
    connection.close()