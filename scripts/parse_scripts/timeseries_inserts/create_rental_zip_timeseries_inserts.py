def multiFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/multiFamilyTimeSeries/Zip_Zri_MultiFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[7:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            zipcode = line_parts[1].strip("\"")
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'multiFamilyResidenceRental')"
            zipcode_select = "(select zipcode.id from zipcode " \
                                  + "where zipcode.zip_code = '" + zipcode + "' limit 1)"
            for idx in range(7, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO zip_timeseries (zipcode_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + zipcode_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO zip_timeseries (zipcode_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + zipcode_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/zip_rental_multiFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def singleFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/sFRTimeSeries/Zip_Zri_SingleFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[7:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            zipcode = line_parts[1].strip("\"")
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'singleFamilyResidenceRental')"
            zipcode_select = "(select zipcode.id from zipcode " \
                             + "where zipcode.zip_code = '" + zipcode + "' limit 1)"
            for idx in range(7, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO zip_timeseries (zipcode_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + zipcode_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO zip_timeseries (zipcode_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + zipcode_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/zip_rental_singleFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


multiFamily()
singleFamily()