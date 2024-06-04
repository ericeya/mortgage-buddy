# LensConnect
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54)
 
## Description

This is a terminal app program that helps you calculate mortgage payment based on loan amount. There's also options for more sophisticated calculation based on the price of the house that you're trying to buy which takes in factors of location / LTV for more accurate estimate of total PITIA (principal, interest, taxes, insurance, association fees).

## Table of Contents (Optional)

- [Installation](#installation)
- [Usage](#usage)
- [Credits](#credits)
- [Features](#features)
- [Questions](#questions)

## Installation
You may run this in your terminal directly or download the `mortgage-buddy.exe` file to simply double click the `.exe` file.
You can click on release on the right side, or [click here](https://github.com/ericeya/mortgage-buddy/releases/tag/mortgage-buddy) that will take you to the download release page. Then click on `mortgage-buddy.exe` file to download for use.

_Windows may give you a warning for running this file but I assure you, there's no malware nor any harmful content in the file._

## Usage
Choose the menu option of your choice:
<p align="center">
  <img alt="menu option screenshot" src="./sample-images/Screenshot 2024-06-04 134347.png" />
</p>

Answer the prompted questions:
<p align="center">
  <img alt="Gif of login/signup process" src="./sample-images/Screenshot 2024-06-04 134520.png" />
</p>


The questions for loan qualification prompts you to answer many questions. You can roughly estimate your responses to get rough estimates. Having a background of mortgage underwriter, I have written this script to properly analyze user's financial situation to see loan qualification for **conventional mortgage program**. This does not include any other mortgage programs such as Non-QM, government programs, or other high-balance loan programs. Contact your local mortgage broker or bank for consultation if you want to check your qualification for other loan programs.

## Credits

Application developers:

* <a href="https://github.com/ericeya"> Eric Lee </a>


## Features

Web scraping is utilized using `beautifulsoup4` library to grab current national average rate for mortgage from [bankrate.com](https://bankrate.com). Mortgage insurance premium rate is dated as of Dec 2023. Should there be any changes in mortgage insurance premium rates, then the estimate may not be accurate (please reach out to me if something seems off, so that I can update the application).

## Questions

Any questions please reach-out to me: 

* Eric Lee: Eric.hyunil.lee@gmail.com