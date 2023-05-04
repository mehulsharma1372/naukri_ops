"""This is the main file which calls the scraping.py"""
import scraping

if __name__ == "__main__":
    hey = scraping.GetData()
    hey.to_csv()