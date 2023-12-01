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

- Author:
- Description:
- Usage:

## NS lookup

- Author:
- Description:
- Usage:

## Certificate Lookup

- Author: [Tyree Maeser](https://github.com/Tymaze3)
- Description: The Certificate Lookup tool provides a user-friendly interface to retrieve detailed information about SSL certificates for a given URL. SSL certificates play a critical role in securing online communication by encrypting data and ensuring the authenticity of websites. This tool empowers users to inspect the specifics of a website's SSL certificate, offering transparency and security awareness.
- Usage:
  1. From the Netulla home page, click the Certificate Lookup Tool link in the sidebar.
  2. Enter the URL in the format of  ‘example.com’, and hit “Get Certificate.”
  3. Upon successful execution, the SSL certificate information for the entered domain will be displayed. Information includes details about the SSL certificate, such as its validity period and issuer.
  4. If an issue occurs during the certificate lookup, error messages will be displayed.

## Subnet Scan

- Author: [Tristan Young](https://github.com/tyoung-99)
- Description: This tool scans a subnetwork to determine the location of each webserver on it. This involves breaking apart the IP into its network ID and host ID, then iterating through every possible host ID using the same network ID. This allows the tool to identify and locate every possible host on the subnet.
- Usage:
  1. From the Netulla home page, click the Subnet Scanner link in the sidebar.
  2. Enter an IP address in the subnet you would like to scan and press `Enter`.
  3. If the IP address entered is valid, the tool will scan the subnet and identify the location of each webserver, then display the results below.
     - The results are displayed both on a navigable map of the world, and in a table listed by IP, city, and country.
  4. To scan additional subnets, replace the data entered in the text box and press `Enter` again.

## IP Geolocation

- Author:
- Description:
- Usage:

## Network Analysis

- Author:
- Description:
- Usage:

## Subnet Calculator

- Author:
- Description:
- Usage:

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

- Author:
- Description:
- Usage:

## URL Encoder and Decoder

- Author:
- Description:
- Usage:

## Regex Tester

- Author:
- Description:
- Usage:

# Password Tools

## Password Complexity Checker

- Author:
- Description:
- Usage:

## Password Generator

- Author:
- Description:
- Usage:
