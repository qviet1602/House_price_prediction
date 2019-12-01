def process_data(input_file_name, feature, output_file_name):
    insert_lines = []
    month_year_list = []
    with open(input_file_name, "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[5:]
                line_count += 1
                continue


            city_name = line_parts[0].strip("\"")
            state_code = line_parts[1].strip("\"")
            county_name = line_parts[3].strip("\"")

            city_name = city_name.replace('\'', '\'\'')
            county_name = county_name.replace('\'', '\'\'')

            city_select = "(select city.id from city inner join county on city.county_id = county.id " \
                          "inner join state on county.state_id = state.id where county.name ='" + county_name \
                          + "' and state.state_code = '" + state_code + "' and city.name = '" + city_name + "')"
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = '" + feature + "')"
            for idx in range(5, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    list_price = int(round(float(line_parts[idx].strip("\""))))
                    insert_line = "INSERT INTO city_median_price (city_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 5].strip("\"") + \
                                  "','" + str(list_price) + "');"
                else:
                    insert_line = "INSERT INTO city_median_price (city_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 5].strip("\"") + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open(output_file_name, "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

process_data("data/rentalListings/medianRentListPrice_1bedroom/City_MedianRentalPrice_1Bedroom.csv",
          "oneBedroom", "data/city_rental_median_price_1bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_2bedroom/City_MedianRentalPrice_2Bedroom.csv",
          "twoBedroom", "data/city_rental_median_price_2bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_3bedroom/City_MedianRentalPrice_3Bedroom.csv",
          "threeBedroom", "data/city_rental_median_price_3bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_4bedroom/City_MedianRentalPrice_4Bedroom.csv",
          "fourBedroom", "data/city_rental_median_price_4bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_5PlusBedroom/City_MedianRentalPrice_5BedroomOrMore.csv",
          "fivePlusBedroom", "data/city_rental_median_price_5bedroom_insert.sql")

process_data("data/rentalListings/medianRentListPrice_condoCoop/City_MedianRentalPrice_CondoCoop.csv",
          "condoCoOp", "data/city_rental_median_price_condo_insert.sql")

process_data("data/rentalListings/medianRentListPrice_duplexTriplex/City_MedianRentalPrice_DuplexTriplex.csv",
          "duplexTriplex", "data/city_rental_median_price_duplexTriplex_insert.sql")

process_data("data/rentalListings/medianRentListPrice_multiFamily/City_MedianRentalPrice_Mfr5Plus.csv",
          "multiFamilyResidenceRental", "data/city_rental_median_price_multiFamilyResidenceRental_insert.sql")

process_data("data/rentalListings/medianRentListPrice_sfrCondoCoop/City_MedianRentalPrice_AllHomes.csv",
          "all", "data/city_rental_median_price_all_insert.sql")

process_data("data/rentalListings/medianRentListPrice_singleFamilyResidence/City_MedianRentalPrice_Sfr.csv",
          "singleFamilyResidenceRental", "data/city_rental_median_price_singleFamilyResidenceRental_insert.sql")

process_data("data/rentalListings/medianRentListPrice_studio/City_MedianRentalPrice_Studio.csv",
          "studio", "data/city_rental_median_price_studio_insert.sql")