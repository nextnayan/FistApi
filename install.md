pip install fastapi "uvicorn[standard]" sqlalchemy pydantic-settings python-dotenv
pip freeze > requirements.txt
git push fistapi main
uvicorn main:app --reload


{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiJ0ZXN0QGV4YW1wbGUuY29tIiwiZXhwIjoxNzc1NjU4NzAxfQ.mNkp_A4NmlCc5Sh20eEWjDIo9FHj3XE5SLEwiZWUqB4",
  "token_type": "bearer"
}


{
  "email": "test@example.com",
  "full_name": "Test User",
  "password": "mysecretpassword123"
}