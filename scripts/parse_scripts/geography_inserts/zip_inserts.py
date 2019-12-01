all_files = [
    "./data/ZRI/allSummary/Zip_Zri_AllHomesPlusMultifamily_Summary.csv",
    "./data/ZRI/medianSFRCondo/Zip_ZriPerSqft_AllHomes.csv",
    "./data/ZRI/sFRTimeSeries/Zip_Zri_SingleFamilyResidenceRental.csv",
    "./data/ZRI/allHomesTimeSeries/Zip_Zri_AllHomesPlusMultifamily.csv",
    "./data/ZRI/multiFamilyTimeSeries/Zip_Zri_MultiFamilyResidenceRental.csv",
    "./data/rentalListings/medianRentListPriceSqFt_4bedroom/Zip_MedianRentalPricePerSqft_4Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_sfrCondoCoop/Zip_MedianRentalPrice_AllHomes.csv",
    "./data/rentalListings/medianRentListPriceSqFt_duplexTriplex/Zip_MedianRentalPricePerSqft_DuplexTriplex.csv",
    "./data/rentalListings/medianRentListPriceSqFt_sFRCondoCoop/Zip_MedianRentalPricePerSqft_AllHomes.csv",
    "./data/rentalListings/medianRentListPrice_condoCoop/Zip_MedianRentalPrice_CondoCoop.csv",
    "./data/rentalListings/medianRentListPrice_duplexTriplex/Zip_MedianRentalPrice_DuplexTriplex.csv",
    "./data/rentalListings/medianRentListPrice_2bedroom/Zip_MedianRentalPrice_2Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_2bedroom/Zip_MedianRentalPricePerSqft_2Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_4bedroom/Zip_MedianRentalPrice_4Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_singleFamilyResidence/Zip_MedianRentalPricePerSqft_Sfr.csv",
    "./data/rentalListings/medianRentListPriceSqFt_multiFamily/Zip_MedianRentalPricePerSqft_Mfr5Plus.csv",
    "./data/rentalListings/medianRentListPrice_1bedroom/Zip_MedianRentalPrice_1Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_5bedroom/Zip_MedianRentalPricePerSqft_5BedroomOrMore.csv",
    "./data/rentalListings/medianRentListPrice_3bedroom/Zip_MedianRentalPrice_3Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_5PlusBedroom/Zip_MedianRentalPrice_5BedroomOrMore.csv",
    "./data/rentalListings/medianRentListPrice_singleFamilyResidence/Zip_MedianRentalPrice_Sfr.csv",
    "./data/rentalListings/medianRentListPriceSqFt_condoCoop/Zip_MedianRentalPricePerSqft_CondoCoop.csv",
    "./data/rentalListings/medianRentListPrice_multiFamily/Zip_MedianRentalPrice_Mfr5Plus.csv",
    "./data/rentalListings/medianRentListPriceSqFt_3bedroom/Zip_MedianRentalPricePerSqft_3Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_studio/Zip_MedianRentalPricePerSqft_Studio.csv",
    "./data/rentalListings/medianRentListPrice_studio/Zip_MedianRentalPrice_Studio.csv",
    "./data/rentalListings/medianRentListPriceSqFt_1bedroom/Zip_MedianRentalPricePerSqft_1Bedroom.csv",
    "./data/ZHVI/singleFamilyHomeTimeSeries/Zip_Zhvi_SingleFamilyResidence.csv",
    "./data/ZHVI/condoCoOpTimeSeries/Zip_Zhvi_Condominum.csv",
    "./data/ZHVI/all_homes_condoCoOpTimeSeries/Zip_Zhvi_AllHomes.csv",
    "./data/ZHVI/twoBedroomTimeSeries/Zip_Zhvi_2bedroom.csv",
    "./data/ZHVI/threeBedroomTimeSeries/Zip_Zhvi_3bedroom.csv",
    "./data/ZHVI/fivePlusBedroomTimeSeries/Zip_Zhvi_5BedroomOrMore.csv",
    "./data/ZHVI/fourBedroomTimeSeries/Zip_Zhvi_4bedroom.csv",
    "./data/ZHVI/medianPerSqFt/Zip_MedianValuePerSqft_AllHomes.csv",
    "./data/ZHVI/oneBedroomTimeSeries/Zip_Zhvi_1bedroom.csv",
    "./data/homeListings_Sales/medianListPrice/Zip_MedianListingPrice_AllHomes.csv",
]

