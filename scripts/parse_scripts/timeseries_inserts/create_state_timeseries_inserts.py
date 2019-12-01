def get_state_code(state_name):
    state_names_map = {}
    state_names_map["Alabama"] = "AL"
    state_names_map["Alaska"] = "AK"
    state_names_map["Arizona"] = "AZ"
    state_names_map["Arkansas"] = "AR"
    state_names_map["California"] = "CA"
    state_names_map["Colorado"] = "CO"
    state_names_map["Connecticut"] = "CT"
    state_names_map["Delaware"] = "DE"
    state_names_map["Florida"] = "FL"
    state_names_map["Georgia"] = "GA"
    state_names_map["Hawaii"] = "HI"
    state_names_map["Idaho"] = "ID"
    state_names_map["Illinois"] = "IL"
    state_names_map["Indiana"] = "IN"
    state_names_map["Iowa"] = "IA"
    state_names_map["Kansas"] = "KS"
    state_names_map["Kentucky"] = "KY"
    state_names_map["Louisiana"] = "LA"
    state_names_map["Maine"] = "ME"
    state_names_map["Maryland"] = "MD"
    state_names_map["Massachusetts"] = "MA"
    state_names_map["Michigan"] = "MI"
    state_names_map["Minnesota"] = "MN"
    state_names_map["Mississippi"] = "MS"
    state_names_map["Missouri"] = "MO"
    state_names_map["Montana"] = "MT"
    state_names_map["Nebraska"] = "NE"
    state_names_map["Nevada"] = "NV"
    state_names_map["New Hampshire"] = "NH"
    state_names_map["New Jersey"] = "NJ"
    state_names_map["New Mexico"] = "NM"
    state_names_map["New York"] = "NY"
    state_names_map["North Carolina"] = "NC"
    state_names_map["North Dakota"] = "ND"
    state_names_map["Ohio"] = "OH"
    state_names_map["Oklahoma"] = "OK"
    state_names_map["Oregon"] = "OR"
    state_names_map["Pennsylvania"] = "PA"
    state_names_map["Rhode Island"] = "RI"
    state_names_map["South Carolina"] = "SC"
    state_names_map["South Dakota"] = "SD"
    state_names_map["Tennessee"] = "TN"
    state_names_map["Texas"] = "TX"
    state_names_map["Utah"] = "UT"
    state_names_map["Vermont"] = "VT"
    state_names_map["Virginia"] = "VA"
    state_names_map["Washington"] = "WA"
    state_names_map["West Virginia"] = "WV"
    state_names_map["Wisconsin"] = "WI"
    state_names_map["Wyoming"] = "WY"
    state_names_map["District of Columbia"] = "DC"
    state_names_map["Marshall Islands"] = "MH"

    return state_names_map.get(state_name, None)


def condo():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/condoCoOpTimeSeries/State_Zhvi_Condominum.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'condoCoOp')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_condo_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def oneBedroom():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/oneBedroomTimeSeries/State_Zhvi_1bedroom.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'oneBedroom')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_oneBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def twoBedroom():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/twoBedroomTimeSeries/State_Zhvi_2bedroom.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'twoBedroom')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_twoBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def threeBedroom():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/threeBedroomTimeSeries/State_Zhvi_3bedroom.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'threeBedroom')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_threeBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def fourBedroom():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/fourBedroomTimeSeries/State_Zhvi_4bedroom.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fourBedroom')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_fourBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def fivePlusBedroom():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/fivePlusBedroomTimeSeries/State_Zhvi_5BedroomOrMore.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fivePlusBedroom')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_fivePlusBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def singleFamilyHome():
    insert_lines = []
    month_year_list = []
    with open(
        "data/ZHVI/singleFamilyHomeTimeSeries/State_Zhvi_SingleFamilyResidence.csv", "r"
    ) as csv_file:
        line_count = 0
        for line in csv_file:
            line = line.rstrip("\n")
            line_parts = line.split(",")
            if line_count == 0:
                month_year_list = line_parts[3:]
                line_count += 1
                continue

            zillow_id = line_parts[0].strip('"')
            state_name = line_parts[1].strip('"')
            state_code = get_state_code(state_name)

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'singleFamilyHome')"
            state_select = (
                "(SELECT id from state where state_code='" + state_code + "')"
            )
            for idx in range(3, len(line_parts), 1):
                if line_parts[idx].strip('"') != "":
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "','"
                        + line_parts[idx].strip('"')
                        + "');"
                    )
                else:
                    insert_line = (
                        "INSERT INTO state_timeseries (state_id, home_type_id, year_month, zillow_id, index_value)"
                        + " VALUES("
                        + state_select
                        + ","
                        + home_type_select
                        + ",'"
                        + month_year_list[idx - 3].strip('"')
                        + "','"
                        + zillow_id
                        + "',null);"
                    )
                insert_lines.append(insert_line)

            line_count += 1

    sql_file = open("data/state_singleFamilyHome_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


condo()
oneBedroom()
twoBedroom()
threeBedroom()
fourBedroom()
fivePlusBedroom()
singleFamilyHome()
