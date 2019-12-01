all_files = ["./data/ZRI/allSummary/Neighborhood_Zri_AllHomesPlusMultifamily_Summary.csv",
             "./data/ZRI/medianSFRCondo/Neighborhood_ZriPerSqft_AllHomes.csv",
             "./data/ZRI/sFRTimeSeries/Neighborhood_Zri_SingleFamilyResidenceRental.csv",
             "./data/ZRI/allHomesTimeSeries/Neighborhood_Zri_AllHomesPlusMultifamily.csv",
             "./data/ZRI/multiFamilyTimeSeries/Neighborhood_Zri_MultiFamilyResidenceRental.csv",
             "./data/rentalListings/medianRentListPriceSqFt_4bedroom/Neighborhood_MedianRentalPricePerSqft_4Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_sfrCondoCoop/Neighborhood_MedianRentalPrice_AllHomes.csv",
             "./data/rentalListings/medianRentListPriceSqFt_duplexTriplex/Neighborhood_MedianRentalPricePerSqft_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPriceSqFt_sFRCondoCoop/Neighborhood_MedianRentalPricePerSqft_AllHomes.csv",
             "./data/rentalListings/medianRentListPrice_condoCoop/Neighborhood_MedianRentalPrice_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_duplexTriplex/Neighborhood_MedianRentalPrice_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPrice_2bedroom/Neighborhood_MedianRentalPrice_2Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_2bedroom/Neighborhood_MedianRentalPricePerSqft_2Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_4bedroom/Neighborhood_MedianRentalPrice_4Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_singleFamilyResidence/Neighborhood_MedianRentalPricePerSqft_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_multiFamily/Neighborhood_MedianRentalPricePerSqft_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPrice_1bedroom/Neighborhood_MedianRentalPrice_1Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_5bedroom/Neighborhood_MedianRentalPricePerSqft_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_3bedroom/Neighborhood_MedianRentalPrice_3Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_5PlusBedroom/Neighborhood_MedianRentalPrice_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_singleFamilyResidence/Neighborhood_MedianRentalPrice_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_condoCoop/Neighborhood_MedianRentalPricePerSqft_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_multiFamily/Neighborhood_MedianRentalPrice_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPriceSqFt_3bedroom/Neighborhood_MedianRentalPricePerSqft_3Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_studio/Neighborhood_MedianRentalPricePerSqft_Studio.csv",
             "./data/rentalListings/medianRentListPrice_studio/Neighborhood_MedianRentalPrice_Studio.csv",
             "./data/rentalListings/medianRentListPriceSqFt_1bedroom/Neighborhood_MedianRentalPricePerSqft_1Bedroom.csv",
             "./data/ZHVI/singleFamilyHomeTimeSeries/Neighborhood_Zhvi_SingleFamilyResidence.csv",
             "./data/ZHVI/condoCoOpTimeSeries/Neighborhood_Zhvi_Condominum.csv",
             "./data/ZHVI/all_homes_condoCoOpTimeSeries/Neighborhood_Zhvi_AllHomes.csv",
             "./data/ZHVI/twoBedroomTimeSeries/Neighborhood_Zhvi_2bedroom.csv",
             "./data/ZHVI/threeBedroomTimeSeries/Neighborhood_Zhvi_3bedroom.csv",
             "./data/ZHVI/fivePlusBedroomTimeSeries/Neighborhood_Zhvi_5BedroomOrMore.csv",
             "./data/ZHVI/fourBedroomTimeSeries/Neighborhood_Zhvi_4bedroom.csv",
             "./data/ZHVI/medianPerSqFt/Neighborhood_MedianValuePerSqft_AllHomes.csv",
             "./data/ZHVI/oneBedroomTimeSeries/Neighborhood_Zhvi_1bedroom.csv",
             "./data/homeListings_Sales/medianListPrice/Neighborhood_MedianListingPrice_AllHomes.csv"
             ]

def break_into_line_parts_1(line):
    parts = []
    c_idx = 0
    while c_idx < len(line):
        if line[c_idx] != '\"':
            word = ""
            while line[c_idx] != ',':
                word += line[c_idx]
                c_idx += 1
                if c_idx >= len(line):
                    break
            parts.append(word)
            c_idx += 1
        else:
            word = ""
            c_idx += 1
            if c_idx >= len(line):
                break
            while line[c_idx] != '\"':
                word += line[c_idx]
                c_idx += 1
            next_idx = c_idx + 1
            if next_idx < len(line):
                if line[next_idx] == ',':
                    c_idx += 2
                else:
                    c_idx += 1
            parts.append(word)

    return parts

