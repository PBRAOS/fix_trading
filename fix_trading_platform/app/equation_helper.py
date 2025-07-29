from models import Base, User, Trade, CashReservation
from sqlalchemy.orm import Session

## Helper functions to check cash binding
def bind_cash(user_id, symbol, quantity, price, db: Session):

    ## EQUATION CALL BIND.

    # Create a reservation record in the DB
    reservation = CashReservation(
        user_id=user_id,
        symbol=symbol,
        quantity=quantity,
        price=price,
        is_finalized=False
    )
    db.add(reservation)
    db.commit()
    db.refresh(reservation)
    return True

def finalize_cash(user_id, symbol, quantity, price, db: Session):

    ## EQUATION CALL FINALIZE.

    # Update the reservation to finalized
    reservation = db.query(CashReservation).filter_by(
        user_id=user_id,
        symbol=symbol,
        quantity=quantity,
        price=price,
        is_finalized=False
    ).first()
    if reservation:
        reservation.is_finalized = True
        db.commit()

def rollback_cash_reservation(user_id, symbol, quantity, price, db: Session):

    ## EQUATION CALL ROLLBACK.

    # Delete the reservation if something fails
    reservation = db.query(CashReservation).filter_by(
        user_id=user_id,
        symbol=symbol,
        quantity=quantity,
        price=price,
        is_finalized=False
    ).first()
    if reservation:
        db.delete(reservation)
        db.commit()
