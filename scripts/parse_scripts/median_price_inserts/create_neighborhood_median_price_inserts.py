def break_into_line_parts(line):
    parts = []
    c_idx = 0
    while c_idx < len(line):
        if line[c_idx] != '\"':
            word = ""
            while line[c_idx] != ',':
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
            while line[c_idx] != '\"':
                word += line[c_idx]
                c_idx += 1
            next_idx = c_idx + 1
            if next_idx < len(line):
                if line[next_idx] == ',':
                    c_idx += 2
                else:
                    c_idx += 1
            parts.append(word)

    return parts

def all_homes():
    insert_lines = []
    month_year_list = []
    with open("data/homeListings_Sales/medianListPrice/Neighborhood_MedianListingPrice_AllHomes.csv", "r", encoding="latin-1") as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = break_into_line_parts(line)
            if line_count == 0:
                month_year_list = line_parts[6:]
                line_count += 1
                continue

            neighborhood_name = line_parts[0].strip("\"")
            city_name = line_parts[1].strip("\"")
            state_code = line_parts[2].strip("\"")
            county_name = line_parts[4].strip("\"")
            city_name = city_name.replace('\'', '\'\'')
            county_name = county_name.replace('\'', '\'\'')
            neighborhood_name = neighborhood_name.replace('\'', '\'\'')

            neighborhood_select = "(select neighborhood.id from neighborhood " \
                                  "inner join city on neighborhood.city_id = city.id " \
                                  "inner join county on city.county_id = county.id " \
                                  "inner join state on county.state_id = state.id " \
                                  "where neighborhood.name = '" + neighborhood_name + \
                                  "' and city.name = '" + \
                                  city_name + "' and county.name = '" + county_name + "' " \
                                                                                  "and state.state_code = '" + state_code + "')"
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'all')"
            for idx in range(6, len(line_parts), 1):
                if line_parts[idx].strip("\"") != "":
                    list_price = int(round(float(line_parts[idx].strip("\""))))
                    insert_line = "INSERT INTO neighborhood_median_price (neighborhood_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + neighborhood_select + "," + home_type_select  + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "','"  \
                                  + str(list_price) + "');"
                else:
                    insert_line = "INSERT INTO neighborhood_median_price (neighborhood_id, home_type_id, year_month, list_price)" + \
                                  " VALUES(" + neighborhood_select + "," + home_type_select  + ",'" + month_year_list[
                                      idx - 6].strip("\"") + "',null);"

                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/neighborhood_median_price_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

all_homes()