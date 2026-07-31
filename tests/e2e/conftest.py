import os
import subprocess
import time

import pytest
import requests
from playwright.sync_api import sync_playwright


@pytest.fixture(scope="session")
def fastapi_server(tmp_path_factory):
    test_directory = tmp_path_factory.mktemp(
        "e2e_database"
    )

    test_database = test_directory / "e2e_test.db"

    environment = os.environ.copy()
    environment["DATABASE_URL"] = (
        f"sqlite:///{test_database}"
    )

    init_process = subprocess.run(
        ["python", "-m", "app.init_db"],
        env=environment,
        capture_output=True,
        text=True,
    )

    if init_process.returncode != 0:
        raise RuntimeError(
            "Failed to initialize E2E database:\n"
            + init_process.stderr
        )

    fastapi_process = subprocess.Popen(
        ["python", "main.py"],
        env=environment,
    )

    server_url = "http://127.0.0.1:8000/"
    timeout = 30
    start_time = time.time()

    print("Starting FastAPI server...")

    while time.time() - start_time < timeout:
        try:
            response = requests.get(
                server_url,
                timeout=2,
            )

            if response.status_code == 200:
                print(
                    "FastAPI server is up and running."
                )
                break
        except requests.exceptions.RequestException:
            pass

        time.sleep(1)
    else:
        fastapi_process.terminate()
        raise RuntimeError(
            "FastAPI server failed to start "
            "within 30 seconds."
        )

    yield

    print("Shutting down FastAPI server...")
    fastapi_process.terminate()
    fastapi_process.wait()
    print("FastAPI server has been terminated.")


@pytest.fixture(scope="session")
def playwright_instance_fixture():
    with sync_playwright() as playwright:
        yield playwright


@pytest.fixture(scope="session")
def browser(playwright_instance_fixture):
    browser_instance = (
        playwright_instance_fixture.chromium.launch(
            headless=True
        )
    )

    yield browser_instance
    browser_instance.close()


@pytest.fixture
def page(browser):
    browser_page = browser.new_page()

    yield browser_page
    browser_page.close()