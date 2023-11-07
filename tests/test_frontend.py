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
    def enter_ip(ip):
        page.get_by_label("Enter IP address").click()
        page.get_by_label("Enter IP address").fill(ip)
        page.get_by_label("Enter IP address").press("Enter")
        running_icon.wait_for(state="hidden")

    page.get_by_role("img", name="open").click()
    page.get_by_text("Network Tool").click()
    page.get_by_role("img", name="open").nth(1).click()
    page.get_by_text("Subnet Scanner").click()
    running_icon = page.get_by_text("Running...")

    # Invalid input - not IP
    enter_ip("1.2.3")

    # Check error message
    error = page.get_by_test_id("stNotification")
    expect(error).to_be_visible()
    expect(error).to_have_text("Invalid IP address.")

    # Invalid input - bogon IP
    enter_ip("192.168.0.1")

    # Check error message
    error = page.get_by_test_id("stNotification")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "That IP is reserved for special use and cannot be located."
    )

    # Valid input - 8.8.8.8
    enter_ip("8.8.8.8")

    # Check map
    ip_map = page.locator("#view-default-view")
    ip_map.wait_for(state="visible", timeout=0)
    expect(ip_map).to_be_visible()

    # Check table
    expect(page.locator(".dvn-scroller")).to_be_visible()
    table = page.locator("//table[@role='grid']")

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

        if row_num - 2 >= 4 and row_num - 2 <= 7:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Ath Thawrah")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("SY")
        elif (
            (row_num - 2 >= 16 and row_num - 2 <= 19)
            or row_num - 2 == 84
            or row_num - 2 == 115
            or row_num - 2 == 138
            or (row_num - 2 >= 204 and row_num - 2 <= 207)
            or (row_num - 2 >= 242 and row_num - 2 <= 243)
        ):
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Pretty Prairie")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("US")
        elif (
            (row_num - 2 >= 20 and row_num - 2 <= 23)
            or (row_num - 2 >= 86 and row_num - 2 <= 87)
            or row_num - 2 == 116
            or (row_num - 2 >= 148 and row_num - 2 <= 149)
            or (row_num - 2 >= 188 and row_num - 2 <= 195)
            or (row_num - 2 >= 216 and row_num - 2 <= 223)
            or row_num - 2 == 235
        ):
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Mecca")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("SA")
        elif row_num - 2 == 29:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Lucknow")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("IN")
        elif row_num - 2 >= 44 and row_num - 2 <= 47:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Jambi City")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("ID")
        elif row_num - 2 >= 100 and row_num - 2 <= 101:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Narsimhapur")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("IN")
        elif row_num - 2 >= 102 and row_num - 2 <= 103:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Wed Alnkil")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("SA")
        elif row_num - 2 >= 104 and row_num - 2 <= 111:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Ar Rass")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("SA")
        elif row_num - 2 == 114:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Chicago")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("US")
        elif row_num - 2 >= 128 and row_num - 2 <= 131:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text(
                "Dardenne Prairie"
            )
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("US")
        elif row_num - 2 >= 160 and row_num - 2 <= 161:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Hyderābād")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("IN")
        else:
            expect(row.locator("//td[@aria-colindex=3]")).to_have_text("Mountain View")
            expect(row.locator("//td[@aria-colindex=4]")).to_have_text("US")


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
