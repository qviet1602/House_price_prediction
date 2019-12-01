def break_into_line_parts(line):
    parts = []
    c_idx = 0
    while c_idx < len(line):
        if line[c_idx] != '"':
            word = ""
            while line[c_idx] != ",":
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
            while line[c_idx] != '"':
                word += line[c_idx]
                c_idx += 1
            next_idx = c_idx + 1
            if next_idx < len(line):
                if line[next_idx] == ",":
                    c_idx += 2
                else:
                    c_idx += 1
            parts.append(word)

    return parts


def process_data(input_file_name, feature, output_file_name):
    insert_lines = []
    month_year_list = []
    with open(input_file_name, "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = break_into_line_parts(line)
            if line_count == 0:
                month_year_list = line_parts[6:]
                line_count += 1
                continue

            neighborhood_name = line_parts[0].strip('"')
            city_name = line_parts[1].strip('"')
            state_code = line_parts[2].strip('"')
            county_name = line_parts[4].strip('"')
            city_name = city_name.replace("'", "''")
            county_name = county_name.replace("'", "''")
            neighborhood_name = neighborhood_name.replace("'", "''")

            neighborhood_select = (
                "(select neighborhood.id from neighborhood "
                "inner join city on neighborhood.city_id = city.id "
                "inner join county on city.county_id = county.id "
                "inner join state on county.state_id = state.id "
                "where neighborhood.name = '"
                + neighborhood_name
                + "' and city.name = '"
                + city_name
                + "' and county.name = '"
                + county_name
                + "' "
                "and state.state_code = '" + state_code + "')"
            )
            home_type_select = (
                "(SELECT id from home_type where type = 'rental' and feature = '"
                + feature
                + "')"
            )
            for idx in range(6, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    list_price = int(round(float(line_parts[idx].strip('"'))))
                    insert_line = (
                        "INSERT INTO neighborhood_median_price (neighborhood_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + neighborhood_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 6].strip('"')
                        + "','"
                        + str(list_price)
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO neighborhood_median_price (neighborhood_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + neighborhood_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 6].strip('"')
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
    "data/rentalListings/medianRentListPrice_1bedroom/Neighborhood_MedianRentalPrice_1Bedroom.csv",
    "oneBedroom",
    "data/neighborhood_rental_median_price_1bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_2bedroom/Neighborhood_MedianRentalPrice_2Bedroom.csv",
    "twoBedroom",
    "data/neighborhood_rental_median_price_2bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_3bedroom/Neighborhood_MedianRentalPrice_3Bedroom.csv",
    "threeBedroom",
    "data/neighborhood_rental_median_price_3bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_4bedroom/Neighborhood_MedianRentalPrice_4Bedroom.csv",
    "fourBedroom",
    "data/neighborhood_rental_median_price_4bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_5PlusBedroom/Neighborhood_MedianRentalPrice_5BedroomOrMore.csv",
    "fivePlusBedroom",
    "data/neighborhood_rental_median_price_5bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_condoCoop/Neighborhood_MedianRentalPrice_CondoCoop.csv",
    "condoCoOp",
    "data/neighborhood_rental_median_price_condo_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_duplexTriplex/Neighborhood_MedianRentalPrice_DuplexTriplex.csv",
    "duplexTriplex",
    "data/neighborhood_rental_median_price_duplexTriplex_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_multiFamily/Neighborhood_MedianRentalPrice_Mfr5Plus.csv",
    "multiFamilyResidenceRental",
    "data/neighborhood_rental_median_price_multiFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_sfrCondoCoop/Neighborhood_MedianRentalPrice_AllHomes.csv",
    "all",
    "data/neighborhood_rental_median_price_all_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_singleFamilyResidence/Neighborhood_MedianRentalPrice_Sfr.csv",
    "singleFamilyResidenceRental",
    "data/neighborhood_rental_median_price_singleFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_studio/Neighborhood_MedianRentalPrice_Studio.csv",
    "studio",
    "data/neighborhood_rental_median_price_studio_insert.sql",
)
