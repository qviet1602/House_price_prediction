import requests
from bs4 import BeautifulSoup
from url_information import *


def parse_name_column(name_column):
    span_data = name_column.find_all("span", class_="sName")
    return span_data[0].get_text()


def parse_address_column(address_column):
    return address_column.get_text()


def parse_city_column(city_column):
    return city_column.get_text()


def parse_zipcode_column(zip_column):
    return zip_column.get_text()


def parse_county_column(county_column):
    return county_column.get_text()


def parse_average_standard_score(average_standard_column):
    return average_standard_column.get_text()


def parse_schooldigger_rating(schooldigger_rating_column):
    inner_span_data = schooldigger_rating_column.find_all("span", class_="starSpan")
    if len(inner_span_data) > 0:
        stars = inner_span_data[0].find_all("span", class_="glyphicon-star")

        return len(stars)

    return -1


def scrape_schooldigger():
    url_info_list = get_url_info_state_code()
    schools_csv_file = open("schools_data.csv", "a")
    schools_csv_file.write(
        "State,City,Zipcode,County,Address,School Name,Average Standard Score,SchoolDigger Rating"
    )
    schools_csv_file.write("\n")
    try:
        print()
        total = len(url_info_list)
        for i in range(total):
            info = url_info_list[i]
            url = (
                "https://www.schooldigger.com/go/"
                + info.get_state()
                + "/zip/"
                + info.get_zipcode()
                + "/search.aspx"
            )
            print("URL: ", url, " i:", i)
            html_page = requests.get(url)
            if html_page.status_code == 200:
                soup = BeautifulSoup(html_page.content, "html.parser")
                table_data = soup.find_all("table", id="tabSchooList")
                full_table = table_data[0]
                tbody_data = full_table.find_all("tbody")
                tbody_data_children = list(tbody_data[0].children)
                for each_row in tbody_data_children:
                    if each_row != "\n":
                        all_columns = list(each_row.children)
                        all_main_columns = []
                        for each_column in all_columns:
                            if each_column != "\n":
                                all_main_columns.append(each_column)

                        name_column = all_main_columns[0]
                        address_column = all_main_columns[3]
                        city_column = all_main_columns[4]
                        zip_column = all_main_columns[5]
                        county_column = all_main_columns[6]
                        average_standard_column = all_main_columns[24]
                        schooldigger_rating_column = all_main_columns[27]

                        city_value = parse_city_column(city_column)
                        zip_value = parse_zipcode_column(zip_column)
                        county_value = parse_county_column(county_column)
                        address_value = parse_address_column(address_column)
                        school_name = parse_name_column(name_column)
                        average_standard_value = parse_average_standard_score(
                            average_standard_column
                        )
                        schooldigger_rating_value = parse_schooldigger_rating(
                            schooldigger_rating_column
                        )

                        schools_csv_file.write(
                            info.get_state()
                            + ","
                            + city_value
                            + ","
                            + info.get_zipcode()
                            + ","
                            + county_value
                            + ","
                            + address_value
                            + ","
                            + school_name
                            + ","
                            + average_standard_value
                            + ","
                            + str(schooldigger_rating_value)
                        )
                        schools_csv_file.write("\n")
            else:
                print("Error ")
    finally:
        print()
        schools_csv_file.close()


scrape_schooldigger()
