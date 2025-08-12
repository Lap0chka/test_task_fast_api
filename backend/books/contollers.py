@app.post("/auth/register", status_code=201)
def register(user_in: UserRegister, db: Session = Depends(get_db)):
    existing = db.scalar(select(User).where(func.lower(User.username) == user_in.username.lower()))
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")
    user = User(username=user_in.username, password_hash=get_password_hash(user_in.password))
    db.add(user)
    db.commit()
    db.refresh(user)
    return {"id": str(user.id), "username": user.username}