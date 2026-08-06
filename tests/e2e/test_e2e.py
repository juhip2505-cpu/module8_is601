# tests/e2e/test_e2e.py

import uuid
import pytest  # Import the pytest framework for writing and running tests
from playwright.sync_api import expect

# The following decorators and functions define E2E tests for the FastAPI calculator application.

@pytest.mark.e2e
def test_hello_world(page, fastapi_server):
    """
    Test that the homepage displays "Hello World".

    This test verifies that when a user navigates to the homepage of the application,
    the main header (`<h1>`) correctly displays the text "Hello World". This ensures
    that the server is running and serving the correct template.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Use an assertion to check that the text within the first <h1> tag is exactly "Hello World".
    # If the text does not match, the test will fail.
    assert page.inner_text('h1') == 'Calculator'

@pytest.mark.e2e
def test_calculator_add(page, fastapi_server):
    """
    Test the addition functionality of the calculator.

    This test simulates a user performing an addition operation using the calculator
    on the frontend. It fills in two numbers, clicks the "Add" button, and verifies
    that the result displayed is correct.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '5'.
    page.fill('#b', '5')
    
    # Click the button that has the exact text "Add". This triggers the addition operation.
    page.click('button:text("Add")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly "Result: 15".
    # This verifies that the addition operation was performed correctly and the result is displayed as expected.
    expect(page.locator("#result")).to_have_text(
    "Result: 15",
    timeout=5000,
)

@pytest.mark.e2e
def test_calculator_divide_by_zero(page, fastapi_server):
    """
    Test the divide by zero functionality of the calculator.

    This test simulates a user attempting to divide a number by zero using the calculator.
    It fills in the numbers, clicks the "Divide" button, and verifies that the appropriate
    error message is displayed. This ensures that the application correctly handles invalid
    operations and provides meaningful feedback to the user.
    """
    # Navigate the browser to the homepage URL of the FastAPI application.
    page.goto('http://localhost:8000')
    
    # Fill in the first number input field (with id 'a') with the value '10'.
    page.fill('#a', '10')
    
    # Fill in the second number input field (with id 'b') with the value '0', attempting to divide by zero.
    page.fill('#b', '0')
    
    # Click the button that has the exact text "Divide". This triggers the division operation.
    page.click('button:text("Divide")')
    
    # Use an assertion to check that the text within the result div (with id 'result') is exactly
    # "Error: Cannot divide by zero!". This verifies that the application handles division by zero
    # gracefully and displays the correct error message to the user.
    expect(page.locator("#result")).to_have_text(
    "Error: Cannot divide by zero!",
    timeout=5000,
)

@pytest.mark.e2e
def test_user_registration(page, fastapi_server):
    """
    Test successful user registration through the frontend form.
    """
    unique_id = uuid.uuid4().hex[:8]

    username = f"playwrightuser{unique_id}"
    email = f"playwright_{unique_id}@example.com"

    page.goto("http://localhost:8000/register-page")

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", "Password123")
    page.fill("#confirm-password", "Password123")

    page.click('button:text("Register")')

    expect(page.locator("#message")).to_have_text(
        "Registration successful!",
        timeout=5000,
    )

@pytest.mark.e2e
def test_user_login(page, fastapi_server):
    """
    Test successful user login through the frontend form.
    """
    unique_id = uuid.uuid4().hex[:8]

    username = f"loginuser{unique_id}"
    email = f"login_{unique_id}@example.com"
    password = "Password123"

    page.goto("http://localhost:8000/register-page")

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)

    page.click('button:text("Register")')

    expect(page.locator("#message")).to_have_text(
        "Registration successful!",
        timeout=5000,
    )

    page.goto("http://localhost:8000/login-page")

    page.fill("#email", email)
    page.fill("#password", password)

    page.click('button:text("Login")')

    expect(page.locator("#message")).to_have_text(
        "Login successful!",
        timeout=5000,
    )


@pytest.mark.e2e
def test_registration_rejects_short_password(
    page,
    fastapi_server,
):
    """
    Test that registration rejects a password
    shorter than eight characters.
    """
    unique_id = uuid.uuid4().hex[:8]

    page.goto(
        "http://localhost:8000/register-page"
    )

    page.fill(
        "#username",
        f"shortpass{unique_id}",
    )

    page.fill(
        "#email",
        f"shortpass_{unique_id}@example.com",
    )

    page.fill(
        "#password",
        "short",
    )

    page.fill(
        "#confirm-password",
        "short",
    )

    page.click('button:text("Register")')

    expect(
        page.locator("#message")
    ).to_have_text(
        "Password must be at least 8 characters long.",
        timeout=5000,
    )


@pytest.mark.e2e
def test_login_rejects_wrong_password(
    page,
    fastapi_server,
):
    """
    Test that login rejects an incorrect password.
    """
    unique_id = uuid.uuid4().hex[:8]

    username = f"wrongpass{unique_id}"
    email = f"wrongpass_{unique_id}@example.com"
    password = "Password123"

    page.goto(
        "http://localhost:8000/register-page"
    )

    page.fill("#username", username)
    page.fill("#email", email)
    page.fill("#password", password)
    page.fill("#confirm-password", password)

    page.click('button:text("Register")')

    expect(
        page.locator("#message")
    ).to_have_text(
        "Registration successful!",
        timeout=5000,
    )

    page.goto(
        "http://localhost:8000/login-page"
    )

    page.fill("#email", email)
    page.fill("#password", "WrongPassword123")

    page.click('button:text("Login")')

    expect(
        page.locator("#message")
    ).to_have_text(
        "Invalid email or password",
        timeout=5000,
    )