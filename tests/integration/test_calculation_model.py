from app.database import Base, SessionLocal, engine
from app.models import Calculation


def test_create_calculation():
    Base.metadata.create_all(bind=engine)

    db = SessionLocal()

    try:
        calculation = Calculation(
            a=10,
            b=5,
            type="Add",
            result=15,
        )

        db.add(calculation)
        db.commit()
        db.refresh(calculation)

        assert calculation.id is not None
        assert calculation.result == 15
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)