import sqlalchemy
from sqlalchemy import create_engine, text

# SQLite 데이터베이스 파일 설정
DATABASE_URL = "sqlite:///test_database.db"
engine = create_engine(DATABASE_URL)

# 데이터베이스 연결 및 작업 실행
with engine.connect() as conn:
    # 트랜잭션 시작
    trans = conn.begin()
    
    try:
        # 기존 products 테이블 이름 변경
        conn.execute(text("ALTER TABLE products RENAME TO products_old;"))

        # 새로운 products 테이블 생성
        conn.execute(text("""
            CREATE TABLE products (
                id INTEGER PRIMARY KEY,
                name TEXT NOT NULL,
                color TEXT NOT NULL,
                code TEXT NOT NULL,
                bud_type TEXT
            );
        """))

        # 트랜잭션 커밋
        trans.commit()

    except Exception as e:
        # 에러 발생 시 롤백
        trans.rollback()
        print(f"An error occurred: {e}")