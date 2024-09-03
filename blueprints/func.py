from flask import g
import sqlite3, string, random

DATABASE = 'test_database.db'

# SQLite 데이터베이스 연결
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db

# 데이터베이스 연결 종료
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# 쿼리 실행 함수
def query_db(query, args=(), one=False):
    cur = get_db().cursor()
    cur.execute(query, args)
    rv = cur.fetchall()
    cur.close()
    return (rv[0] if rv else None) if one else rv

# 랜덤 문자열 생성 함수
def generate_code(length):
    characters = string.ascii_letters + string.digits
    code = ''.join(random.choice(characters) for _ in range(length))
    return code

# 소수점 두 자리로 포맷, 천 단위 쉼표 사용
def number_format(value):
    return "{:,.2f}".format(value)