def break_into_line_parts(line):
    c_idx = 0
    word_end_idx = 0
    parts = []
    extra = 0
    print("Line ", line)
    while c_idx < len(line):
        word_begin_idx = c_idx
        if line[c_idx] == "\"":
            word_begin_idx = c_idx + 1
            c_idx += 1
            extra = 2
            end_char = "\""
        else:
            next_idx = c_idx + 1
            if next_idx >= len(line):
                break
            if line[next_idx] == "\"":
                c_idx += 1
                word_begin_idx = c_idx + 1
                c_idx += 1
                end_char = "\""
                extra = 2
            else:
                end_char = ","
                extra = 1

        while line[c_idx] != end_char:
            word_end_idx += 1
            c_idx += 1
            if c_idx >= len(line):
                c_idx = len(line) - 1
                break

        parts.append(line[word_begin_idx:word_begin_idx + word_end_idx])
        c_idx = word_begin_idx + word_end_idx + extra
        word_end_idx = 0

    return parts


cities = set()
counties = set()
neighborhoods = set()

for each_file in all_files:
    print("Processing ", each_file)
    with open(each_file, "r", encoding="latin-1") as csv_file:
        line_num = 0
        idx_map = {}

        for line in csv_file:
            line = line.rstrip("\n")
            #line_parts = line.split(",")
            line_parts = break_into_line_parts_1(line)
            if line_num == 0:
                for part_idx in range(len(line_parts)):
                    each_line_part = line_parts[part_idx]
                    if each_line_part.strip("\"") == "RegionName":
                        idx_map['RegionName'] = part_idx
                    if each_line_part.strip("\"") == "City":
                        idx_map['City'] = part_idx
                    if each_line_part.strip("\"") == "State":
                        idx_map['State'] = part_idx
                    if each_line_part.strip("\"") == "CountyName" or each_line_part.strip("\"") == "County":
                        idx_map['County'] = part_idx

                line_num += 1
                continue
            neighborhood_name = line_parts[idx_map.get('RegionName')].strip("\"")
            city_name = line_parts[idx_map.get('City')].strip("\"")
            state_code = line_parts[idx_map.get('State')].strip("\"")
            county_name = line_parts[idx_map.get('County')].strip("\"")

            combo_county = state_code + "::" + county_name
            combo_city = state_code + "::" + county_name + "::" + city_name
            neighborhood_combo = state_code + "::" + county_name + "::" + city_name + "::" + neighborhood_name

            counties.add(combo_county)
            cities.add(combo_city)
            neighborhoods.add(neighborhood_combo)
            line_num += 1

insert_lines = []
for each_combo in counties:
    state_code, county_name = each_combo.split("::")
    select_line = "(SELECT id from state where state_code='" + state_code + "')"
    insert_line = "INSERT INTO county(name, state_id) values('" + county_name + "'," + select_line + ");"
    insert_lines.append(insert_line)

sql_file = open("./data/sql/county_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()


insert_lines = []
for each_combo in cities:
    state_code, county_name, city_name = each_combo.split("::")
    city_name = city_name.replace('\'', '\'\'')
    county_name = county_name.replace('\'', '\'\'')

    select_state_id_line = "(SELECT id from state where state_code='" + state_code + "')"
    select_county_id_line = "(SELECT id from county where name='" + county_name \
                            + "' and state_id = " + select_state_id_line + ")"
    insert_line = "INSERT INTO city(name, state_id, county_id) " \
                  "values('" + city_name + "'," + select_state_id_line + "," + select_county_id_line + ");"
    insert_lines.append(insert_line)

sql_file = open("./data/sql/city_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()


def construct_state_select(state_code):
    return "(SELECT id from state where state_code= '" + state_code + "')"

def construct_county_select(county_name, state_code):
    statement = "(SELECT county.id from county" + \
                " inner join state on county.state_id = state.id" + \
                " where county.name = '" + county_name + "' and state.state_code = '" + state_code + "')"
    return statement

def construct_city_select(city_name, county_name, state_code):
    statement = "(select city.id from city" + \
                " inner join county" + \
                " on city.county_id = county.id" + \
                " inner join state on city.state_id = state.id" + \
                " where city.name = '" + city_name + "' and state.state_code = '" + state_code + \
                "' and county.name = '" + county_name + "')"
    return statement

insert_lines = []
for each_combo in neighborhoods:
    state_code, county_name, city_name, neighborhood_name = each_combo.split("::")
    city_name = city_name.replace('\'', '\'\'')
    county_name = county_name.replace('\'', '\'\'')
    neighborhood_name = neighborhood_name.replace('\'', '\'\'')

    insert_line = "INSERT INTO neighborhood(state_id, county_id, city_id, name) values(" \
                  + construct_state_select(state_code) + \
                  "," + construct_county_select(county_name, state_code) + \
                  "," + construct_city_select(city_name, county_name, state_code) + ",'" + neighborhood_name + "');"
    insert_lines.append(insert_line)



sql_file = open("./data/sql/neighborhood_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()
