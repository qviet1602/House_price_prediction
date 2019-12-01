def multiFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/multiFamilyTimeSeries/County_Zri_MultiFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[7:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            county_name = line_parts[1].strip("\"")
            state_code = line_parts[2].strip("\"")
            county_name = county_name.replace('\'', '\'\'')
            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'multiFamilyResidenceRental')"
            county_select = "(select county.id from county inner join state on county.state_id = state.id where county.name ='" + county_name \
                            + "' and state.state_code = '" + state_code + "')"
            for idx in range(7, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO county_timeseries (county_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO county_timeseries (county_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/county_rental_multiFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def singleFamily():
    insert_lines = []
    month_year_list = []
    with open("data/ZRI/sFRTimeSeries/County_Zri_SingleFamilyResidenceRental.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[7:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip("\"")
            county_name = line_parts[1].strip("\"")
            state_code = line_parts[2].strip("\"")
            county_name = county_name.replace('\'', '\'\'')

            home_type_select = "(SELECT id from home_type where type = 'rental' and feature = 'singleFamilyResidenceRental')"
            county_select = "(select county.id from county inner join state on county.state_id = state.id where county.name ='" + county_name \
                            + "' and state.state_code = '" + state_code + "')"
            for idx in range(7, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    insert_line = "INSERT INTO county_timeseries (county_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "','" + line_parts[idx].strip("\"") + "');"
                else:
                    insert_line = "INSERT INTO county_timeseries (county_id, home_type_id, year_month, zillow_id, index_value)" + \
                                  " VALUES(" + county_select + "," + home_type_select + ",'" + month_year_list[
                                      idx - 7].strip("\"") + "','" + zillow_id + \
                                  "',null);"
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/county_rental_singleFamily_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


multiFamily()
singleFamily()