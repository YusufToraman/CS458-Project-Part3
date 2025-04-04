# --- Test cases ---
test_cases = [
    {
        "label": "Invalid password",
        "email": "admin123@gmail.com",
        "password": "wrongpass",
        "expect_success": False
    },
    {
        "label": "Nonexistent user",
        "email": "wronguser@gmail.com",
        "password": "admin123",
        "expect_success": False
    },
    {
        "label": "Invalid email format (no @)",
        "email": "wrongusergmail.com",
        "password": "admin123",
        "expect_success": False
    },
    {
        "label": "Invalid email format (no .com)",
        "email": "wronguser@gmail",
        "password": "admin123",
        "expect_success": False
    },
    {
        "label": "Valid credentials",
        "email": "admin@gmail.com",
        "password": "admin123",
        "expect_success": True
    },
]

valid_credential = {
    "email": "admin@gmail.com",
    "password": "admin123",
}

email_sent_test_cases = [
    {
        "label": "Not sending email",
        "email": "a",
        "expect_success": False
    },
    {
        "label": "Sending email",
        "email": "burakdemirel49@gmail.com",
        "expect_success": True
    }
]