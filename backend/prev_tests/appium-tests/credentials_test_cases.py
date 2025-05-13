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

datetime_test_cases = [
    {
        "label": "Valid date",
        "date": "01/10/2023",
        "expect_success": True
    },
    {
        "label": "Invalid date format",
        "date": "32/10/2023",
        "expect_success": False
    },
    {
        "label": "Invalid date format (no year)",
        "date": "01/10",
        "expect_success": False
    },
    {
        "label": "Invalid date format (no month)",
        "date": "01/2023",
        "expect_success": False
    }
]