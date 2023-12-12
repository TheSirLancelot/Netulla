# Netulla Final Report

**Members:**

-   William Weir, Team Lead
-   Tyler Wilson, Software Engineer
-   Tristan Young, Software Engineer
-   Oscar Vasquez Flores, Software Engineer
-   Reynaldo Veras, Software Engineer
-   Tyree Maeser, Software Engineer
-   Joshua Welch, N/A [^1]

[^1]: Joshua Welch was assigned to our group, but was not present during the semester.

## Overview, Summary of Individual Contributions, and Development Plan
-   This project is a network-tools suite that provides the user a myriad of mini-applications via the web.

### Phase 1 (21 Nov 2023)

| Task                                       | Assignee             | Description                                      |
| ------------------------------------------ | -------------------- | ------------------------------------------------ |
| <li>- [x] Traceroute Visualizer</li>       | Tyler Wilson         | Shows traceroute hops on a map                   |
| <li>- [x] NS lookup</li>                   | Oscar Vasquez Flores | DNS record lookup                                |
| <li>- [x] Password complexity checker</li> | Reynaldo Veras       | Checks the strength of a user's password         |
| <li>- [x] Certificate Lookup</li>          | Tyree Maeser         | Displays a website's SSL Certificate information |
| <li>- [x] Subnet Scan</li>                 | Tristan Young        | Scans a subnet to identify webservers            |

### Phase 2 (28 Nov 2023)

| Task                              | Assignee      | Description                                           |
| --------------------------------- | ------------- | ----------------------------------------------------- |
| <li>- [x] WHOIS</li>              | William Weir  | Queries registration information for an IP address    |
| <li>- [x] Password Generator</li> | Tyler Wilson  | Generates a password using specified complexity rules |
| <li>- [x] HTTP Header Tool</li>   | Tristan Young | Inspect a server's HTTP response header               |
| <li>- [x] Online Curl Tool</li>   | Tyree Maeser  | Display a website without rendering it                |

### Phase 3 (05 Dec 2023)

| Task                                   | Assignee             | Description                                               |
| -------------------------------------- | -------------------- | --------------------------------------------------------- |
| <li>- [x] Ping</li>                    | Tristan Young        | See if a website is up right now                          |
| <li>- [x] What is my IP</li>           | Tyler Wilson         | Identify the user's current IP and geolocation info       |
| <li>- [x] URL Encoder/Decoder</li>     | William Weir         | URL encode/decode a string                                |
| <li>- [x] Regex Tester</li>            | Reynaldo Veras       | Perform matching with user-given regex on user-given data |
| <li>- [x] Accessibility Assurance</li> | Oscar Vasquez Flores | Ensures we are meeting the WCAG guidelines                |

## Project Design
## 1. Considerations

#### 1.1 Assumptions

The main assumptions with this application are that a) the user will have an active internet connection, b) the repository that the code is saved to remains available, and c) the hosting site that we are using remains free and available.

#### 1.2 Constraints

Our main constraint is that our entire application is run from a docker container. If, for whatever reason, there is a feature that we need added that has trouble functioning in that environment, we will need to find workarounds. Additionally, as mentioned in the assumptions section, we require our code to be saved in the GitHub repository that is targeted by the hosting site. If that connection is no longer available, we will need to find other hosting means.

#### 1.3 System Environment

The main system environment is the docker container that everything is run from. The docker container has all dependencies installed in it during creation. Our second system environment is the GitHub repository. There are two branches that are regularly utilized for development: main and dev. The main branch is what the hosting site is using for the code on our website. The dev branch, once development on a feature is complete and has passed all tests and reviews, is merged into main to ensure that the website is always feature-complete and functioning properly. Finally, we utilize a free hosting service provided by Streamlit's own [website](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app). (Note: Streamlit is the main python package that is being used to develop the web-application)

## 2. Architecture

#### 2.1 Overview

The web-application has a main "splash screen" with a dropdown box that displays the current tool categories that are available. Once a tool category is selected, the user is shown the selection of specific tools in that category, a selection can be made, and the user may begin using the chosen tool.

#### 2.2 Diagrams

![image](https://github.com/TheSirLancelot/Netulla/assets/22830818/552adb78-105c-4dc3-9e93-a41bc62ae90c)

## Test Plan
- Our full test plan can be found [here](https://github.com/TheSirLancelot/Netulla/blob/dev/TestPlan.md).

## Development History
- The following shows the amount of commits over the duration of the project (top graph) and the days that we committed to the project the most during the week (bottom graph). 
![image](https://github.com/TheSirLancelot/Netulla/assets/22830818/5528fb06-5a76-4912-ae9d-a0b04094a629)

## Conclusion
### Lessons Learned
- Set internal timelines but stick to them.
- Hold each other accountable

### Design Strengths/Weaknesses
- The tool, as a whole, is very feature-rich, but each feature was designed to be lightweight
- There were slight issues with dependencies when dealing with the three environments we were working with (local development environment(s), github workflow environment (for integration testing), and our hosted website). We have identified a solution that would work if this project was going to be released into production.

### Course Suggestions
- Maybe not specifically a course suggestion, but a Computer Science degree program suggestion at UMGC: For many, this was the first interaction with **integral** parts of software development in today's world. Specifically, git/version control mechanisms like pull requests, merges, etc. Additionally, there were no substantial discussions on the types of project management solutions that are used in today's software development (agile, waterfall, etc.). Obviously, we cannot speak for the other teams that were participating in this class, but if there had not been several people on the team with the requisite knowledge to properly plan and execute a project management solution, we are not sure how this project would have been completed. We **highly** suggest integrating some sort of introduction to these key parts of computer science into the degree program.