cities = set()
counties = set()
zips = set()

for each_file in all_files:
    print("Processing ", each_file)
    with open(each_file, "r", encoding="latin-1") as csv_file:
        line_num = 0
        idx_map = {}

        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_num == 0:
                for part_idx in range(len(line_parts)):
                    each_line_part = line_parts[part_idx]
                    if each_line_part.strip('"') == "RegionName":
                        idx_map["RegionName"] = part_idx
                    if each_line_part.strip('"') == "City":
                        idx_map["City"] = part_idx
                    if each_line_part.strip('"') == "State":
                        idx_map["State"] = part_idx
                    if (
                        each_line_part.strip('"') == "CountyName"
                        or each_line_part.strip('"') == "County"
                    ):
                        idx_map["County"] = part_idx

            zipcode = line_parts[idx_map.get("RegionName")].strip('"')
            city_name = line_parts[idx_map.get("City")].strip('"')
            state_code = line_parts[idx_map.get("State")].strip('"')
            county_name = line_parts[idx_map.get("County")].strip('"')

            combo_county = state_code + "::" + county_name
            combo_city = state_code + "::" + county_name + "::" + city_name
            zipcode_combo = (
                state_code + "::" + county_name + "::" + city_name + "::" + zipcode
            )

            counties.add(combo_county)
            cities.add(combo_city)
            zips.add(zipcode_combo)
            line_num += 1

insert_lines = []
for each_combo in counties:
    state_code, county_name = each_combo.split("::")
    select_line = "(SELECT id from state where state_code='" + state_code + "')"
    insert_line = (
        "INSERT INTO county(name, state_id) values('"
        + county_name
        + "',"
        + select_line
        + ");"
    )
    insert_lines.append(insert_line)

sql_file = open("./data/sql/county_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()


insert_lines = []
for each_combo in cities:
    state_code, county_name, city_name = each_combo.split("::")
    city_name = city_name.replace("'", "''")
    county_name = county_name.replace("'", "''")

    select_state_id_line = (
        "(SELECT id from state where state_code='" + state_code + "')"
    )
    select_county_id_line = (
        "(SELECT id from county where name='"
        + county_name
        + "' and state_id = "
        + select_state_id_line
        + ")"
    )
    insert_line = (
        "INSERT INTO city(name, state_id, county_id) "
        "values('"
        + city_name
        + "',"
        + select_state_id_line
        + ","
        + select_county_id_line
        + ");"
    )
    insert_lines.append(insert_line)

sql_file = open("./data/sql/city_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()


def construct_state_select(state_code):
    return "(SELECT id from state where state_code= '" + state_code + "')"


def construct_county_select(county_name, state_code):
    statement = (
        "(SELECT county.id from county"
        + " inner join state on county.state_id = state.id"
        + " where county.name = '"
        + county_name
        + "' and state.state_code = '"
        + state_code
        + "')"
    )
    return statement


def construct_city_select(city_name, county_name, state_code):
    statement = (
        "(select city.id from city"
        + " inner join county"
        + " on city.county_id = county.id"
        + " inner join state on city.state_id = state.id"
        + " where city.name = '"
        + city_name
        + "' and state.state_code = '"
        + state_code
        + "' and county.name = '"
        + county_name
        + "')"
    )
    return statement


insert_lines = []
for each_combo in zips:
    state_code, county_name, city_name, zipcode = each_combo.split("::")
    city_name = city_name.replace("'", "''")
    county_name = county_name.replace("'", "''")

    insert_line = (
        "INSERT INTO zipcode(state_id, county_id, city_id, zip_code) values("
        + construct_state_select(state_code)
        + ","
        + construct_county_select(county_name, state_code)
        + ","
        + construct_city_select(city_name, county_name, state_code)
        + ",'"
        + zipcode
        + "');"
    )
    insert_lines.append(insert_line)

sql_file = open("./data/sql/zip_inserts.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()
