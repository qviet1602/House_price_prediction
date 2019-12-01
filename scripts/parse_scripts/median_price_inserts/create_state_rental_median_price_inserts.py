def get_state_code(state_name):
    state_names_map = {}
    state_names_map["Alabama"] = "AL"
    state_names_map["Alaska"] = "AK"
    state_names_map["Arizona"] = "AZ"
    state_names_map["Arkansas"] = "AR"
    state_names_map["California"] = "CA"
    state_names_map["Colorado"] = "CO"
    state_names_map["Connecticut"] = "CT"
    state_names_map["Delaware"] = "DE"
    state_names_map["Florida"] = "FL"
    state_names_map["Georgia"] = "GA"
    state_names_map["Hawaii"] = "HI"
    state_names_map["Idaho"] = "ID"
    state_names_map["Illinois"] = "IL"
    state_names_map["Indiana"] = "IN"
    state_names_map["Iowa"] = "IA"
    state_names_map["Kansas"] = "KS"
    state_names_map["Kentucky"] = "KY"
    state_names_map["Louisiana"] = "LA"
    state_names_map["Maine"] = "ME"
    state_names_map["Maryland"] = "MD"
    state_names_map["Massachusetts"] = "MA"
    state_names_map["Michigan"] = "MI"
    state_names_map["Minnesota"] = "MN"
    state_names_map["Mississippi"] = "MS"
    state_names_map["Missouri"] = "MO"
    state_names_map["Montana"] = "MT"
    state_names_map["Nebraska"] = "NE"
    state_names_map["Nevada"] = "NV"
    state_names_map["New Hampshire"] = "NH"
    state_names_map["New Jersey"] = "NJ"
    state_names_map["New Mexico"] = "NM"
    state_names_map["New York"] = "NY"
    state_names_map["North Carolina"] = "NC"
    state_names_map["North Dakota"] = "ND"
    state_names_map["Ohio"] = "OH"
    state_names_map["Oklahoma"] = "OK"
    state_names_map["Oregon"] = "OR"
    state_names_map["Pennsylvania"] = "PA"
    state_names_map["Rhode Island"] = "RI"
    state_names_map["South Carolina"] = "SC"
    state_names_map["South Dakota"] = "SD"
    state_names_map["Tennessee"] = "TN"
    state_names_map["Texas"] = "TX"
    state_names_map["Utah"] = "UT"
    state_names_map["Vermont"] = "VT"
    state_names_map["Virginia"] = "VA"
    state_names_map["Washington"] = "WA"
    state_names_map["West Virginia"] = "WV"
    state_names_map["Wisconsin"] = "WI"
    state_names_map["Wyoming"] = "WY"
    state_names_map["District of Columbia"] = "DC"
    state_names_map["Marshall Islands"] = "MH"

    return state_names_map.get(state_name, None)


def process_data(input_file_name, feature, output_file_name):
    print("Processing ", input_file_name)
    insert_lines = []
    month_year_list = []
    with open(input_file_name, "r") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[2:]
                line_count += 1
                continue

            state_name = line_parts[0].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = (
                "(SELECT id from home_type where type = 'rental' and feature = '"
                + feature
                + "')"
            )
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(2, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    list_price = int(round(float(line_parts[idx].strip('"'))))
                    insert_line = (
                        "INSERT INTO state_median_price (state_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 2].strip('"')
                        + "','"
                        + str(list_price)
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_median_price (state_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 2].strip('"')
                        + "',null);"
                    )

                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open(output_file_name, "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


process_data(
    "data/rentalListings/medianRentListPrice_1bedroom/State_MedianRentalPrice_1Bedroom.csv",
    "oneBedroom",
    "data/state_rental_median_price_1bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_2bedroom/State_MedianRentalPrice_2Bedroom.csv",
    "twoBedroom",
    "data/state_rental_median_price_2bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_3bedroom/State_MedianRentalPrice_3Bedroom.csv",
    "threeBedroom",
    "data/state_rental_median_price_3bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_4bedroom/State_MedianRentalPrice_4Bedroom.csv",
    "fourBedroom",
    "data/state_rental_median_price_4bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_5PlusBedroom/State_MedianRentalPrice_5BedroomOrMore.csv",
    "fivePlusBedroom",
    "data/state_rental_median_price_5bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_condoCoop/State_MedianRentalPrice_CondoCoop.csv",
    "condoCoOp",
    "data/state_rental_median_price_condo_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_duplexTriplex/State_MedianRentalPrice_DuplexTriplex.csv",
    "duplexTriplex",
    "data/state_rental_median_price_duplexTriplex_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_multiFamily/State_MedianRentalPrice_Mfr5Plus.csv",
    "multiFamilyResidenceRental",
    "data/state_rental_median_price_multiFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_sfrCondoCoop/State_MedianRentalPrice_AllHomes.csv",
    "all",
    "data/state_rental_median_price_all_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_singleFamilyResidence/State_MedianRentalPrice_Sfr.csv",
    "singleFamilyResidenceRental",
    "data/state_rental_median_price_singleFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_studio/State_MedianRentalPrice_Studio.csv",
    "studio",
    "data/state_rental_median_price_studio_insert.sql",
)
