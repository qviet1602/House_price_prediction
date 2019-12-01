def process_data(input_file_name, feature, output_file_name):
    insert_lines = []
    month_year_list = []
    with open(input_file_name, "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[6:]
                line_count += 1
                continue

            county_name = line_parts[0].strip("\"")
            state_code = line_parts[1].strip("\"")
            county_name = county_name.replace('\'', '\'\'')
            county_select = "(select county.id from county inner join state on county.state_id = state.id where county.name ='" + county_name \
                            + "' and state.state_code = '" + state_code + "')"
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = '" + feature + "')"
            for idx in range(6, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    list_price = int(round(float(line_parts[idx].strip("\""))))
                    insert_line = "INSERT INTO county_median_price (county_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','" + \
                                  str(list_price) + "');"
                else:
                    insert_line = "INSERT INTO county_median_price (county_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "',null);"

                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open(output_file_name, "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

process_data("data/rentalListings/medianRentListPrice_1bedroom/County_MedianRentalPrice_1Bedroom.csv",
          "oneBedroom", "data/county_rental_median_price_1bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_2bedroom/County_MedianRentalPrice_2Bedroom.csv",
          "twoBedroom", "data/county_rental_median_price_2bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_3bedroom/County_MedianRentalPrice_3Bedroom.csv",
          "threeBedroom", "data/county_rental_median_price_3bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_4bedroom/County_MedianRentalPrice_4Bedroom.csv",
          "fourBedroom", "data/county_rental_median_price_4bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_5PlusBedroom/County_MedianRentalPrice_5BedroomOrMore.csv",
          "fivePlusBedroom", "data/county_rental_median_price_5bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_condoCoop/County_MedianRentalPrice_CondoCoop.csv",
          "condoCoOp", "data/county_rental_median_price_condo_insert.sql")

process_data("data/rentalListings/medianRentListPrice_duplexTriplex/County_MedianRentalPrice_DuplexTriplex.csv",
          "duplexTriplex", "data/county_rental_median_price_duplexTriplex_insert.sql")

process_data("data/rentalListings/medianRentListPrice_multiFamily/County_MedianRentalPrice_Mfr5Plus.csv",
          "multiFamilyResidenceRental", "data/county_rental_median_price_multiFamilyResidenceRental_insert.sql")

process_data("data/rentalListings/medianRentListPrice_sfrCondoCoop/County_MedianRentalPrice_AllHomes.csv",
          "all", "data/county_rental_median_price_all_insert.sql")

process_data("data/rentalListings/medianRentListPrice_singleFamilyResidence/County_MedianRentalPrice_Sfr.csv",
          "singleFamilyResidenceRental", "data/county_rental_median_price_singleFamilyResidenceRental_insert.sql")

process_data("data/rentalListings/medianRentListPrice_studio/County_MedianRentalPrice_Studio.csv",
          "studio", "data/county_rental_median_price_studio_insert.sql")