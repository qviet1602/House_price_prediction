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

            zipcode = line_parts[0].strip('"')
            zipcode_select = (
                "(select zipcode.id from zipcode "
                + "where zipcode.zip_code = '"
                + zipcode
                + "' limit 1)"
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
                        "INSERT INTO zip_median_price (zipcode_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + zipcode_select
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
                        "INSERT INTO zip_median_price (zipcode_id, home_type_id, year_month, list_price)"
                        + " VALUES("
                        + zipcode_select
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
    "data/rentalListings/medianRentListPrice_1bedroom/Zip_MedianRentalPrice_1Bedroom.csv",
    "oneBedroom",
    "data/zip_rental_median_price_1bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_2bedroom/Zip_MedianRentalPrice_2Bedroom.csv",
    "twoBedroom",
    "data/zip_rental_median_price_2bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_3bedroom/Zip_MedianRentalPrice_3Bedroom.csv",
    "threeBedroom",
    "data/zip_rental_median_price_3bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_4bedroom/Zip_MedianRentalPrice_4Bedroom.csv",
    "fourBedroom",
    "data/zip_rental_median_price_4bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_5PlusBedroom/Zip_MedianRentalPrice_5BedroomOrMore.csv",
    "fivePlusBedroom",
    "data/zip_rental_median_price_5bedroom_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_condoCoop/Zip_MedianRentalPrice_CondoCoop.csv",
    "condoCoOp",
    "data/zip_rental_median_price_condo_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_duplexTriplex/Zip_MedianRentalPrice_DuplexTriplex.csv",
    "duplexTriplex",
    "data/zip_rental_median_price_duplexTriplex_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_multiFamily/Zip_MedianRentalPrice_Mfr5Plus.csv",
    "multiFamilyResidenceRental",
    "data/zip_rental_median_price_multiFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_sfrCondoCoop/Zip_MedianRentalPrice_AllHomes.csv",
    "all",
    "data/zip_rental_median_price_all_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_singleFamilyResidence/Zip_MedianRentalPrice_Sfr.csv",
    "singleFamilyResidenceRental",
    "data/zip_rental_median_price_singleFamilyResidenceRental_insert.sql",
)

process_data(
    "data/rentalListings/medianRentListPrice_studio/Zip_MedianRentalPrice_Studio.csv",
    "studio",
    "data/zip_rental_median_price_studio_insert.sql",
)
