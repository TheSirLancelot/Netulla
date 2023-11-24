# DON'T FORGET TO RUN:
# pip -r requirements.txt

from contextlib import contextmanager
from time import sleep
import subprocess

import pytest
from playwright.sync_api import Page, expect


LOCAL_TEST = False

PORT = "8503" if LOCAL_TEST else "8699"


@pytest.fixture(scope="module", autouse=True)
def before_module():
    # Run the streamlit app before each module
    with run_streamlit():
        yield


@pytest.fixture(scope="function", autouse=True)
def before_test(page: Page):
    page.goto(f"localhost:{PORT}")
    page.set_viewport_size({"width": 2000, "height": 2000})


# Take screenshot of each page if there are failures for this session
@pytest.fixture(scope="function", autouse=True)
def after_test(page: Page, request):
    yield
    if request.node.rep_call.failed:
        page.screenshot(path=f"screenshot-{request.node.name}.png", full_page=True)


@contextmanager
def run_streamlit():
    """Run the streamlit app on port 8599"""

    if LOCAL_TEST:
        try:
            yield 1
        finally:
            pass
    else:
        p = subprocess.Popen(
            [
                "streamlit",
                "run",
                "Home.py",
                "--server.port",
                PORT,
                "--server.headless",
                "true",
            ]
        )

        sleep(5)

        try:
            yield 1
        finally:
            p.kill()


# use examples from this repo to build out the unit tests for your feature
# https://github.com/randyzwitch/streamlit-folium/blob/master/tests/test_frontend.py

# python-playwright docs:
# https://playwright.dev/python/docs/


# generic test to make sure your testing framework is set up
def test_page_name(page: Page):
    # Check page title

    expect(page).to_have_title(
        "Shadow Suite"
    )  # TODO: Change this when we update test page


def test_url_encoder_decoder(page: Page):
    # TODO: empty test
    pass


def test_http_header_tool(page: Page):
    # TODO: empty test
    pass


def test_reverse_ip(page: Page):
    # TODO: empty test
    pass


def test_certificate_lookup(page: Page):
    # TODO: empty test
    pass


def test_subnet_scanner(page: Page):
    # TODO: empty test
    pass


def test_wget(page: Page):
    # TODO: empty test
    pass


def test_password_complexity(page: Page):
    # TODO: empty test
    pass


def test_ns_lookup(page: Page):
    # Go to the main page of the Streamlit app
    page.goto(f"http://localhost:{PORT}")

    # Go to NS Lookup function
    page.frame_locator("iframe[title=\"streamlit_antd_components\\.utils\\.component_func\\.sac\"]").get_by_role("menuitem", name=" Ns Lookup").click()

    # Check page title
    expect(page.get_by_role("heading", name="NS Lookup").locator("span")).to_be_visible()

    # Wait for the input field to be visible on the ns_lookup subpage
    domain_input_selector = 'input[aria-label="Enter Domain (e.g., google.com)"]'
    domain_input = page.wait_for_selector(domain_input_selector, state="visible")
    
    # Fill in the known domain name
    domain_input.fill("google.com")

    # Simulate pressing the Enter key to submit the domain
    page.press(domain_input_selector, "Enter")

    # Wait for the Streamlit action to complete
    page.wait_for_timeout(3000)  # Adjust this based on response time

    # Check for the success message
    success_message = page.locator("text=Valid Domain")
    expect(success_message).to_have_count(1)

    # Check if IP addresses are displayed as a list
    ip_addresses = page.locator("ul > li")
    ip_count = ip_addresses.count()

    # Assert that there is at least one IP address
    assert ip_count > 0, "No IP addresses were found."

    # Check if the hostname is displayed
    hostname = page.locator("text=Hostname")
    expect(hostname).to_have_count(1)

def test_ping(page: Page):
    # TODO: empty test
    pass


def test_whois_lookup(page: Page):
    # TODO: empty test
    pass


def test_what_is_my_ip(page: Page):
    # TODO: empty test
    pass


def test_traceroute_visualizer(page: Page):
    # TODO: empty test
    pass


def test_password_generator(page: Page):
    # TODO: empty test
    pass
