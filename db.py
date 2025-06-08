import sqlite3
from pathlib import Path

DB_PATH = Path("sqlite3.db")


def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()

    # 사용자 클릭 수 저장
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_clicks (
        user_uuid TEXT PRIMARY KEY,
        click_count INTEGER DEFAULT 0,
        nickname TEXT
    )
    """)

    # 사용자 인벤토리 이미지 저장
    c.execute("""
    CREATE TABLE IF NOT EXISTS user_inventory (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_uuid TEXT,
        image_id TEXT,
        UNIQUE(user_uuid, image_id)
    )
    """)

    conn.commit()
    conn.close()


def add_clicks(user_uuid, count):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        INSERT INTO user_clicks (user_uuid, click_count)
        VALUES (?, ?)
        ON CONFLICT(user_uuid) DO UPDATE SET click_count = click_count + excluded.click_count
    """, (user_uuid, count))
    conn.commit()
    conn.close()


def get_inventory(user_uuid):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT image_id FROM user_inventory WHERE user_uuid = ?
    """, (user_uuid,))
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]


def add_image_to_inventory(user_uuid, image_id):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO user_inventory (user_uuid, image_id)
            VALUES (?, ?)
        """, (user_uuid, image_id))
        conn.commit()
    except sqlite3.IntegrityError:
        # 중복된 이미지면 무시
        pass
    finally:
        conn.close()


def get_world_records(limit=10):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT user_uuid, click_count
        FROM user_clicks
        ORDER BY click_count DESC
        LIMIT ?
    """, (limit,))
    records = [{"user_uuid": row[0], "click_count": row[1]} for row in c.fetchall()]
    conn.close()
    return records


if __name__ == "__main__":
    print("📦 Initializing database...")
    init_db()

    user_id = "test-user-uuid"
    print(f"👤 테스트 사용자 UUID: {user_id}")

    print("➕ 클릭 수 추가...")
    add_clicks(user_id, 10)

    print("🎨 이미지 인벤토리에 추가...")
    add_image_to_inventory(user_id, "brainrot_001")
    add_image_to_inventory(user_id, "brainrot_002")  # 중복 테스트 가능

    print("📋 인벤토리 가져오기:")
    inventory = get_inventory(user_id)
    print(inventory)

    print("🏆 월드 랭킹 TOP 10:")
    leaderboard = get_world_records()
    for rank, record in enumerate(leaderboard, 1):
        print(f"{rank}. {record['user_uuid']} - {record['click_count']} clicks")