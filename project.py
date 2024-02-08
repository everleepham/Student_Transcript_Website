import jaydebeapi

def connect(db_driver_path: str, db_url, db_user: str, db_password: str) -> jaydebeapi.Connection:
    conn = jaydebeapi.connect(
        "org.h2.Driver", db_driver_path, db_url, [db_user, db_password])
    return conn



