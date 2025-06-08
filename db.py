"""
    db.py
"""
import sqlite3
from pathlib import Path

DB_PATH = Path("sqlite3.db")


def init_db():
    """Initialize the SQLite database and create required tables if they do not exist."""
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

    # 이미지 생성 기록 저장
    c.execute("""
    CREATE TABLE IF NOT EXISTS generated_images (
        image_hash TEXT PRIMARY KEY,
        name TEXT,
        prompt TEXT,
        b64_json TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def add_generated_image(image_hash, name, prompt, b64_json):
    """
    Add a newly generated image's data to the database.

    Args:
        image_hash (str): The SHA-256 hash of the image, used as a primary key.
        name (str): The generated name for the image.
        prompt (str): The prompt used to generate the image.
        b64_json (str): The base64-encoded image data.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute("""
            INSERT INTO generated_images (image_hash, name, prompt, b64_json)
            VALUES (?, ?, ?, ?)
        """, (image_hash, name, prompt, b64_json))
        conn.commit()
    except sqlite3.IntegrityError:
        # 해시가 이미 존재하면 무시
        pass
    finally:
        conn.close()

def add_clicks(user_uuid, count):
    """
    Add to a user's total click count.

    Args:
        user_uuid (str): Unique user identifier.
        count (int): Number of clicks to add.
    """
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
    """
    Retrieve the list of image IDs in a user's inventory.

    Args:
        user_uuid (str): Unique user identifier.

    Returns:
        List[str]: List of image IDs.
    """
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
        SELECT image_id FROM user_inventory WHERE user_uuid = ?
    """, (user_uuid,))
    results = c.fetchall()
    conn.close()
    return [row[0] for row in results]


def add_image_to_inventory(user_uuid, image_id):
    """
    Add a new image to a user's inventory, if not already present.

    Args:
        user_uuid (str): Unique user identifier.
        image_id (str): ID of the image to add.
    """
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
    """
    Retrieve the top users sorted by click count.

    Args:
        limit (int): Maximum number of users to return. Default is 10.

    Returns:
        List[Dict[str, Union[str, int]]]: List of user records with UUID and click count.
    """
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

    USER_ID = "test-user-uuid"
    print(f"👤 테스트 사용자 UUID: {USER_ID}")

    print("➕ 클릭 수 추가...")
    add_clicks(USER_ID, 10)

    print("🎨 이미지 인벤토리에 추가...")
    add_image_to_inventory(USER_ID, "brainrot_001")
    add_image_to_inventory(USER_ID, "brainrot_002")  # 중복 테스트 가능

    print("📋 인벤토리 가져오기:")
    inventory = get_inventory(USER_ID)
    print(inventory)

    print("🏆 월드 랭킹 TOP 10:")
    leaderboard = get_world_records()
    for rank, record in enumerate(leaderboard, 1):
        print(f"{rank}. {record['user_uuid']} - {record['click_count']} clicks")
