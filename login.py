from werkzeug.security import generate_password_hash, check_password_hash

# When user signs up
user_password = "somesecretpassword"
hashed_password = generate_password_hash(
    user_password)  # store this in database

# When user signs in with wrong password
wrong_user_password = "wrongpassword"
# retrieve hashed_password from database and take the password keyed by user in the sign in form
result_one = check_password_hash(hashed_password, wrong_user_password)
print(result_one)

# When user signs in with correct password
correct_user_password = "somesecretpassword"
# retrieve hashed_password from database and take the password keyed by user in the sign in form
result_two = check_password_hash(hashed_password, correct_user_password)
print(result_two)
