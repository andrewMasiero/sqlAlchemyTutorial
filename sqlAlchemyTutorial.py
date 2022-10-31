from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy import create_engine

data = [{"x": x, "y": x + 1} for x in range(0, 20, 2)]
engine = create_engine("sqlite+pysqlite:///:memory:", echo=True)
with engine.connect() as conn:
    conn.execute(text("CREATE TABLE some_table (x int, y int)"))
    conn.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        data
    )
    conn.commit()


with Session(engine) as session:
    result = session.execute(
        text("INSERT INTO some_table (x, y) VALUES (:x, :y)"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()


stmt = text("SELECT x, y FROM some_table WHERE y > :y ORDER BY x, y")
with Session(engine) as session:
    result = session.execute(stmt, {"y": 6})
    for row in result:
        print(f"x: {row.x}  y: {row.y}")

with Session(engine) as session:
    result = session.execute(
        text("UPDATE some_table SET y=:y WHERE x=:x"),
        [{"x": 9, "y": 11}, {"x": 13, "y": 15}],
    )
    session.commit()
