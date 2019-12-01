def condo():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/condoCoOpTimeSeries/Zip_Zhvi_Condominum.csv", "r") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'condoCoOp')"
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

    sql_file = open("data/zip_condoCoOp_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def oneBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/oneBedroomTimeSeries/Zip_Zhvi_1bedroom.csv", "r") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'oneBedroom')"
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

    sql_file = open("data/zip_oneBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def twoBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/twoBedroomTimeSeries/Zip_Zhvi_2bedroom.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'twoBedroom')"
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

    sql_file = open("data/zip_twoBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def threeBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/threeBedroomTimeSeries/Zip_Zhvi_3bedroom.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'threeBedroom')"
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

    sql_file = open("data/zip_threeBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def fourBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/fourBedroomTimeSeries/Zip_Zhvi_4bedroom.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fourBedroom')"
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

    sql_file = open("data/zip_fourBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()

def fivePlusBedroom():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/fivePlusBedroomTimeSeries/Zip_Zhvi_5BedroomOrMore.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'fivePlusBedroom')"
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

    sql_file = open("data/zip_fiveBedroom_timeseries_insert.sql", "a")

    for line in insert_lines:
        sql_file.write(line)
        sql_file.write("\n")

    sql_file.close()


def singleFamilyHome():
    insert_lines = []
    month_year_list = []
    with open("data/ZHVI/singleFamilyHomeTimeSeries/Zip_Zhvi_SingleFamilyResidence.csv", "r", encoding="latin-1") as csv_file:
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
            home_type_select = "(SELECT id from home_type where type = 'purchase' and feature = 'singleFamilyHome')"
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

    sql_file = open("data/zip_singleFamily_timeseries_insert.sql", "a")

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