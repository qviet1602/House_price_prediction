all_files = [
    "./data/ZRI/allSummary/County_Zri_AllHomesPlusMultifamily_Summary.csv",
    "./data/ZRI/medianSFRCondo/County_ZriPerSqft_AllHomes.csv",
    "./data/ZRI/sFRTimeSeries/County_Zri_SingleFamilyResidenceRental.csv",
    "./data/ZRI/allHomesTimeSeries/County_Zri_AllHomesPlusMultifamily.csv",
    "./data/ZRI/multiFamilyTimeSeries/County_Zri_MultiFamilyResidenceRental.csv",
    "./data/rentalListings/medianRentListPriceSqFt_4bedroom/County_MedianRentalPricePerSqft_4Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_sfrCondoCoop/County_MedianRentalPrice_AllHomes.csv",
    "./data/rentalListings/medianRentListPriceSqFt_duplexTriplex/County_MedianRentalPricePerSqft_DuplexTriplex.csv",
    "./data/rentalListings/medianRentListPriceSqFt_sFRCondoCoop/County_MedianRentalPricePerSqft_AllHomes.csv",
    "./data/rentalListings/medianRentListPrice_condoCoop/County_MedianRentalPrice_CondoCoop.csv",
    "./data/rentalListings/medianRentListPrice_duplexTriplex/County_MedianRentalPrice_DuplexTriplex.csv",
    "./data/rentalListings/medianRentListPrice_2bedroom/County_MedianRentalPrice_2Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_2bedroom/County_MedianRentalPricePerSqft_2Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_4bedroom/County_MedianRentalPrice_4Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_singleFamilyResidence/County_MedianRentalPricePerSqft_Sfr.csv",
    "./data/rentalListings/medianRentListPriceSqFt_multiFamily/County_MedianRentalPricePerSqft_Mfr5Plus.csv",
    "./data/rentalListings/medianRentListPrice_1bedroom/County_MedianRentalPrice_1Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_5bedroom/County_MedianRentalPricePerSqft_5BedroomOrMore.csv",
    "./data/rentalListings/medianRentListPrice_3bedroom/County_MedianRentalPrice_3Bedroom.csv",
    "./data/rentalListings/medianRentListPrice_5PlusBedroom/County_MedianRentalPrice_5BedroomOrMore.csv",
    "./data/rentalListings/medianRentListPrice_singleFamilyResidence/County_MedianRentalPrice_Sfr.csv",
    "./data/rentalListings/medianRentListPriceSqFt_condoCoop/County_MedianRentalPricePerSqft_CondoCoop.csv",
    "./data/rentalListings/medianRentListPrice_multiFamily/County_MedianRentalPrice_Mfr5Plus.csv",
    "./data/rentalListings/medianRentListPriceSqFt_3bedroom/County_MedianRentalPricePerSqft_3Bedroom.csv",
    "./data/rentalListings/medianRentListPriceSqFt_studio/County_MedianRentalPricePerSqft_Studio.csv",
    "./data/rentalListings/medianRentListPrice_studio/County_MedianRentalPrice_Studio.csv",
    "./data/rentalListings/medianRentListPriceSqFt_1bedroom/County_MedianRentalPricePerSqft_1Bedroom.csv",
    "./data/ZHVI/all_homes_topTierTimeSeries/County_Zhvi_TopTier.csv",
    "./data/ZHVI/singleFamilyHomeTimeSeries/County_Zhvi_SingleFamilyResidence.csv",
    "./data/ZHVI/condoCoOpTimeSeries/County_Zhvi_Condominum.csv",
    "./data/ZHVI/all_homes_bottomTierTimeSeries/County_Zhvi_BottomTier.csv",
    "./data/ZHVI/all_homes_condoCoOpTimeSeries/County_Zhvi_AllHomes.csv",
    "./data/ZHVI/twoBedroomTimeSeries/County_Zhvi_2bedroom.csv",
    "./data/ZHVI/threeBedroomTimeSeries/County_Zhvi_3bedroom.csv",
    "./data/ZHVI/fivePlusBedroomTimeSeries/County_Zhvi_5BedroomOrMore.csv",
    "./data/ZHVI/fourBedroomTimeSeries/County_Zhvi_4bedroom.csv",
    "./data/ZHVI/medianPerSqFt/County_MedianValuePerSqft_AllHomes.csv",
    "./data/ZHVI/oneBedroomTimeSeries/County_Zhvi_1bedroom.csv",
    "./data/homeListings_Sales/medianListPrice/County_MedianListingPrice_AllHomes.csv",
    "./data/homeListings_Sales/newMonthlyForSaleInventory_raw/NewMonthlyListings_NSA_AllHomes_County.csv",
]

counties_by_state = set()

for each_file in all_files:
    print("Processing ", each_file)
    with open(each_file, "r", encoding="latin-1") as csv_file:
        line_num = 0
        idx_1 = 1
        idx_2 = 2
        if "medianListPrice" in each_file or "rentalListings" in each_file:
            idx_1 = 0
            idx_2 = 1
        if "newMonthlyForSaleInventory_raw" in each_file:
            idx_1 = 2
            idx_2 = 4

        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_num == 0:
                line_num += 1
                continue

            county_name = line_parts[idx_1].strip('"')
            state_code = line_parts[idx_2].strip('"')

            combo = state_code + "::" + county_name

            counties_by_state.add(combo)
            line_num += 1


insert_lines = []
for each_combo in counties_by_state:
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
