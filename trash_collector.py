import os
import time
from datetime import datetime

from database import SessionLocal, FileRecord

TEMP_DIR = "/temp"
CHECK_INTERVAL = 3600  # 1 hour


def cleanup():
    db = SessionLocal()
    try:
        now = datetime.utcnow()
        expired = db.query(FileRecord).filter(FileRecord.expires_at <= now).all()

        for record in expired:
            path = os.path.join(TEMP_DIR, record.filename)
            if os.path.isfile(path):
                os.remove(path)
            db.delete(record)

        db.commit()
        print(f"[{now.isoformat()}] Cleaned up {len(expired)} expired file(s)")
    finally:
        db.close()


if __name__ == "__main__":
    print("Trash collector started")
    while True:
        cleanup()
        time.sleep(CHECK_INTERVAL)
