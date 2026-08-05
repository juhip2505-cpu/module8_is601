from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.jwt_handler import get_current_user
from app.models import Calculation, User
from app.operations import calculate_result
from app.schemas import (
    CalculationCreate,
    CalculationRead,
    CalculationUpdate,
)

router = APIRouter(
    prefix="/calculations",
    tags=["Calculations"],
)


@router.post(
    "",
    response_model=CalculationRead,
    status_code=status.HTTP_201_CREATED,
)
def create_calculation(
    calculation: CalculationCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    result = calculate_result(
        calculation.a,
        calculation.b,
        calculation.type.value,
    )

    db_calculation = Calculation(
        a=calculation.a,
        b=calculation.b,
        type=calculation.type.value,
        result=result,
        user_id=current_user.id,
    )

    db.add(db_calculation)
    db.commit()
    db.refresh(db_calculation)

    return db_calculation


@router.get(
    "",
    response_model=list[CalculationRead],
)
def browse_calculations(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    return (
        db.query(Calculation)
        .filter(Calculation.user_id == current_user.id)
        .all()
    )


@router.get(
    "/{calculation_id}",
    response_model=CalculationRead,
)
def read_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    return calculation


@router.put(
    "/{calculation_id}",
    response_model=CalculationRead,
)
def update_calculation(
    calculation_id: int,
    update: CalculationUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    calculation.a = update.a
    calculation.b = update.b
    calculation.type = update.type.value
    calculation.result = calculate_result(
        update.a,
        update.b,
        update.type.value,
    )

    db.commit()
    db.refresh(calculation)

    return calculation


@router.delete(
    "/{calculation_id}",
)
def delete_calculation(
    calculation_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    calculation = (
        db.query(Calculation)
        .filter(
            Calculation.id == calculation_id,
            Calculation.user_id == current_user.id,
        )
        .first()
    )

    if calculation is None:
        raise HTTPException(
            status_code=404,
            detail="Calculation not found",
        )

    db.delete(calculation)
    db.commit()

    return {
        "message": "Calculation deleted successfully"
    }