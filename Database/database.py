import sqlite3 as sql


def add_position(latitude: float, longitude: float, connection: sql.Connection) -> None:
    """
    Add a free parking spot coordinate to database.
    """
    with connection:
        connection.execute("INSERT INTO coordinates (latitude, longitude) VALUES (:latitude, :longitude)",
                           {'latitude': latitude, 'longitude': longitude})


def remove_position(latitude: float, longitude: float, connection: sql.Connection, radius: float = 0) -> None:
    """
    Remove a free parking spot coordinate from database. A radius can be specified to remove all coordinates within a
    certain square radius.
    """
    with connection:
        connection.execute("DELETE from coordinates WHERE latitude BETWEEN :latitude_lower AND :latitude_upper AND "
                           "longitude BETWEEN :longitude_lower AND :longitude_upper",
                           {'latitude_lower': latitude - radius, 'latitude_upper': latitude + radius,
                            'longitude_lower': longitude - radius, 'longitude_upper': longitude + radius})


def get_all_positions(cursor: sql.Cursor) -> list:
    """
    Get a list of all free parking positions stored in database.
    """
    cursor.execute("SELECT * FROM coordinates")
    return cursor.fetchall()


def get_positions_in_range(latitude: float, longitude: float, radius: float, cursor: sql.Cursor) -> list:
    """
    Get a list of all free parking positions stored in database that are within a certain square radius.
    """
    cursor.execute("SELECT * FROM coordinates WHERE latitude BETWEEN :latitude_lower AND :latitude_upper AND "
                   "longitude BETWEEN :longitude_lower AND :longitude_upper",
                   {'latitude_lower': latitude - radius, 'latitude_upper': latitude + radius,
                    'longitude_lower': longitude - radius, 'longitude_upper': longitude + radius})
    return cursor.fetchall()


def main():
    conn = sql.connect(':memory:')
    cursor = conn.cursor()
    cursor.execute("""
                    CREATE TABLE IF NOT EXISTS coordinates (
                        latitude REAL NOT NULL,
                        longitude REAL NOT NULL,
                        UNIQUE (latitude, longitude) -- No duplicate coordinates
                    );
                    """)

    conn.close()


if __name__ == "__main__":
    main()
