def get_full_state_name(short_name):
    state_names_map = {}
    state_names_map['AL'] = 'Alabama'
    state_names_map['AK'] = 'Alaska'
    state_names_map['AZ'] = 'Arizona'
    state_names_map['AR'] = 'Arkansas'
    state_names_map['CA'] = 'California'
    state_names_map['CO'] = 'Colorado'
    state_names_map['CT'] = 'Connecticut'
    state_names_map['DE'] = 'Delaware'
    state_names_map['FL'] = 'Florida'
    state_names_map['GA'] = 'Georgia'
    state_names_map['HI'] = 'Hawaii'
    state_names_map['ID'] = 'Idaho'
    state_names_map['IL'] = 'Illinois'
    state_names_map['IN'] = 'Indiana'
    state_names_map['IA'] = 'Iowa'
    state_names_map['KS'] = 'Kansas'
    state_names_map['KY'] = 'Kentucky'
    state_names_map['LA'] = 'Louisiana'
    state_names_map['ME'] = 'Maine'
    state_names_map['MD'] = 'Maryland'
    state_names_map['MA'] = 'Massachusetts'
    state_names_map['MI'] = 'Michigan'
    state_names_map['MN'] = 'Minnesota'
    state_names_map['MS'] = 'Mississippi'
    state_names_map['MO'] = 'Missouri'
    state_names_map['MT'] = 'Montana'
    state_names_map['NE'] = 'Nebraska'
    state_names_map['NV'] = 'Nevada'
    state_names_map['NH'] = 'New Hampshire'
    state_names_map['NJ'] = 'New Jersey'
    state_names_map['NM'] = 'New Mexico'
    state_names_map['NY'] = 'New York'
    state_names_map['NC'] = 'North Carolina'
    state_names_map['ND'] = 'North Dakota'
    state_names_map['OH'] = 'Ohio'
    state_names_map['OK'] = 'Oklahoma'
    state_names_map['OR'] = 'Oregon'
    state_names_map['PA'] = 'Pennsylvania'
    state_names_map['RI'] = 'Rhode Island'
    state_names_map['SC'] = 'South Carolina'
    state_names_map['SD'] = 'South Dakota'
    state_names_map['TN'] = 'Tennessee'
    state_names_map['TX'] = 'Texas'
    state_names_map['UT'] = 'Utah'
    state_names_map['VT'] = 'Vermont'
    state_names_map['VA'] = 'Virginia'
    state_names_map['WA'] = 'Washington'
    state_names_map['WV'] = 'West Virginia'
    state_names_map['WI'] = 'Wisconsin'
    state_names_map['WY'] = 'Wyoming'
    state_names_map['DC'] = 'District of Columbia'
    state_names_map['MH'] = 'Marshall Islands'

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
            line_parts_cleaned = list(map(lambda part: part.strip('\"'), line_parts))
            zipcode = line_parts_cleaned[1]
            city = line_parts_cleaned[2]
            state_code = line_parts_cleaned[3]
            state = get_full_state_name(state_code)
            if state is None:
                continue
            else:
                url_info.append(UrlInfo(state, city, zipcode))

    return url_info

def get_url_info_state_code():
    url_info = []
    with open("Zip_Zhvi_Condominum.csv", "r") as csv_file:
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            line_parts_cleaned = list(map(lambda part: part.strip('\"'), line_parts))
            zipcode = line_parts_cleaned[1]
            city = line_parts_cleaned[2]
            state_code = line_parts_cleaned[3]
            state = state_code
            if state == "State":
                continue
            else:
                url_info.append(UrlInfo(state, city, zipcode))

    return url_info