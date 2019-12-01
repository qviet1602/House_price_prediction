def condo():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/condoCoOpTimeSeries/County_Zhvi_Condominum.csv", "r") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'condoCoOp')"
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

    sql_file = open("data/county_condoCoOp_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def oneBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/oneBedroomTimeSeries/County_Zhvi_1bedroom.csv", "r") as csv_file:
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

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'oneBedroom')"
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

    sql_file = open("data/county_oneBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def twoBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/twoBedroomTimeSeries/County_Zhvi_2bedroom.csv", "r") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'twoBedroom')"
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

    sql_file = open("data/county_twoBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def threeBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/threeBedroomTimeSeries/County_Zhvi_3bedroom.csv", "r") as csv_file:
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

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'threeBedroom')"
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

    sql_file = open("data/county_threeBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def fourBedroom():
    insert_lines = []
    month_year_list = []

    with open("data/ZHVI/fourBedroomTimeSeries/County_Zhvi_4bedroom.csv", "r") as csv_file:
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

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fourBedroom')"
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

    sql_file = open("data/county_fourBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def fivePlusBedroom():
    insert_lines = []
    month_year_list = []

    with open("data/ZHVI/fivePlusBedroomTimeSeries/County_Zhvi_5BedroomOrMore.csv", "r") as csv_file:
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

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fivePlusBedroom')"
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

    sql_file = open("data/county_fivePlusBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()




def singleFamilyHome():
    insert_lines = []
    month_year_list = []

    with open("data/ZHVI/singleFamilyHomeTimeSeries/County_Zhvi_SingleFamilyResidence.csv", "r", encoding="latin-1") as csv_file:
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

            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'singleFamilyHome')"
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

    sql_file = open("data/county_singleFamilyHome_timeseries_insert.sql", "a")

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