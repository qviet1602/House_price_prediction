def get_state_code(state_name):
    state_names_map = {}
    state_names_map['Alabama'] = 'AL'
    state_names_map['Alaska'] = 'AK'
    state_names_map['Arizona'] = 'AZ'
    state_names_map['Arkansas'] = 'AR'
    state_names_map['California'] = 'CA'
    state_names_map['Colorado'] = 'CO'
    state_names_map['Connecticut'] = 'CT'
    state_names_map['Delaware'] = 'DE'
    state_names_map['Florida'] = 'FL'
    state_names_map['Georgia'] = 'GA'
    state_names_map['Hawaii'] = 'HI'
    state_names_map['Idaho'] = 'ID'
    state_names_map['Illinois'] = 'IL'
    state_names_map['Indiana'] = 'IN'
    state_names_map['Iowa'] = 'IA'
    state_names_map['Kansas'] = 'KS'
    state_names_map['Kentucky'] = 'KY'
    state_names_map['Louisiana'] = 'LA'
    state_names_map['Maine'] = 'ME'
    state_names_map['Maryland'] = 'MD'
    state_names_map['Massachusetts'] = 'MA'
    state_names_map['Michigan'] = 'MI'
    state_names_map['Minnesota'] = 'MN'
    state_names_map['Mississippi'] = 'MS'
    state_names_map['Missouri'] = 'MO'
    state_names_map['Montana'] = 'MT'
    state_names_map['Nebraska'] = 'NE'
    state_names_map['Nevada'] = 'NV'
    state_names_map['New Hampshire'] = 'NH'
    state_names_map['New Jersey'] = 'NJ'
    state_names_map['New Mexico'] = 'NM'
    state_names_map['New York'] = 'NY'
    state_names_map['North Carolina'] = 'NC'
    state_names_map['North Dakota'] = 'ND'
    state_names_map['Ohio'] = 'OH'
    state_names_map['Oklahoma'] = 'OK'
    state_names_map['Oregon'] = 'OR'
    state_names_map['Pennsylvania'] = 'PA'
    state_names_map['Rhode Island'] = 'RI'
    state_names_map['South Carolina'] = 'SC'
    state_names_map['South Dakota'] = 'SD'
    state_names_map['Tennessee'] = 'TN'
    state_names_map['Texas'] = 'TX'
    state_names_map['Utah'] = 'UT'
    state_names_map['Vermont'] = 'VT'
    state_names_map['Virginia'] = 'VA'
    state_names_map['Washington'] = 'WA'
    state_names_map['West Virginia'] = 'WV'
    state_names_map['Wisconsin'] = 'WI'
    state_names_map['Wyoming'] = 'WY'
    state_names_map['District of Columbia'] = 'DC'
    state_names_map['Marshall Islands'] = 'MH'

    return state_names_map.get(state_name, None)

all_files = ["./data/ZRI/allSummary/State_Zri_AllHomesPlusMultifamily_Summary.csv",
             "./data/ZRI/medianSFRCondo/State_ZriPerSqft_AllHomes.csv",
             "./data/ZRI/sFRTimeSeries/State_Zri_SingleFamilyResidenceRental.csv",
             "./data/ZRI/allHomesTimeSeries/State_Zri_AllHomesPlusMultifamily.csv",
             "./data/ZRI/multiFamilyTimeSeries/State_Zri_MultiFamilyResidenceRental.csv",
             "./data/rentalListings/medianRentListPriceSqFt_4bedroom/State_MedianRentalPricePerSqft_4Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_sfrCondoCoop/State_MedianRentalPrice_AllHomes.csv",
             "./data/rentalListings/medianRentListPriceSqFt_duplexTriplex/State_MedianRentalPricePerSqft_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPriceSqFt_sFRCondoCoop/State_MedianRentalPricePerSqft_AllHomes.csv",
             "./data/rentalListings/medianRentListPrice_condoCoop/State_MedianRentalPrice_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_duplexTriplex/State_MedianRentalPrice_DuplexTriplex.csv",
             "./data/rentalListings/medianRentListPrice_2bedroom/State_MedianRentalPrice_2Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_2bedroom/State_MedianRentalPricePerSqft_2Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_4bedroom/State_MedianRentalPrice_4Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_singleFamilyResidence/State_MedianRentalPricePerSqft_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_multiFamily/State_MedianRentalPricePerSqft_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPrice_1bedroom/State_MedianRentalPrice_1Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_5bedroom/State_MedianRentalPricePerSqft_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_3bedroom/State_MedianRentalPrice_3Bedroom.csv",
             "./data/rentalListings/medianRentListPrice_5PlusBedroom/State_MedianRentalPrice_5BedroomOrMore.csv",
             "./data/rentalListings/medianRentListPrice_singleFamilyResidence/State_MedianRentalPrice_Sfr.csv",
             "./data/rentalListings/medianRentListPriceSqFt_condoCoop/State_MedianRentalPricePerSqft_CondoCoop.csv",
             "./data/rentalListings/medianRentListPrice_multiFamily/State_MedianRentalPrice_Mfr5Plus.csv",
             "./data/rentalListings/medianRentListPriceSqFt_3bedroom/State_MedianRentalPricePerSqft_3Bedroom.csv",
             "./data/rentalListings/medianRentListPriceSqFt_studio/State_MedianRentalPricePerSqft_Studio.csv",
             "./data/rentalListings/medianRentListPrice_studio/State_MedianRentalPrice_Studio.csv",
             "./data/rentalListings/medianRentListPriceSqFt_1bedroom/State_MedianRentalPricePerSqft_1Bedroom.csv",
             "./data/ZHVI/all_homes_topTierTimeSeries/State_Zhvi_TopTier.csv",
             "./data/ZHVI/singleFamilyHomeTimeSeries/State_Zhvi_SingleFamilyResidence.csv",
             "./data/ZHVI/condoCoOpTimeSeries/State_Zhvi_Condominum.csv",
             "./data/ZHVI/all_homes_bottomTierTimeSeries/State_Zhvi_BottomTier.csv",
             "./data/ZHVI/all_homes_condoCoOpTimeSeries/State_Zhvi_AllHomes.csv",
             "./data/ZHVI/twoBedroomTimeSeries/State_Zhvi_2bedroom.csv",
             "./data/ZHVI/threeBedroomTimeSeries/State_Zhvi_3bedroom.csv",
             "./data/ZHVI/fivePlusBedroomTimeSeries/State_Zhvi_5BedroomOrMore.csv",
             "./data/ZHVI/fourBedroomTimeSeries/State_Zhvi_4bedroom.csv",
             "./data/ZHVI/medianPerSqFt/State_MedianValuePerSqft_AllHomes.csv",
             "./data/ZHVI/oneBedroomTimeSeries/State_Zhvi_1bedroom.csv",
             "./data/homeListings_Sales/medianListPrice/State_MedianListingPrice_AllHomes.csv"]

states_map = {}

for each_file in all_files:
    print("Processing ", each_file)
    with open(each_file, "r") as csv_file:
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_parts[0].strip("\"") == "RegionID":
                continue

            state_name = line_parts[1].strip("\"")
            state_code = get_state_code(state_name)
            if state_code is None:
                continue
            states_map[state_code] = state_name


insert_lines = []
for each_state_code in states_map.keys():
    state_name = states_map.get(each_state_code)
    insert_line = "INSERT INTO state(state_code, name) values('" + each_state_code + "','" + state_name + "');"
    insert_lines.append(insert_line)

sql_file = open("./data/sql/states_insert.sql", "a")

for line in insert_lines:
    sql_file.write(line)
    sql_file.write("\n")

sql_file.close()