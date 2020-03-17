# _*_ coding: utf-8 _*_
# !/usr/bin/env python3

"""
Created on: 12/03/2020
@author: Collisio-Adolebitque

Gather confirmed COVID19 numbers from the UK & IE Gov web pages and send them to BigQuery.

Pre-reqs:
An active Google Cloud Platform account and subscription.
A configured GCP project.
Enabled BigQuery and Compute APIs.

Python requirements:
> pip3 install requests
> pip3 install beautifulsoup4
> pip3 install --upgrade google-cloud-bigquery

Ref:
https://cloud.google.com/bigquery/docs/reference/libraries#client-libraries-install-python
"""


import requests
import re
import datetime
from bs4 import BeautifulSoup
from google.cloud import bigquery


class WebScraper:
    def __init__(self):
        self.uk_url = 'https://www.publichealth.hscni.net/news/covid-19-coronavirus'
        self.ie_url = 'https://www.gov.ie/en/news/7e0924-latest-updates-on-covid-19-coronavirus/'

    def get_uk_updates(self) -> int:
        """
        Get the confirmed case numbers from the matching string on the NI page.
        :return: int
        """
        soup = self._get_covid19_updates(self.uk_url)
        confirmed_cases_string = self._find_string(soup, '^As of .*').split()
        confirmed_cases = confirmed_cases_string[-1]
        confirmed_cases = confirmed_cases.split('.')
        return int(confirmed_cases[0])

    def get_ie_updates(self) -> int:
        """
        Inconsistent messaging on the IE site requires multiple filters.
        :return: int
        """
        soup = self._get_covid19_updates(self.ie_url)
        confirmed_cases = []
        confirmed_cases_1 = self._find_string(soup, 'There have been .* deaths associated').split()
        confirmed_cases.append(int(confirmed_cases_1[13]))
        confirmed_cases_2 = self._find_string(soup, 'There are now .* cases of').split()
        confirmed_cases.append(int(confirmed_cases_2[3]))
        confirmed_cases_3 = self._find_string(soup, 'total number of cases in Ireland is').split()
        confirmed_cases.append(int(self._get_last_item(confirmed_cases_3)))
        confirmed_cases_4 = self._find_string(soup, 'This brings the total number of').split()
        confirmed_cases.append(int(self._get_last_item(confirmed_cases_4)))
        return self._get_largest_number(confirmed_cases)

    @staticmethod
    def _get_last_item(matched_string) -> int:
        """
        Output the confirmed case number when it's the last item in the string.
        :param matched_string:
        :return: int
        """
        last_item = matched_string[-1]
        remove_full_stop = last_item.split('.')
        return int(remove_full_stop[0])

    @staticmethod
    def _get_covid19_updates(url: str) -> BeautifulSoup:
        """
        Get the requested web page contents.
        :param url:
        :return: BeautifulSoup
        """
        page = requests.get(url)  # Get the COVID19 update page.
        soup = BeautifulSoup(page.text, 'html.parser')  # Create BeautifulSoup object to work off.
        return soup  # Return the page contents.

    @staticmethod
    def _find_string(soup: BeautifulSoup, regex: str) -> str:
        """
        Apply the RegEx pattern to the web page contents and return the match.
        :param soup:
        :param regex:
        :return: str
        """
        string = soup.find(text=re.compile(regex)).strip()
        return string

    @staticmethod
    def _get_largest_number(num_list: list) -> int:
        """
        Get the largest number from the array of IE site strings.
        :param num_list:
        :return: int
        """
        num_list.sort(reverse=True)
        return num_list[0]


