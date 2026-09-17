import httpx
from jose import jwt
from app.core.config import settings
from app.core.database import SessionLocal
from app.models.user import User


def test_auth():
    client = httpx.Client(base_url="http://127.0.0.1:8000", timeout=30.0)

    test_email = "demo_ecologist@darukaa.earth"
    test_password = "ForestConservation2026!"

    # Ensure clean slate for idempotent testing
    cleanup_db = SessionLocal()
    cleanup_db.query(User).filter(User.email == test_email).delete()
    cleanup_db.commit()
    cleanup_db.close()

    print("--- TEST 1: Register user ---")
    reg_res = client.post("/auth/register", json={"email": test_email, "password": test_password})
    print("Register status:", reg_res.status_code)
    print("Register response:", reg_res.json())
    assert reg_res.status_code == 201, f"Expected 201, got {reg_res.status_code}"
    user_data = reg_res.json()
    assert "hashed_password" not in user_data, "Password leak in UserOut!"
    assert user_data["email"] == test_email
    assert user_data["id"].startswith("usr-")

    print("\n--- TEST 2: Verify Supabase database storage ---")
    db = SessionLocal()
    db_user = db.query(User).filter(User.email == test_email).first()
    assert db_user is not None, "User was not found in Supabase!"
    print("User in Supabase DB:")
    print("  ID:", db_user.id)
    print("  Email:", db_user.email)
    print("  Hashed Password:", db_user.hashed_password)
    assert db_user.hashed_password.startswith("$2b$"), "Password is not a valid bcrypt hash!"
    assert db_user.hashed_password != test_password, "Password was stored in plaintext!"
    db.close()

    print("\n--- TEST 3: Duplicate registration (should return 409) ---")
    dup_res = client.post("/auth/register", json={"email": test_email, "password": test_password})
    print("Duplicate status:", dup_res.status_code)
    print("Duplicate detail:", dup_res.json())
    assert dup_res.status_code == 409, f"Expected 409, got {dup_res.status_code}"

    print("\n--- TEST 4: Login with incorrect password (should return 401) ---")
    bad_login = client.post("/auth/login", json={"email": test_email, "password": "WrongPassword123!"})
    print("Bad login status:", bad_login.status_code)
    print("Bad login detail:", bad_login.json())
    assert bad_login.status_code == 401, f"Expected 401, got {bad_login.status_code}"
    assert bad_login.headers.get("www-authenticate") == "Bearer"

    print("\n--- TEST 5: Login with correct credentials (should return 200 + token) ---")
    good_login = client.post("/auth/login", json={"email": test_email, "password": test_password})
    print("Good login status:", good_login.status_code)
    token_data = good_login.json()
    print("Token data:", token_data)
    assert good_login.status_code == 200, f"Expected 200, got {good_login.status_code}"
    assert "access_token" in token_data
    assert token_data["token_type"] == "bearer"

    print("\n--- TEST 6: Decode and sanity-check JWT payload ---")
    token = token_data["access_token"]
    payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    print("Decoded JWT payload:", payload)
    assert payload["sub"] == db_user.id
    assert "exp" in payload
    assert "iat" in payload

    print("\nALL 6 VERIFICATION TESTS PASSED SUCCESSFULLY!")


if __name__ == "__main__":
    test_auth()
