# polovnjaci_scrap
**Project Overview: Polovni Automobili Scraper**
This project is a web scraping tool designed to extract car advertisement data from polovniautomobili.com, a popular Serbian website for buying and selling used cars. The tool gathers detailed information about each car listing and exports the data into an Excel file for easy analysis and further use.

**Key Features:**
-Ad and Page Count: Automatically calculates the total number of ads and pages to scrape.
-Detailed Ad Information: Extracts comprehensive details from each ad, such as location, price, condition, make, model, year, mileage, fuel type, and more.
-Data Export: Consolidates all scraped data into an Excel file with neatly organized columns.
-Error Handling: Incorporates robust error handling to manage network issues or page structure changes.
-Graceful Interruption Handling: Ensures data is saved even if the process is interrupted by the user or encounters an unexpected error.

**Technologies Used:**
-Python: The primary programming language for the project.
-Requests: For making HTTP requests to the website.
-BeautifulSoup: For parsing HTML and extracting the required data.
-OpenPyXL: For writing the scraped data to an Excel file.
-Logging: For logging the scraping process and handling errors effectively.

**How to Use:**
-Clone the repository.
-Install the required dependencies.
-Run the script to start scraping data.
-The output will be saved in an Excel file named ads_data.xlsx.

This tool is ideal for anyone looking to analyze car listings from polovniautomobili.com or integrate this data into larger projects or datasets.
