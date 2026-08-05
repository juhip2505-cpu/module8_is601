from app.database import Base, SessionLocal, engine
from app.models import Calculation, User


def test_create_calculation():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        user = User(
            username="testuser",
            email="test@example.com",
            password_hash="hashedpassword",
        )

        db.add(user)
        db.commit()
        db.refresh(user)

        calculation = Calculation(
            a=10,
            b=5,
            type="Add",
            result=15,
            user_id=user.id,
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        assert calculation.id is not None
        assert calculation.result == 15
        assert calculation.user_id == user.id

    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)