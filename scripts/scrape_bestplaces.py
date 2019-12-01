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
    with open("Zip_Zhvi_Condominum.csv", "r") as csv_file:
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            line_parts_cleaned = list(map(lambda part: part.strip('"'), line_parts))
            zipcode = line_parts_cleaned[1]
            city = line_parts_cleaned[2]
            state_code = line_parts_cleaned[3]
            state = get_full_state_name(state_code)
            if state is None:
                continue
            else:
                url_info.append(UrlInfo(state, city, zipcode))

    return url_info


def scrape_bestplaces():
    url_info_list = get_url_info()
    crime_data_csv_file = open("crime_data.csv", "a")
    crime_data_csv_file.write("State,City,Zipcode,Violent Crime,Property Crime")
    crime_data_csv_file.write("\n")
    try:
        total = len(url_info_list)
        print("Total ", total)
        for i in range(total):
            info = url_info_list[i]
            state = info.get_state().replace(" ", "%20")
            city = info.get_city().replace(" ", "%20")
            url = (
                "https://www.bestplaces.net/crime/zip-code/"
                + state
                + "/"
                + city
                + "/"
                + info.get_zipcode()
            )
            print("URL: ", url, " i:", i)
            html_page = requests.get(url)
            if html_page.status_code == 200:
                soup = BeautifulSoup(html_page.content, "html.parser")

                soup_list = soup.find_all("div", class_="container")
                """Check for oops"""
                oops_stuff = soup_list[0].find_all("h3")
                is_oops = False
                if len(oops_stuff) != 0:
                    oops_text = oops_stuff[0].getText()
                    if "Oops" in oops_text:
                        crime_data_csv_file.write(info.get_state())
                        crime_data_csv_file.write(",")
                        crime_data_csv_file.write(info.get_city())
                        crime_data_csv_file.write(",")
                        crime_data_csv_file.write(info.get_zipcode())
                        crime_data_csv_file.write(",")
                        crime_data_csv_file.write("")
                        crime_data_csv_file.write(",")
                        crime_data_csv_file.write("")
                        crime_data_csv_file.write("\n")
                        is_oops = True
                if not is_oops:
                    first_div = soup_list[1].find_all("h5")
                    interested_elements = list(first_div)
                    item1 = interested_elements[0]
                    item2 = interested_elements[1]
                    item1_more_children = list(item1.children)
                    item2_more_children = list(item2.children)
                    violent_crime_index = item1_more_children[0].rfind("is")
                    property_crime_index = item2_more_children[0].rfind("is")
                    violent_crime = item1_more_children[0][violent_crime_index + 3 : -1]
                    property_crime = item2_more_children[0][
                        property_crime_index + 3 : -1
                    ]
                    crime_data_csv_file.write(info.get_state())
                    crime_data_csv_file.write(",")
                    crime_data_csv_file.write(info.get_city())
                    crime_data_csv_file.write(",")
                    crime_data_csv_file.write(info.get_zipcode())
                    crime_data_csv_file.write(",")
                    crime_data_csv_file.write(violent_crime + "")
                    crime_data_csv_file.write(",")
                    crime_data_csv_file.write(property_crime + "")
                    crime_data_csv_file.write("\n")
            else:
                crime_data_csv_file.write(info.get_state())
                crime_data_csv_file.write(",")
                crime_data_csv_file.write(info.get_city())
                crime_data_csv_file.write(",")
                crime_data_csv_file.write(info.get_zipcode())
                crime_data_csv_file.write(",")
                crime_data_csv_file.write("")
                crime_data_csv_file.write(",")
                crime_data_csv_file.write("")
                crime_data_csv_file.write("\n")
    finally:
        crime_data_csv_file.close()


def get_urls():
    url_info_list = get_url_info()
    url_list = []
    for info in url_info_list:
        url = (
            "https://www.bestplaces.net/crime/zip-code/"
            + info.get_state()
            + "/"
            + info.get_city()
            + "/"
            + info.get_zipcode()
        )
        url_list.append(url)

    return url_list


scrape_bestplaces()
