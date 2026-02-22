import os
from psycopg2 import pool
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


class Database:
    def __init__(self):
        self.connection_pool = pool.SimpleConnectionPool(
            minconn=1,
            maxconn=10,
            host=os.getenv("DB_HOST"),
            database=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            port=os.getenv("DB_PORT"),
        )

    def execute(
        self,
        sql,
        *params,
        fetchone=False,
        fetchall=False,
        commit=False
    ):
        connection = self.connection_pool.getconn()
        try:
            with connection.cursor(cursor_factory=RealDictCursor) as cursor:
                cursor.execute(sql, params)

                result = None
                if fetchone:
                    result = cursor.fetchone()
                elif fetchall:
                    result = cursor.fetchall()

                if commit:
                    connection.commit()

                return result

        except Exception as e:
            connection.rollback()
            print("Database error:", e)
            raise e

        finally:
            self.connection_pool.putconn(connection)



    def create_tables(self):
        users_table = """
        CREATE TABLE IF NOT EXISTS users(
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT UNIQUE
        );
        """

        saved_quotes_table = """
        CREATE TABLE IF NOT EXISTS saved_quotes(
            id SERIAL PRIMARY KEY,
            telegram_id BIGINT,
            quote TEXT,
            author VARCHAR(255),
            UNIQUE(telegram_id, quote)
        );
        """

        index_query = """
        CREATE INDEX IF NOT EXISTS idx_saved_quotes_telegram_id
        ON saved_quotes(telegram_id);
        """

        self.execute(users_table, commit=True)
        self.execute(saved_quotes_table, commit=True)
        self.execute(index_query, commit=True)

    # -----------------------
    # USERS
    # -----------------------

    def add_user(self, telegram_id):
        sql = """
        INSERT INTO users (telegram_id)
        VALUES (%s)
        ON CONFLICT (telegram_id) DO NOTHING;
        """
        self.execute(sql, telegram_id, commit=True)

    # -----------------------
    # SAVED QUOTES
    # -----------------------

    def save_quote(self, telegram_id, quote, author):
        sql = """
        INSERT INTO saved_quotes (telegram_id, quote, author)
        VALUES (%s, %s, %s)
        ON CONFLICT (telegram_id, quote) DO NOTHING;
        """
        self.execute(sql, telegram_id, quote, author, commit=True)

    def get_saved_quotes(self, telegram_id):
        sql = """
        SELECT quote, author
        FROM saved_quotes
        WHERE telegram_id = %s
        ORDER BY id DESC;
        """
        return self.execute(sql, telegram_id, fetchall=True)