from app.database.session import check_database_connection, get_db

def test_database_connection_ping():
    assert check_database_connection() is True

def test_database_session_generator():
    db_gen = get_db()
    db = next(db_gen)
    assert db is not None
    try:
        next(db_gen)
    except StopIteration:
        pass
