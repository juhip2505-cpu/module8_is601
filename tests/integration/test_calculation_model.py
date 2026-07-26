from app.database import SessionLocal
from app.models import Calculation


def test_create_calculation():
    db = SessionLocal()

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

    db.delete(calculation)
    db.commit()
    db.close()