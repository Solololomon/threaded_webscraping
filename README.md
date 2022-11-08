# threading_webscraping
A webscraper that shows the efficiency of using multiple threads.

The webscraper itself takes user input to build an IMDb query, and then returns
a table of films and information about those films using data scraped from the website.

Run nothread.py, and then run withthread.py. It will print the comparative times it took to
generate a table through web-scraping with and without using multiple threads.
