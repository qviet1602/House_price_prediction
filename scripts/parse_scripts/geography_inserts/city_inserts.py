all_files = ["./data/ZRI/allSummary/City_Zri_AllHomesPlusMultifamily_Summary.csv",
             "./data/ZRI/medianSFRCondo/City_ZriPerSqft_AllHomes.csv",
             "./data/ZRI/sFRTimeSeries/City_Zri_SingleFamilyResidenceRental.csv",
             "./data/ZRI/allHomesTimeSeries/City_Zri_AllHomesPlusMultifamily.csv",
             "./data/ZRI/multiFamilyTimeSeries/City_Zri_MultiFamilyResidenceRental.csv",
             "./data/rentalListings/medianRentListPriceSqFt_4bedroom/City_MedianRentalPricePerSqft_4Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_sfrCondoCoop/City_MedianRentalPrice_AllHomes.csv",
             "./data/rentalListings/medianRentListPriceSqFt_duplexTriplex/City_MedianRentalPricePerSqft_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPriceSqFt_sFRCondoCoop/City_MedianRentalPricePerSqft_AllHomes.csv",
             "./data/rentalListings/medianRentListPrice_condoCoop/City_MedianRentalPrice_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_duplexTriplex/City_MedianRentalPrice_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPrice_2bedroom/City_MedianRentalPrice_2Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_2bedroom/City_MedianRentalPricePerSqft_2Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_4bedroom/City_MedianRentalPrice_4Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_singleFamilyResidence/City_MedianRentalPricePerSqft_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_multiFamily/City_MedianRentalPricePerSqft_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPrice_1bedroom/City_MedianRentalPrice_1Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_5bedroom/City_MedianRentalPricePerSqft_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_3bedroom/City_MedianRentalPrice_3Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_5PlusBedroom/City_MedianRentalPrice_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_singleFamilyResidence/City_MedianRentalPrice_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_condoCoop/City_MedianRentalPricePerSqft_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_multiFamily/City_MedianRentalPrice_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPriceSqFt_3bedroom/City_MedianRentalPricePerSqft_3Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_studio/City_MedianRentalPricePerSqft_Studio.csv",
             "./data/rentalListings/medianRentListPrice_studio/City_MedianRentalPrice_Studio.csv",
             "./data/rentalListings/medianRentListPriceSqFt_1bedroom/City_MedianRentalPricePerSqft_1Bedroom.csv",
             "./data/ZHVI/all_homes_topTierTimeSeries/City_Zhvi_TopTier.csv",
             "./data/ZHVI/singleFamilyHomeTimeSeries/City_Zhvi_SingleFamilyResidence.csv",
             "./data/ZHVI/condoCoOpTimeSeries/City_Zhvi_Condominum.csv",
             "./data/ZHVI/all_homes_bottomTierTimeSeries/City_Zhvi_BottomTier.csv",
             "./data/ZHVI/all_homes_condoCoOpTimeSeries/City_Zhvi_AllHomes.csv",
             "./data/ZHVI/twoBedroomTimeSeries/City_Zhvi_2bedroom.csv",
             "./data/ZHVI/threeBedroomTimeSeries/City_Zhvi_3bedroom.csv",
             "./data/ZHVI/fivePlusBedroomTimeSeries/City_Zhvi_5BedroomOrMore.csv",
             "./data/ZHVI/fourBedroomTimeSeries/City_Zhvi_4bedroom.csv",
             "./data/ZHVI/medianPerSqFt/City_MedianValuePerSqft_AllHomes.csv",
             "./data/ZHVI/oneBedroomTimeSeries/City_Zhvi_1bedroom.csv",
             "./data/homeListings_Sales/medianListPrice/City_MedianListingPrice_AllHomes.csv"]

cities = set()
counties = set()

for each_file in all_files:
    print("Processing ", each_file)
    with open(each_file, "r", encoding="latin-1") as csv_file:
        line_num = 0
        idx_1 = 1
        idx_2 = 2
        idx_3 = 4
        if "medianListPrice" in each_file or "rentalListings" in each_file:
            idx_1 = 0
            idx_2 = 1
            idx_3 = 3

        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_num == 0:
                line_num += 1
                continue

            city_name = line_parts[idx_1].strip("\"")
            state_code = line_parts[idx_2].strip("\"")
            county_name = line_parts[idx_3].strip("\"")

            combo_county = state_code + "::" + county_name
            combo_city = state_code + "::" + county_name + "::" + city_name

            counties.add(combo_county)
            cities.add(combo_city)
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
