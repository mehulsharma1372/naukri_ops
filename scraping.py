"""This module contains function written to scrape the website of Naukri.com"""
import os
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import constants


class GetData:
    """This class is formed to get the data from the website via scraping."""

    def __init__(self):
        self.title = []
        self.links = []
        self.companies = []
        self.experience = []
        self.salary = []
        self.location = []
        self.final_dict = dict()

    def get_authentication(self, url):
        """This function is responsible for getting authentication and establish a connection."""
        driver = webdriver.Edge(executable_path=constants.DRIVER_PATH)
        driver.get(url)
        soup = BeautifulSoup(driver.page_source, constants.HTML_LIB)
        return soup

    def format_data(self):
        """This function filters the data and extract what's required."""
        i = 10  # Edit this if you want to scrape more or less pages.
        for j in range(1, i):
            url = os.path.join(constants.URL + str(j))
            soup = self.get_authentication(url)
            list = soup.find(constants.DIV_TAG, class_=constants.LIST_TAG)
            try:
                for article in list:
                    try:
                        title = article.find(constants.ANCHOR_TAG).text
                        self.title.append(title)
                        href = article.find(constants.ANCHOR_TAG)[constants.HREF]
                        self.links.append(href)

                        company = (
                            article.find(
                                constants.DIV_TAG, class_=constants.COMPANYINFO
                            )
                            .find(constants.ANCHOR_TAG)
                            .text
                        )
                        self.companies.append(company)
                        more = article.find(
                            constants.UL_TAG, class_=constants.NIL_CLASS
                        )
                        experience = more.find(
                            constants.LI_TAG, class_=constants.EXPERIENCE_TAG
                        ).text
                        self.experience.append(experience)
                        salary = more.find(
                            constants.LI_TAG, class_=constants.SALARY_TAG
                        ).text
                        self.salary.append(salary)
                        location = more.find(
                            constants.LI_TAG, class_=constants.LOCATION_TAG
                        ).text
                        self.location.append(location)

                    except:
                        pass

            except:
                pass

    def to_csv(self):
        """This function is responsible for converting the data in form dataframe and then further write it to csv."""
        self.format_data()
        self.final_dict[constants.TITLE] = self.title
        self.final_dict[constants.LINK] = self.links
        self.final_dict[constants.COMPANY] = self.companies
        self.final_dict[constants.EXPERIENCE] = self.experience
        self.final_dict[constants.SALARY] = self.salary
        self.final_dict[constants.LOCATION] = self.location
        dataframe = pd.DataFrame(self.final_dict)

        with open(constants.CSV_FILE_NAME, constants.WRITE) as csv:
            dataframe.to_csv(constants.CSV_FILE_NAME, index=False)


if __name__ == "__main__":
    hey = GetData()
    hey.to_csv()
