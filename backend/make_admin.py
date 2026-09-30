import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.orm import Session
from app.core.database import SessionLocal
from app.models.user import User, UserRole

def make_admin(email: str):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.email == email).first()
        if not user:
            print(f"Error: Koi aisi user id ({email}) nahi mili database me!")
            return
            
        if user.role == UserRole.ADMIN:
            print(f"User {email} pehle se hi ADMIN hai!")
        else:
            user.role = UserRole.ADMIN
            db.commit()
            print(f"Success! {email} ab ADMIN ban gaya hai. 🎉")
    except Exception as e:
        print("Error aaya:", e)
    finally:
        db.close()

if __name__ == "__main__":
    email_to_upgrade = input("Admin kisko banana hai? Apna email type karo: ")
    make_admin(email_to_upgrade)
