def all_homes():
    insert_lines = []
    month_year_list = []
    with open("data/homeListings_Sales/medianListPrice/City_MedianListingPrice_AllHomes.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'all')"
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

    sql_file = open("data/city_median_price_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

all_homes()