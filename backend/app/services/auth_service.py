from datetime import datetime, timedelta, timezone

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    generate_refresh_token,
    hash_refresh_token,
)
from app.models import User,RefreshToken

from app.schemas.auth import RegisterRequest


def register_user(request: RegisterRequest, db: Session) -> User:
    # 1. Check if email already exists
    existing_user = db.query(User).filter(User.email == request.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # 2. Create new user with hashed password
    new_user = User(
        email=request.email,
        hashed_password=hash_password(request.password),
        first_name=request.first_name,
        last_name=request.last_name,
    )

    # 3. Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def _create_tokens(user: User, db: Session) -> dict:
    """Access + Refresh token pair banata hai. Internal helper function."""

    # 1. Access token (short-lived, 30 min)
    access_token = create_access_token(data={"sub": str(user.id)})

    # 2. Refresh token (long-lived, 7 days)
    raw_refresh_token = generate_refresh_token()
    token_hash = hash_refresh_token(raw_refresh_token)
    expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)

    # 3. Save refresh token hash in DB
    db_refresh_token = RefreshToken(
        user_id=user.id,
        token_hash=token_hash,
        expires_at=expires_at,
    )
    db.add(db_refresh_token)
    db.commit()

    return {
        "access_token": access_token,
        "refresh_token": raw_refresh_token,
        "token_type": "bearer",
    }


def authenticate_user(email: str, password: str, db: Session) -> dict:
    # 1. Find user by email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 2. Verify password
    if not verify_password(password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password"
        )

    # 3. Check if user is active
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Account is deactivated"
        )

    # 4. Create both tokens
    return _create_tokens(user, db)


def refresh_access_token(refresh_token: str, db: Session) -> dict:
    """Purana refresh token leke naya access + refresh token deta hai (ROTATION)."""

    # 1. Hash the incoming token to find it in DB
    token_hash = hash_refresh_token(refresh_token)

    # 2. Find in DB
    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
    ).first()

    if not db_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid refresh token"
        )

    # 3. Check expiry
    if db_token.expires_at < datetime.now(timezone.utc):
        db_token.revoked = True
        db.commit()
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token expired"
        )

    # 4. Revoke old token (rotation — har baar naya token milega)
    db_token.revoked = True
    db.commit()

    # 5. Get user
    user = db.query(User).filter(User.id == db_token.user_id).first()
    if not user or not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found or deactivated"
        )

    # 6. Create new token pair
    return _create_tokens(user, db)


def logout_user(refresh_token: str, db: Session) -> None:
    """Refresh token revoke karta hai — effectively logout."""

    token_hash = hash_refresh_token(refresh_token)

    db_token = db.query(RefreshToken).filter(
        RefreshToken.token_hash == token_hash,
        RefreshToken.revoked == False,
    ).first()

    if db_token:
        db_token.revoked = True
        db.commit()