class BigQuery:
    def __init__(self, project_id, dataset_name, table_id):
        self.project_id = project_id
        self.dataset_name = dataset_name
        self.dataset_id = f'{self.project_id}.{self.dataset_name}'
        self.table_id = table_id
        self.bq_client = bigquery.Client(project=self.project_id)

    def does_dataset_exist(self, dataset_id: str) -> bool:
        """
        Check if the BigQuery DataSet exists.
        :param dataset_id:
        :return: bool
        """
        try:
            self.bq_client.get_dataset(dataset_id)
            return True
        except Exception as err:
            print('{}'.format(err))
            return False

    def does_table_exist(self) -> bool:
        """
        Check if the BigQuery table exists.
        :return: bool
        """
        try:
            self.bq_client.get_table(f'{self.dataset_id}.{self.table_id}')
            return True
        except Exception as err:
            print('{}'.format(err))
            return False

    def does_record_exist(self, uk, ie):
        """
        Check if a matching record exists.  Needs work.
        :param uk:
        :param ie:
        :return: bool
        """
        dml_statement = f"SELECT * FROM `{self.dataset_id}.{self.table_id}` " \
                        f"WHERE Date='CURRENT_DATE' " \
                        f"AND NI_Confirmed={uk} " \
                        f"AND IE_Confirmed={ie} LIMIT 1"
        try:
            query_job = self.bq_client.query(dml_statement)
            is_exist = len(list(query_job.result())) >= 1
            return is_exist
        except Exception as err:
            print(err)
        return False

    def bq_create_dataset(self) -> str:
        """
        Construct a full Dataset object to send to the API, if it doesn't already exist.
        Specify the geographic location where the dataset should reside.
        Send the dataset to the API for creation.
        :return: str
        """
        dataset = bigquery.Dataset(self.dataset_id)
        dataset.location = "EU"
        dataset = self.bq_client.create_dataset(dataset)  # Make an API request.
        return "Created dataset {}.{}".format(self.bq_client.project, dataset.dataset_id)

    def bq_create_table(self) -> str:
        """
        Prepares a reference to the table.
        Create the table if it doesn't exist.
        :return: str
        """
        dataset_ref = self.bq_client.get_dataset(self.dataset_id)
        table_ref = dataset_ref.table(self.table_id)
        try:
            schema = [
                bigquery.SchemaField('Date', 'DATE', mode='REQUIRED', description='Date'),
                bigquery.SchemaField('NI_Confirmed', 'INTEGER', description='NI Confirmed Cases'),
                bigquery.SchemaField('NI_Dead', 'INTEGER', description='NI Confirmed Dead'),
                bigquery.SchemaField('IE_Confirmed', 'INTEGER', description='IE Confirmed Cases'),
                bigquery.SchemaField('IE_Dead', 'INTEGER', description='IE Confirmed Dead'),
            ]
            table = bigquery.Table(table_ref, schema=schema)
            table = self.bq_client.create_table(table)
            return f'table {table.table_id} created.'
        except Exception as err:
            return '{}'.format(err)

    def bq_add_updates(self, uk, ie) -> str:
        """
        Add the latest confirmed case numbers to the appropriate fields.
        TODO: Add confirmed death numbers.
        :param uk:
        :param ie:
        :return: str
        """
        dml_statement = (f"INSERT {self.dataset_name}.{self.table_id} "
                         f"(Date, NI_Confirmed, IE_Confirmed) VALUES "
                         f"(CURRENT_DATE, {uk}, {ie})")
        if not self.does_record_exist(uk, ie):
            query_job = self.bq_client.query(dml_statement)  # API request
            query_job.result()  # Waits for statement to finish
            return f"Added NI_Confirmed: {uk}, IE_Confirmed: {ie} to table: {self.table_id}."


def main(event) -> None:
    """
    Set the project, dataset and table names.
    Create BigQuery dataset if it doesn't exist.
    Create table if it doesn't exist.
    Add a new record.
    NB: Google Cloud Function passes a parameter (event) to the primary function.
    :return: None
    """
    project_id = 'covid19-20200312'
    dataset_name = 'covid_collector'
    table_id = 'uki_covid19_confirmed_cases'
    big_query = BigQuery(project_id, dataset_name, table_id)

    if not big_query.does_dataset_exist(f'{project_id}.{dataset_name}'):
        print('{}'.format(big_query.bq_create_dataset()))

    if not big_query.does_table_exist():
        print('{}'.format(big_query.bq_create_table()))

    web_scraper = WebScraper()
    print(big_query.bq_add_updates(web_scraper.get_uk_updates(),
                                   web_scraper.get_ie_updates()))


if __name__ == '__main__':
    main()
