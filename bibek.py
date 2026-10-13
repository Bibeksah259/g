username="bibek"
password="python123"
is_active=True
if username:
    if password:
        if is_active:
            print("login successful")
        else:
            print("account is not active")
    else:
        print("password required")
else:
    print("username required")