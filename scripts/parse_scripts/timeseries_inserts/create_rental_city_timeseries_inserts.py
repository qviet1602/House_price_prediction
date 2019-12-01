def multiFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/multiFamilyTimeSeries/City_Zri_MultiFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[6:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            city_name = line_parts[1].strip("\"")
            state_code = line_parts[2].strip("\"")
            county_name = line_parts[4].strip("\"")
            city_name = city_name.replace('\'', '\'\'')
            county_name = county_name.replace('\'', '\'\'')
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'multiFamilyResidenceRental')"
            city_select = "(select city.id from city inner join county on city.county_id = county.id " \
                          "inner join state on county.state_id = state.id where county.name ='" + county_name \
                            + "' and state.state_code = '" + state_code + "' and city.name = '" + city_name + "')"
            for idx in range(6, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO city_timeseries (city_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO city_timeseries (city_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/city_rental_multiFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def singleFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/sFRTimeSeries/City_Zri_SingleFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[6:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            city_name = line_parts[1].strip("\"")
            state_code = line_parts[2].strip("\"")
            county_name = line_parts[4].strip("\"")
            city_name = city_name.replace('\'', '\'\'')
            county_name = county_name.replace('\'', '\'\'')

            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'singleFamilyResidenceRental')"
            city_select = "(select city.id from city inner join county on city.county_id = county.id " \
                          "inner join state on county.state_id = state.id where county.name ='" + county_name \
                          + "' and state.state_code = '" + state_code + "' and city.name = '" + city_name + "')"
            for idx in range(6, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO city_timeseries (city_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO city_timeseries (city_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + city_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/city_rental_singleFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

multiFamily()
singleFamily()