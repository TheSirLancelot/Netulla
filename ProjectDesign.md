# Design Document
## Members
-   William Weir, Team Lead
-   Tyler Wilson, Software Engineer
-   Tristan Young, Software Engineer
-   Oscar Vasquez Flores, Software Engineer
-   Reynaldo Veras, Software Engineer
-   Tyree Maeser, Software Engineer
-   Joshua Welch, N/A [^1]

[^1]: Joshua Welch was assigned to our group, but was not present during the semester.


## 1. Considerations


#### 1.1 Assumptions
The main assumptions with this application are that a) the user will have an active internet connection, b) the repository that the code is saved to remains available, and b) the hosting site that we are using remains free and available. 

#### 1.2 Constraints
Our main constraint is that our entire application is run from a docker container. If, for whatever reason, there is a feature that we need added that has trouble functioning in that environment, we will need to find workarounds. Additionally, as mentioned in the assumptions section, we require our code to be saved in the GitHub repository that is targeted by the hosting site. If that connection is no longer available, we will need to find other hosting means. 

#### 1.3 System Environment
The main system environment is the docker container that everything is run from. The docker container has all dependencies installed in it during creation. Our second system environment is the GitHub repository. There are two branches that are regularly utilized for development: main and dev. The main branch is what the hosting site is using for the code on our website. The dev branch, once development on a feature is complete and has passed all tests and reviews, is merged into main to ensure that the website is always feature-complete and functioning properly. Finally, we utilize a free hosting service provided by Streamlit's own [website](https://docs.streamlit.io/streamlit-community-cloud/deploy-your-app). (Note: Streamlit is the main python package that is being used to develop the web-application)

## 2. Architecture


#### 2.1 Overview
The web-application has a main "splash screen" with a dropdown box that displays the current tool categories that are available. Once a tool category is selected, the user is shown the selection of specific tools in that category, a selection can be made, and the user may begin using the chosen tool. 

#### 2.2 Diagrams
![image](https://github.com/TheSirLancelot/Netulla/assets/22830818/552adb78-105c-4dc3-9e93-a41bc62ae90c)

## 3. Answers to Feedback
We received feedback from our Project Plan and we would like to take some time to provide our answers:

1. How are you going to implement testing for your application:  SAST and DAST what solution will you use?
   We utilize complete integration testing during each of our Pull Requests, as well as python linting for static analysis. By doing this, we are conducting both static _and_ dynamic testing. More information on the specifics of our integration testing and linting can be found in our [Test Plan](https://github.com/TheSirLancelot/Netulla/blob/dev/TestPlan.md).
2. Will you use ChatGpT?
   There are no features that utilize ChatGPT at this time.
3. Host: where will your program reside on AWS, AZURE or the Data Center?
   Our web-application is hosted via StreamLit. They offer the ability to deploy applications written with their package through a connection with the GitHub repository the application is saved to. This is a free service.
4. Will your users have a feature to upload images? receipts etc.
   There are no features that allow/require the user to upload images at this time.
5. How will you secure the data? Data in transit and Data at REST?
   We do not store any of our user's information, and there are no log ins required, therefor we do not have the need to secure data. 
6. What about IP protection? how will you protect your IP
   Our IP address is protected via Streamlit's own infrastructure. There is no need for added protections from our end.

## 4 Appendices and References

#### 4.1 Definitions and Abbreviations
- Docker: Docker is a set of platform as a service products that use OS-level virtualization to deliver software in packages called containers. The service has both free and premium tiers. The software that hosts the containers is called Docker Engine.
- Streamlit: Streamlit is a free and open-source framework to rapidly build and share beautiful machine learning and data science web apps. It is a Python-based library specifically designed for machine learning engineers.
- Linting: Lint is the computer science term for a static code analysis tool used to flag programming errors, bugs, stylistic errors and suspicious constructs. The term originates from a Unix utility that examined C language source code. A program which performs this function is also known as a "linter".

#### 4.2 References
[Project Design Template](https://github.com/imayobrown/DesignDocumentTemplates/blob/master/DesignDocument.md)https://github.com/imayobrown/DesignDocumentTemplates/blob/master/DesignDocument.md
