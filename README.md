# Netulla

This document is the User Guide for Netulla, A web-based suite of multi-functional network and password tools hosted [here](https://netulla.streamlit.app/). Below, you will find descriptions of the features available, and how to use them.

### Authors:

- [William Weir](https://github.com/TheSirLancelot), Team Lead
- [Tyler Wilson](https://github.com/nevermore23274), Software Engineer
- [Tristan Young](https://github.com/tyoung-99), Software Engineer
- [Oscar Vasquez Flores](https://github.com/oavf15), Software Engineer
- [Reynaldo Veras](https://github.com/Rey41888), Software Engineer
- [Tyree Maeser](https://github.com/Tymaze3), Software Engineer
- Joshua Welch, N/A [^1]

[^1]: Joshua Welch was assigned to our group, but was not present during the semester.

# Table of Contents

- [Network Tools](#network-tools)
  - [Traceroute Visualizer](#traceroute-visualizer)
  - [NS Lookup](#ns-lookup)
  - [Certificate Lookup](#certificate-lookup)
  - [Subnet Scan](#subnet-scan)
  - [IP Geolocation](#ip-geolocation)
  - [Network Analysis](#network-analysis)
  - [Subnet Calculator](#subnet-calculator)
  - [Whois Lookup](#whois-lookup)
  - [HTTP Header Tool](#http-header-tool)
  - [Online WGET Tool](#online-wget-tool)
  - [Ping](#ping)
  - [What is my IP?](#what-is-my-ip)
  - [URL Encoder and Decoder](#url-encoder-and-decoder)
  - [Regex tester](#regex-tester)
- [Password Tools](#password-tools)
  - [Password Complexity Checker](#password-complexity-checker)
  - [Password Generator](#password-generator)

# Network Tools

## Traceroute Visualizer

- Author: [Tyler Wilson](https://github.com/nevermore23274)
- Description: The Traceroute Visualizer tool is an advanced tool that combines the functionality of traceroute and visual mapping to display the path that internet data packets take from the user's device to a specified target IP address or domain. This tool leverages the capabilities of the mtr command (a network diagnostic tool that combines ping and traceroute) and visualizes the data path using an interactive map.
- Usage:
  1. From the Netulla home page, click the Traceroute Visualizer link in the sidebar.
  2. When on the tools page, enter an IP or domain name (8.8.8.8, google.com, etc.) in the text bar.
  3. If you don't want to see the raw output of the MTR command, click on the check-box off as it defaults to showing it.
  4. Press enter after entering in the domain or IP, and adjust the slide bar if you'd like more granular circles.
  5. If you'd like to perform another or different traceroute, replace the domain or IP in the search field and press enter again.

## NS lookup

- Author: [Oscar Vasquez-Flores](https://github.com/oavf15)
- Description: The NS Lookup tool allows you to perform Domain Name System (DNS) lookups to retrieve information about a specific domain. You can obtain details such as IP addresses associated with the domain and its corresponding hostname.
- Usage:
  1. From the Netulla home page, click the NS Lookup link in the sidebar.
  2. In the tool, find the text input labeled "Enter Domain (e.g., google.com)".
  3. To perform a lookup, enter the domain name you want to query into this text field (e.g., "google.com").
  4. After entering the domain, press Enter.
  5. After performing the lookup, the tool will display validation status, IP addresses associated with the domain, and its hostname (reverse lookup).
  6. The tool provides error messages for issues like no DNS records found, domain non-existence, timeouts, or other DNS-related errors.
  7. To perform lookups for different domains, replace the domain name in the text input field and submit the query again.

## Certificate Lookup

- Author: [Tyree Maeser](https://github.com/Tymaze3)
- Description: The Certificate Lookup tool provides a user-friendly interface to retrieve detailed information about SSL certificates for a given URL. SSL certificates play a critical role in securing online communication by encrypting data and ensuring the authenticity of websites. This tool empowers users to inspect the specifics of a website's SSL certificate, offering transparency and security awareness.
- Usage:
  1. From the Netulla home page, click the Certificate Lookup link in the sidebar.
  2. Enter the Domain name in the format of ‘example.com’, and hit “Get Certificate.”
  3. Upon successful execution, the SSL certificate information for the entered domain will be displayed. Information includes details about the SSL certificate, such as its validity period and issuer.
  4. If an issue occurs during the certificate lookup, error messages will be displayed.
  5. To lookup another certificate you will need to erase your original URL, then add a new one and hit "Get Certificate."

## Subnet Scan

- Author: [Tristan Young](https://github.com/tyoung-99)
- Description: This tool scans a subnetwork to determine the location of each webserver on it. This involves breaking apart the IP into its network ID and host ID, then iterating through every possible host ID using the same network ID. This allows the tool to identify and locate every possible host on the subnet.
- Usage:
  1. From the Netulla home page, click the Subnet Scanner link in the sidebar.
  2. Enter an IP address in the subnet you would like to scan and press `Enter`.
  3. If the IP address entered is valid, the tool will scan the subnet and identify the location of each webserver, then display the results below.
     - The results are displayed both on a navigable map of the world, and in a table listed by IP, city, and country.
  4. To scan additional subnets, replace the data entered in the text box and press `Enter` again.

## Network Analysis

- Author:
- Description:
- Usage:

## Subnet Calculator

- Author: [Tyler Wilson](https://github.com/nevermore23274)
- Description: This tool is an intuitive tool designed to assist in understanding and planning network subnets. It provides a detailed breakdown of subnet information based on an IP address and a CIDR (Classless Inter-Domain Routing) notation input.
- Usage:
  1. From the Netulla home page, click the Subnet Calculator link in the sidebar.
  2. Enter in the desired IPv4 address into the text field.
  3. Select the CIDR range (/24 is default).
  4. Press enter, scroll as needed to view the information for the subnet.
  5. If you'd like to calculate for a different subnet, replace the IPv4 address in the text area and press enter again. (ensure you change the CIDR if needed)

## Whois Lookup

- Author: [William Weir](https://github.com/TheSirLancelot)
- Description: Whois is a widely used Internet record listing that identifies who owns a domain and how to get in contact with them. The Internet Corporation for Assigned Names and Numbers (ICANN) regulates domain name registration and ownership. Whois records have proven to be extremely useful and have developed into an essential resource for maintaining the integrity of the domain name registration and website ownership process. A Whois record contains all of the contact information associated with the person, group, or company that registers a particular domain name. Typically, each Whois record will contain information such as the name and contact information of the Registrant (who owns the domain), the name and contact information of the Registrar (the organization or commercial entity that registered the domain name), the registration dates, the name servers, the most recent update, and the expiration date. Whois records may also provide the administrative and technical contact information (which is often, but not always, the registrant).
- Usage:
  1. From the Netulla home page, click the Whois Lookup Tool link in the sidebar.
  2. Enter the IP address or domain name you would like to get the whois information for and hit `Enter`.
  3. Your results should be displayed if you entered a legitimate IP address. If the domain you entered has whois information, it will be displayed. If no whois information can be found for your domain, a blank whois entry will be displayed.
  4. To receive information for additional IP addresses or domains, simply erase your previous entry and type a new one, then hit `Enter`.

## HTTP Header Tool

- Author: [Tristan Young](https://github.com/tyoung-99)
- Description: This tool retrieves and displays the HTTP response headers from a server, based on a URL or IP. HTTP response headers provide additional information about the response being sent back from the server. This can include the server type or location, policies related to the server or response, the date and time of the response, and a variety of other information.
- Usage:
  1. From the Netulla home page, click the Http Header Tool link in the sidebar.
  2. Enter the URL or IP address you would like to get the headers from and click the "Send Request" button. (Make sure to include "http://" or "https://" when entering a URL.)
  3. If the URL or IP address entered is valid, that site's headers will be displayed below.
  4. To make additional requests, replace the data entered in the text box and click "Send Request" again.

## Online cURL Tool

- Author:[Tyree Maeser](https://github.com/Tymaze3)
- Description: The Online Curl Tool provides users with a convenient interface to execute cURL requests directly within the Streamlit app. cURL is a command-line tool widely used for making HTTP requests and retrieving data from the web. This tool allows users to effortlessly interact with cURL without needing to navigate the command line.
- Usage:
  1. From the Netulla home page, click the Online Curl Tool link in the sidebar.
  2. Enter the URL in the format of https://www.example.com, http:// is also an acceptable way to start your URL. Click the "Send Curl Request" button to initiate the cURL request to the specified URL
  3. Upon successful execution, the cURL response will be displayed below the input field. The response is presented in a code block with syntax highlighting for improved readability.
  4. If an issue occurs during the cURL request, error messages will be displayed.
  5. To make another Curl request simply erase the URL you entered and add a new one and hit "Send Curl Request."

## Website Ping

- Author: [Tristan Young](https://github.com/tyoung-99)
- Description: This tool attempts to ping a website to determine if it is up or down. If it is up, it can also determine if there may be difficulties accessing the site due to the level of success in pinging it. Pinging a website involves attempting to send data to it and waiting for a response to that data. If the server replies to all attempts, the test was successful and the website is up. If the server replies to no attempts, the test has failed and the website is down. If the server replied to some, but not all, attempts, there will likely be problems accessing the site.
- Usage:
  1. From the Netulla home page, click the Website Ping link in the sidebar.
  2. Enter the domain name or IP address you would like to ping and press `Enter`. (Make sure to use just a domain, not a full URL, for example - google.com.)
  3. If the domain or IP address entered is valid, the tool will attempt to ping it and will display the result below.
     - The overall result is displayed primarily. To see the individual ping attempts, click the "See individual replies" box to expand it.
  4. To ping additional websites, replace the data entered in the text box and press `Enter` again.

## What Is My IP

- Author: [Tyler Wilson](https://github.com/nevermore23274)
- Description: This tool is designed to provide users with detailed information about their public IP address and its geolocation. The tool first fetches the user's public IP address using an external service. Once the IP address is acquired, the tool then retrieves the geolocation data associated with that IP, including latitude and longitude.
- Usage:
  1. From the Netulla home page, click on Ip Geolocation.
  2. The information for your current location (including latitude and logitude) will be displayed as well as the location on a map.

## URL Encoder and Decoder

- Author:
- Description:
- Usage:

## Regex Tester

- Author: Reynaldo Veras
- Description: This app is designed to assist users in testing regular expressions (regex) against input data. It provides a straightforward interface where users can input a regex pattern and test it against specific data. The app then displays the matched portions of the input data based on the provided regex pattern, aiding users in validating and refining their regex expressions.
- Usage:
- 1. From the Netulla home page, click the Regex Tester link in the sidebar.
  2. Users are then prompted to input a regex pattern and the corresponding data they want to test.
  3. Users can initiate the testing process by clicking the "Test Regex" button after entering the required information.
  4. The app will then execute the regex pattern against the input data and present the matched portions, providing a helpful tool for users working with regular expressions.
  5. To execute with another regex pattern, input data, or both, edit the text in the appropriate box and click "Test Regex" again.

# Password Tools

## Password Complexity Checker

- Author: Reynaldo Veras
- Description: This feature is designed to assess the strength of a given password. It employs a set of criteria to categorize passwords into different levels, such as "Unacceptable," "Weak," "Meh," and "Strong," based on their complexity. This functionality aids users in creating secure and robust passwords by providing instant feedback on the strength of their input.
- Usage:
- 1. From the Netulla home page, click on Password Complexity.
  2. Input a password in the provided text field and press the "Enter" key.
  3. The app will then analyze the password and display its complexity level.
  4. This feature is beneficial for individuals seeking to enhance the security of their accounts by generating passwords that meet higher complexity standards.
  5. To analyze a new password, enter a new one and press the "Enter" key again.

## Password Generator

- Author: [Tyler Wilson](https://github.com/nevermore23274)
- Description: This tool is a user-friendly application designed to create secure and customizable passwords. You can create up to 10 passwords per button press with varying levels of complexity.
- Usage:
  1. From the Netulla home page, click on Password Generator.
  2. First, adjust the slider (values between 6 and 20) to the exact number of characters you'd like the password to have.
  3. Check the different boxes for which values you'd like for the password to have.
  4. Edit the number in the text entry field to decide how many passwords (up to 10) will be generated.
  5. Click on "Generate Passwords" button.
  6. If you'd like to have the passwords regenerated, click "Generate Passwords" as many times as needed until you're satisfied.
