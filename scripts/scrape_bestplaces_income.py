import requests
from bs4 import BeautifulSoup


def get_full_state_name(short_name):
    state_names_map = {}
    state_names_map["AL"] = "Alabama"
    state_names_map["AK"] = "Alaska"
    state_names_map["AZ"] = "Arizona"
    state_names_map["AR"] = "Arkansas"
    state_names_map["CA"] = "California"
    state_names_map["CO"] = "Colorado"
    state_names_map["CT"] = "Connecticut"
    state_names_map["DE"] = "Delaware"
    state_names_map["FL"] = "Florida"
    state_names_map["GA"] = "Georgia"
    state_names_map["HI"] = "Hawaii"
    state_names_map["ID"] = "Idaho"
    state_names_map["IL"] = "Illinois"
    state_names_map["IN"] = "Indiana"
    state_names_map["IA"] = "Iowa"
    state_names_map["KS"] = "Kansas"
    state_names_map["KY"] = "Kentucky"
    state_names_map["LA"] = "Louisiana"
    state_names_map["ME"] = "Maine"
    state_names_map["MD"] = "Maryland"
    state_names_map["MA"] = "Massachusetts"
    state_names_map["MI"] = "Michigan"
    state_names_map["MN"] = "Minnesota"
    state_names_map["MS"] = "Mississippi"
    state_names_map["MO"] = "Missouri"
    state_names_map["MT"] = "Montana"
    state_names_map["NE"] = "Nebraska"
    state_names_map["NV"] = "Nevada"
    state_names_map["NH"] = "New Hampshire"
    state_names_map["NJ"] = "New Jersey"
    state_names_map["NM"] = "New Mexico"
    state_names_map["NY"] = "New York"
    state_names_map["NC"] = "North Carolina"
    state_names_map["ND"] = "North Dakota"
    state_names_map["OH"] = "Ohio"
    state_names_map["OK"] = "Oklahoma"
    state_names_map["OR"] = "Oregon"
    state_names_map["PA"] = "Pennsylvania"
    state_names_map["RI"] = "Rhode Island"
    state_names_map["SC"] = "South Carolina"
    state_names_map["SD"] = "South Dakota"
    state_names_map["TN"] = "Tennessee"
    state_names_map["TX"] = "Texas"
    state_names_map["UT"] = "Utah"
    state_names_map["VT"] = "Vermont"
    state_names_map["VA"] = "Virginia"
    state_names_map["WA"] = "Washington"
    state_names_map["WV"] = "West Virginia"
    state_names_map["WI"] = "Wisconsin"
    state_names_map["WY"] = "Wyoming"
    state_names_map["DC"] = "District of Columbia"
    state_names_map["MH"] = "Marshall Islands"

    return state_names_map.get(short_name, None)


class UrlInfo:
    def __init__(self, state, city, zipcode):
        self.state = state
        self.city = city
        self.zipcode = zipcode

    def get_state(self):
        return self.state

    def get_city(self):
        return self.city

    def get_zipcode(self):
        return self.zipcode


def get_url_info():
    url_info = []
    zipcode_id_map = {}
    with open("data/zipcodes.csv", "r") as csv_file:
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            zipcode = line_parts[1]
            city = line_parts[2]
            state_code = line_parts[3]

            state = get_full_state_name(state_code)
            if state is None:
                continue
            else:
                url_info.append(UrlInfo(state, city, zipcode))

            zipcode_id_map[zipcode] = line_parts[0]

    return url_info, zipcode_id_map


def scrape_bestplaces_income():
    url_info_list, zipcode_id_map = get_url_info()
    income_data_csv_file = open("data/income_data.csv", "a")
    income_data_csv_file.write("Zipcode Id,Average Income,Median Income")
    income_data_csv_file.write("\n")
    try:
        total = len(url_info_list)
        print("Total ", total)
        for i in range(17728, total, 1):
            info = url_info_list[i]
            state = info.get_state().replace(" ", "%20")
            url = (
                "https://www.bestplaces.net/economy/zip-code/"
                + state
                + "/"
                + info.get_city()
                + "/"
                + info.get_zipcode()
            )
            # https://www.bestplaces.net/economy/zip-code/washington/bellevue/98006
            print("URL: ", url, " i:", i)
            html_page = requests.get(url)
            if html_page.status_code == 200:
                soup = BeautifulSoup(html_page.content, "html.parser")

                soup_list = soup.find_all("div", class_="col-md-7 mt-0")
                """Check for oops"""
                is_oops = False
                if len(soup_list) == 0:
                    is_oops = True
                if is_oops:
                    income_data_csv_file.write(zipcode_id_map.get(info.get_zipcode()))
                    income_data_csv_file.write(",")
                    income_data_csv_file.write("")
                    income_data_csv_file.write(",")
                    income_data_csv_file.write("")
                    income_data_csv_file.write("\n")
                else:
                    divs = soup_list[0].find_all("div")
                    first_p = divs[2].find_all("p")
                    if len(first_p) < 4:
                        continue
                    interested_elements = first_p[3].get_text()
                    split_values = interested_elements.split(".")
                    average_value = ""
                    median_value = ""
                    for each_split_value in split_values:
                        if "average income" in each_split_value:
                            average_value_idx = each_split_value.find(
                                "resident is $", 0, len(each_split_value)
                            )
                            if average_value_idx != -1:
                                average_value = each_split_value[
                                    average_value_idx + 13 :
                                ]
                                average_value = average_value.replace("a year", "")
                                average_value = average_value.replace(",", "")
                        if "Median household" in each_split_value:
                            median_value_idx = each_split_value.find(
                                "resident is $", 0, len(each_split_value)
                            )
                            if median_value_idx != -1:
                                median_value = each_split_value[median_value_idx + 13 :]
                                median_value = median_value.replace("a year", "")
                                median_value = median_value.replace(",", "")
                    income_data_csv_file.write(zipcode_id_map.get(info.get_zipcode()))
                    income_data_csv_file.write(",")
                    income_data_csv_file.write(average_value.strip() + "")
                    income_data_csv_file.write(",")
                    income_data_csv_file.write(median_value.strip() + "")
                    income_data_csv_file.write("\n")
                    print("AVG and Median", average_value, median_value)
            else:
                income_data_csv_file.write(zipcode_id_map.get(info.get_zipcode()))
                income_data_csv_file.write(",")
                income_data_csv_file.write("")
                income_data_csv_file.write(",")
                income_data_csv_file.write("")
                income_data_csv_file.write("\n")
    finally:
        income_data_csv_file.close()


scrape_bestplaces_income()
