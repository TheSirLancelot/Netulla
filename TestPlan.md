# Test Plan Document <!-- omit in toc -->

- [IDENTIFICATION INFORMATION SECTION](#identification-information-section)
  - [PRODUCT](#product)
  - [PROJECT DESCRIPTION](#project-description)
  - [PERSONNEL](#personnel)
- [UNIT TEST SECTION](#unit-test-section)
  - [UNIT TEST STRATEGY / EXTENT OF UNIT TESTING:](#unit-test-strategy--extent-of-unit-testing)
  - [UNIT TEST CASES](#unit-test-cases)
- [INTEGRATION TEST SECTION](#integration-test-section)
  - [INTEGRATION TEST STRATEGY AND EXTENT OF INTEGRATION TESTING](#integration-test-strategy-and-extent-of-integration-testing)

## IDENTIFICATION INFORMATION SECTION

### PRODUCT

- **Product Name:** [Netulla](https://netulla.streamlit.app/)

### PROJECT DESCRIPTION

A web-based suite of multi-functional network tools

### PERSONNEL

-   William Weir, Team Lead
-   Tyler Wilson, Software Engineer
-   Tristan Young, Software Engineer
-   Oscar Vasquez FLores, Software Engineer
-   Reynaldo Veras, Software Engineer
-   Tyree Maeser, Software Engineer
-   Joshua Welch, N/A [^1]

[^1]: Joshua Welch was assigned to our group, but was not present during the semester.

## UNIT TEST SECTION

Evaluate new features and bug fixes introduced in this release

### UNIT TEST STRATEGY / EXTENT OF UNIT TESTING:

We utilize a docker container for our application, which alleviates the need for system dependencies. This docker container is also utilized for unit testing, ensuring we are testing how the user will interact with the features that are being implemented. Before each of the unit tests are ran, the testing framework makes a fresh connection to the web application. The framework then works through each of the steps to interact with the features, and expects certain values to be present along the way. If, at any time during the navigation associated with a particular feature, the web page displays incorrectly, the test fails. NOTE: Each of the unit tests are ran in 3 different browsers: Firefox, Chrome, and Safari.

### UNIT TEST CASES
**NOTE**: Each of the unit test cases will be displayed here once each of the features is implemented. The current unit test creation progress can be viewed [here](tests/test_frontend.py).

| \#  | NAME | OBJECTIVE | EXPECTED RESULTS |
| --- | --------- | ----- | ---------------- | 
| 1   |  test_page_name | Ensure successful connection to web-app | expects the page title to equal "Shadow Suite" (title will change in the future) |
| 2   |  test_url_encoder_decoder | TBD | TBD |
| 3   |  test_http_header_tool | TBD | TBD |
| 4   |  test_reverse_ip | TBD | TBD |
| 5   |  test_certificate_lookup | TBD | TBD |
| 6   |  test_subnet_scanner | TBD | TBD |
| 7   |  test_wget | TBD | TBD |
| 8   |  test_password_complexity | TBD | TBD |
| 9   |  test_ns_lookup | TBD | TBD |
| 10   |  test_ping | TBD | TBD |
| 11  |  test_whois_lookup | TBD | TBD |
| 12   |  test_what_is_my_ip | TBD | TBD |
| 13   |  test_traceroute_visualizer | TBD | TBD |
| 14  |  test_password_generator | TBD | TBD |

## INTEGRATION TEST SECTION

Combine individual software modules and test as a group.

### INTEGRATION TEST STRATEGY AND EXTENT OF INTEGRATION TESTING

- Netulla utilizes a GitHub workflow to perform full integration tests. This workflow is triggered every time a pull request is opened, edited, synchronized, or reopened. The following steps run on each trigger of the workflow:
  1. A new Ubuntu runner is created/obtained for the purposes of running our tests. The following actions will take place in the context of this runner.
  2. The code that is intended to be merged is checked out by the workflow. This ensures the most up-to-date code is used in the integration test.
  3. We install the dependencies needed to run Python linting ("the process of performing static analysis on source code to flag patterns that might cause errors or other problems"), along with the tools needed to annotate our GitHub pull requests. Additionally, we utilize a GitHub action that allows our tests to continue when there are linting warnings. This allows our pull requests to be annotated and our tests to be run without exiting on warnings. 
  4. We run the python linter and gather the warnings/errors. They are then annotated in the pull request.
  5. Install the dependencies for docker compose. This is used to create a container for our application to run in.
  6. Start the container. This initializes the application and allows it to be navigated to on port 8501.
  7. Install the browser dependencies needed by playwright, our browser testing platform.
  8. Install the browsers.
  9. Run the pytests that we have created for each of our features.
  10. If any tests fail, the failing test will generate a screenshot that is available as an artifact of the GitHub workflow.
