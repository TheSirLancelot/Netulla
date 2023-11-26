import time
import pytest
from playwright.sync_api import Page, expect

PORT = "8501"

# TODO: Maybe check to see if the container is running?


# This expects the container to already be running
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


# use examples from this repo to build out the unit tests for your feature
# https://github.com/randyzwitch/streamlit-folium/blob/master/tests/test_frontend.py

# python-playwright docs:
# https://playwright.dev/python/docs/


def test_page_name(page: Page):
    page.goto(f"http://localhost:{PORT}")
    # Make sure that page is fully loaded before checking title
    expect(page.get_by_role("heading", name="Netulla").locator("span")).to_be_visible()
    # check that the page title is "Netulla"
    assert page.title() == "Netulla"


def test_url_encoder_decoder(page: Page):
    # TODO: empty test
    pass


def test_http_header_tool(page: Page):
    def enter_address(address):
        page.get_by_label("Enter URL or IP address").click()
        page.get_by_label("Enter URL or IP address").fill(address)
        page.get_by_test_id("baseButton-secondary").click()

    page.frame_locator("iframe[title=\"streamlit_antd_components\\.utils\\.component_func\\.sac\"]").get_by_role("menuitem", name=" HTTP Header Tool").click()

    # Check page title
    expect(page.get_by_role("heading", name="HTTP Header Tool").locator("span")).to_be_visible()

    # Check invalid inputs
    enter_address("www.google.com")   # Missing schema
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, and enter IPs in the form x.x.x.x using only numbers."
    )

    enter_address("htt://www.google.com")   # Invalid schema
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Invalid URL. Please use http:// or https://"
    )

    enter_address("https://www.notasite.com")   # Invalid URL, disabled timeout b/c sometimes webkit test checks slightly before loaded
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Site doesn't exist or connection cannot be made at this time.",
        timeout=0
    )

    enter_address("8.8.8")   # Invalid IP - wrong length
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, and enter IPs in the form x.x.x.x using only numbers."
    )

    enter_address("8.8.8.8s")   # Invalid IP - invalid characters
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, and enter IPs in the form x.x.x.x using only numbers."
    )

    # Check entering URL
    enter_address("https://www.google.com")
    headers = page.get_by_text("Headers")
    headers.wait_for(state="visible")
    expect(headers).to_be_visible()

    # Check entering IP
    enter_address("8.8.8.8")
    headers = page.get_by_text("Headers")
    headers.wait_for(state="visible")
    expect(headers).to_be_visible()


def test_reverse_ip(page: Page):
    # TODO: empty test
    pass


def test_certificate_lookup(page: Page):
    # TODO: empty test
    pass


def test_subnet_scanner(page: Page):
    def enter_ip(ip):
        page.get_by_label("Enter IP address").click()
        page.get_by_label("Enter IP address").fill(ip)
        page.get_by_label("Enter IP address").press("Enter")

    page.frame_locator("iframe[title=\"streamlit_antd_components\\.utils\\.component_func\\.sac\"]").get_by_role("menuitem", name=" Subnet Scanner").click()

    # Invalid input - not IP
    enter_ip("1.2.3")

    # Check error message
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text("Invalid IP address.")

    # Invalid input - bogon IP
    enter_ip("192.168.0.1")

    # Check error message
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "That IP is reserved for special use and cannot be located."
    )

    # Valid input - 8.8.8.8
    enter_ip("8.8.8.8")

    # Check map
    # TODO: Make test work for checking map, currently hangs forever b/c map never appears in GitHub
    # ip_map = page.locator("#view-default-view")
    # expect(ip_map).to_be_visible()

    # Check table
    table = page.locator(".dvn-scroller")
    table.wait_for(state="visible")
    expect(table).to_be_visible()
    table = page.locator("//table[@role='grid']")   # Switch to subcomponent to check cells

    # Headers
    EXPECTED_HEADERS = ["", "IP", "City", "Country"]
    for col, expected in enumerate(EXPECTED_HEADERS, 1):
        expect(table.locator(f"//thead/tr/th[@aria-colindex={col}]")).to_have_text(
            expected
        )
    # Body
    for row_num in range(2, 256 + 2):  # Header included in numbering, rows start at 2
        row = table.locator(f"//tbody/tr[@aria-rowindex={row_num}]")

        expect(row.locator("//td[@aria-colindex=1]")).to_have_text(f"{row_num - 2}")
        expect(row.locator("//td[@aria-colindex=2]")).to_have_text(
            f"8.8.8.{row_num - 2}"
        )

        # Location data may change, just check that cells are full
        expect(row.locator("//td[@aria-colindex=3]")).not_to_be_empty()
        expect(row.locator("//td[@aria-colindex=4]")).not_to_be_empty()


def test_wget(page: Page):
    # TODO: empty test
    pass


def test_password_complexity(page: Page):
    # TODO: empty test
    pass


def test_ns_lookup(page: Page):
    # TODO: empty test
    pass


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
