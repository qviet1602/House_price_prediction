def all_homes():
    insert_lines = []
    month_year_list = []
    with open("data/homeListings_Sales/medianListPrice/County_MedianListingPrice_AllHomes.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'all')"
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

    sql_file = open("data/county_median_price_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

all_homes()