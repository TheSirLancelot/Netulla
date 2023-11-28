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

    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" HTTP Header Tool").click()

    # Check page title
    expect(
        page.get_by_role("heading", name="HTTP Header Tool").locator("span")
    ).to_be_visible()

    # Check invalid inputs
    enter_address("www.google.com")  # Missing schema
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, and enter IPs in the form x.x.x.x using only numbers."
    )

    enter_address("htt://www.google.com")  # Invalid schema
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text("Invalid URL. Please use http:// or https://")

    enter_address(
        "https://www.notasite.com"
    )  # Invalid URL, disabled timeout b/c sometimes webkit test checks slightly before loaded
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Site doesn't exist or connection cannot be made at this time.", timeout=0
    )

    enter_address("8.8.8")  # Invalid IP - wrong length
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text(
        "Incomplete URL or invalid IP. Please include http:// or https:// for URLs, and enter IPs in the form x.x.x.x using only numbers."
    )

    enter_address("8.8.8.8s")  # Invalid IP - invalid characters
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


def test_regex_tester(page: Page):
    # TODO: empty test
    pass


def test_certificate_lookup(page: Page):
    def enter_domain_and_submit(domain):
        # Enter the domain into the text input
        page.get_by_label("Enter a URL (e.g., google.com)").fill(domain)
        # Click the "Get Certificate" button
        page.get_by_test_id("baseButton-secondary").click()

    # Access the Certificate Lookup tool
    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" Certificate Lookup").click()

    # Check page title
    expect(
        page.get_by_role("heading", name="Certificate Lookup").locator("span")
    ).to_be_visible()

    # Invalid input - empty domain
    enter_domain_and_submit("")

    # Check error message for empty domain
    error = page.get_by_test_id("stNotification")
    expect(error).to_be_visible()
    expect(error).to_have_text("Please enter a URL before clicking the button.")

    # Valid input - www.google.com
    enter_domain_and_submit("www.google.com")

    # Check to make sure there isn't an error
    error = page.get_by_test_id("stNotification")
    expect(error).to_be_hidden()


def test_subnet_scanner(page: Page):
    def enter_ip(ip):
        page.get_by_label("Enter IP address").click()
        page.get_by_label("Enter IP address").fill(ip)
        page.get_by_label("Enter IP address").press("Enter")

    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" Subnet Scanner").click()

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
    table = page.locator(
        "//table[@role='grid']"
    )  # Switch to subcomponent to check cells

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


# Test for the online_curl_tool function
def test_curl(page: Page):
    # Access the Online Curl Tool
    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" Online Curl Tool").click()

    # Check page title
    expect(
        page.get_by_role("heading", name="Online Curl Tool").locator("span")
    ).to_be_visible()

    # Enter a valid URL and click the button
    page.get_by_label("Enter URL: https://www.example.com").fill("https://www.google.com")
    page.get_by_test_id("baseButton-secondary").click()

    # Check for the absence of error message
    error = page.get_by_test_id("stNotification")
    expect(error).to_be_hidden()


def test_password_complexity(page: Page):
    # Go to Password Complexity function
    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" Password Complexity").click()

    # Check page title
    expect(
        page.get_by_role("heading", name="Password Complexity Checker").locator("span")
    ).to_be_visible()

    # Test for an unacceptable password
    enter_password(page, "short")
    assert_password_complexity(page, "Unacceptable")

    # Test for a weak password
    enter_password(page, "weakpassword")
    assert_password_complexity(page, "Weak")

    # Test for a meh password
    enter_password(page, "MehPassword123")
    assert_password_complexity(page, "Meh")

    # Test for a strong password
    enter_password(page, "Strong@Password123")
    assert_password_complexity(page, "Strong")


def enter_password(page: Page, password: str):
    password_input = page.get_by_label("Password:")
    password_input.fill(password)
    page.keyboard.press("Enter")  # needed since you don't have a button


def assert_password_complexity(page: Page, expected_complexity: str):
    complexity_text = page.get_by_text("Password Complexity:")
    expect(complexity_text).to_have_text(f"Password Complexity: {expected_complexity}")


def test_ns_lookup(page: Page):
    def run_test(domain: str, expected_result: str):
        # Go to the main page of the Streamlit app
        page.goto(f"http://localhost:{PORT}")

        # Go to NS Lookup function
        page.frame_locator(
            'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
        ).get_by_role("menuitem", name=" Ns Lookup").click()

        # Wait for the page to load
        page.wait_for_selector(
            'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
        )
        # Check page title
        expect(
            page.get_by_role("heading", name="NS Lookup").locator("span")
        ).to_be_visible()

        # Wait for the input field to be visible on the ns_lookup subpage
        domain_input_selector = 'input[aria-label="Enter Domain (e.g., google.com)"]'
        domain_input = page.wait_for_selector(domain_input_selector, state="visible")

        # Fill in the domain name
        domain_input.fill(domain)

        # Simulate pressing the Enter key to submit the domain
        page.press(domain_input_selector, "Enter")

        # Wait for the Streamlit action to complete
        page.wait_for_timeout(3000)  # Adjust this based on response time

        # Check for the expected result
        result_message = page.locator(f"text={expected_result}")
        expect(result_message).to_have_count(1)

    # Test with a valid domain name
    run_test("google.com", "Valid Domain")

    # Test with an empty input
    run_test("", "Please enter a domain.")

    # Test with a non-existent domain
    run_test("nonexistentdomain123456789.com", "Domain does not exist.")


def test_ping(page: Page):
    # TODO: empty test
    pass


def test_whois_lookup(page: Page):
    def enter_address(address):
        page.get_by_label("Enter URL or IP address").click()
        page.get_by_label("Enter URL or IP address").fill(address)
        page.keyboard.press("Enter")

    # Go to Whois Lookup function
    page.frame_locator(
        'iframe[title="streamlit_antd_components\\.utils\\.component_func\\.sac"]'
    ).get_by_role("menuitem", name=" Whois Lookup").click()

    # Check page title
    expect(
        page.get_by_role("heading", name="Whois Lookup Tool").locator("span")
    ).to_be_visible()

    # Check invalid IP
    enter_address("1111.1111.1111.1111")
    error = page.get_by_test_id("stNotification")
    error.wait_for(state="visible")
    expect(error).to_be_visible()
    expect(error).to_have_text("Please enter a valid URL or IP address")

    # Check entering URL
    enter_address("https://www.google.com")
    results = page.get_by_text("Results")
    results.wait_for(state="visible")
    expect(results).to_be_visible()


def test_what_is_my_ip(page: Page):
    # TODO: empty test
    pass


def test_traceroute_visualizer(page: Page):
    # TODO: empty test
    pass


def test_password_generator(page: Page):
    # TODO: empty test
    pass
