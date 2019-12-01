# Standard Library
from decimal import Decimal
from collections import OrderedDict

# Third Party Stuff
import numpy as np
import scipy.spatial.distance as dst
from django.db import connection
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import (
    api_view,
    authentication_classes,
    permission_classes,
)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_states(request):
    if request.method == "GET":
        states_query = (
            "select state_id, string_agg(DISTINCT home_type_id::text, ',') from state_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (1, 2, 3, 4, 5, 6, 9) group by state_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '1,2,3,4,5,6,9'"
        )

        with connection.cursor() as cursor:
            cursor.execute(states_query)
            state_rows = cursor.fetchall()

        state_id_string = ""
        for each_row in state_rows:
            each_county_id = each_row[0]
            state_id_string += "'" + str(each_county_id) + "',"

        state_id_string = state_id_string[:-1]

        state_info_query = (
            "select state.id, state.name from state where state.id in ("
            + state_id_string
            + ") order by state.name"
        )
        with connection.cursor() as cursor:
            cursor.execute(state_info_query)
            state_data_rows = cursor.fetchall()

        data = []
        for each_state in state_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_state[1]
            each_data_dict["id"] = each_state[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


def list_states_rental(request):
    if request.method == "GET":
        states_query = (
            "select state_id, string_agg(DISTINCT year_month, ','), string_agg(DISTINCT home_type_id::text, ',') from state_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (7, 8) group by state_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '7,8' "
            "and string_agg(DISTINCT year_month, ',') = '2010-12,2011-12,2012-12,2013-12,2014-12,2015-12,2016-12,2017-12,2018-12,2019-09'"
        )

        with connection.cursor() as cursor:
            cursor.execute(states_query)
            state_rows = cursor.fetchall()

        state_id_string = ""
        for each_row in state_rows:
            each_county_id = each_row[0]
            state_id_string += "'" + str(each_county_id) + "',"

        state_id_string = state_id_string[:-1]

        state_info_query = (
            "select state.id, state.name from state where state.id in ("
            + state_id_string
            + ") order by state.name"
        )
        with connection.cursor() as cursor:
            cursor.execute(state_info_query)
            state_data_rows = cursor.fetchall()

        data = []
        for each_state in state_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_state[1]
            each_data_dict["id"] = each_state[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_counties_purchase(request):
    if request.method == "GET":
        counties_query = (
            "select county_id, string_agg(DISTINCT home_type_id::text, ',') from county_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (1, 2, 3, 4, 5, 6, 9) group by county_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '1,2,3,4,5,6,9'"
        )
        with connection.cursor() as cursor:
            cursor.execute(counties_query)
            county_rows = cursor.fetchall()

        county_id_string = ""
        for each_row in county_rows:
            each_county_id = each_row[0]
            county_id_string += "'" + str(each_county_id) + "',"

        county_id_string = county_id_string[:-1]

        county_info_query = (
            "select county.id, county.name, state.name from county inner join state on county.state_id = state.id where county.id in ("
            + county_id_string
            + ") order by state.name, county.name"
        )
        with connection.cursor() as cursor:
            cursor.execute(county_info_query)
            county_data_rows = cursor.fetchall()

        data = []
        for each_county in county_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_county[1] + " (" + each_county[2] + ")"
            each_data_dict["id"] = each_county[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_counties_rental(request):
    if request.method == "GET":
        counties_query = (
            "select county_id, string_agg(DISTINCT year_month, ','), string_agg(DISTINCT home_type_id::text, ',') from county_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (7, 8) group by county_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '7,8' "
            "and string_agg(DISTINCT year_month, ',') = '2010-12,2011-12,2012-12,2013-12,2014-12,2015-12,2016-12,2017-12,2018-12,2019-09'"
        )
        with connection.cursor() as cursor:
            cursor.execute(counties_query)
            county_rows = cursor.fetchall()

        county_id_string = ""
        for each_row in county_rows:
            each_county_id = each_row[0]
            county_id_string += "'" + str(each_county_id) + "',"

        county_id_string = county_id_string[:-1]

        county_info_query = (
            "select county.id, county.name, state.name from county inner join state on county.state_id = state.id where county.id in ("
            + county_id_string
            + ") order by state.name, county.name"
        )
        with connection.cursor() as cursor:
            cursor.execute(county_info_query)
            county_data_rows = cursor.fetchall()

        data = []
        for each_county in county_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_county[1] + " (" + each_county[2] + ")"
            each_data_dict["id"] = each_county[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_zips_purchase(request):
    if request.method == "GET":
        zips_query = (
            "select zipcode_id, string_agg(DISTINCT home_type_id::text, ',') from zip_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (1, 2, 3, 4, 5, 6, 9) group by zipcode_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '1,2,3,4,5,6,9'"
        )
        with connection.cursor() as cursor:
            cursor.execute(zips_query)
            zip_rows = cursor.fetchall()

        zipcode_id_string = ""
        for each_row in zip_rows:
            each_county_id = each_row[0]
            zipcode_id_string += "'" + str(each_county_id) + "',"

        zipcode_id_string = zipcode_id_string[:-1]

        zipcode_info_query = (
            "select zipcode.id, zipcode.zip_code, state.name from zipcode inner join state on zipcode.state_id = state.id where zipcode.id in ("
            + zipcode_id_string
            + ") order by state.name, zipcode.zip_code"
        )
        with connection.cursor() as cursor:
            cursor.execute(zipcode_info_query)
            zip_data_rows = cursor.fetchall()

        data = []
        for each_zip in zip_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_zip[1] + " (" + each_zip[2] + ")"
            each_data_dict["id"] = each_zip[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


def list_zips_rental(request):
    if request.method == "GET":
        zips_query = (
            "select zipcode_id, string_agg(DISTINCT year_month, ','), string_agg(DISTINCT home_type_id::text, ',') from zip_timeseries "
            "where index_value is not null and (year_month like '201%-12' or year_month = '2019-09') "
            "and home_type_id in (7, 8) group by zipcode_id "
            "having string_agg(DISTINCT home_type_id::text, ',') = '7,8' "
            "and string_agg(DISTINCT year_month, ',') = '2010-12,2011-12,2012-12,2013-12,2014-12,2015-12,2016-12,2017-12,2018-12,2019-09'"
        )

        with connection.cursor() as cursor:
            cursor.execute(zips_query)
            zip_rows = cursor.fetchall()

        zipcode_id_string = ""
        for each_row in zip_rows:
            each_county_id = each_row[0]
            zipcode_id_string += "'" + str(each_county_id) + "',"
        zipcode_id_string = zipcode_id_string[:-1]

        zipcode_info_query = (
            "select zipcode.id, zipcode.zip_code, state.name from zipcode inner join state on zipcode.state_id = state.id where zipcode.id in ("
            + zipcode_id_string
            + ") order by state.name, zipcode.zip_code"
        )
        with connection.cursor() as cursor:
            cursor.execute(zipcode_info_query)
            zip_data_rows = cursor.fetchall()

        data = []
        for each_zip in zip_data_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_zip[1] + " (" + each_zip[2] + ")"
            each_data_dict["id"] = each_zip[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_state_data_purchase(request):
    if request.method == "GET":
        state_id = request.GET.get("state_id", 23)
        all_years_query = "select distinct(substr(year_month, 1, 4)) from state_timeseries where state_id = %s order by substr(year_month, 1, 4)"
        with connection.cursor() as cursor:
            cursor.execute(all_years_query, [state_id])
            years_rows = cursor.fetchall()

        last_year_month_query = "select year_month from state_timeseries where state_id = %s and year_month like %s order by year_month desc limit 1"

        with connection.cursor() as cursor:
            cursor.execute(last_year_month_query, [state_id, "2019%"])
            last_year_row = cursor.fetchone()

        all_last_year_months = []

        for each_year_row in years_rows:
            all_last_year_months.append(each_year_row[0] + "-12")

        all_last_year_months.append(last_year_row[0])

        all_last_year_months_str = ""

        for each in all_last_year_months:
            all_last_year_months_str = all_last_year_months_str + "'" + each + "',"

        all_last_year_months_str = all_last_year_months_str[:-1]

        home_types = [
            "condoCoOp",
            "oneBedroom",
            "twoBedroom",
            "threeBedroom",
            "fourBedroom",
            "fivePlusBedroom",
            "singleFamilyHome",
        ]
        data = []
        for each_home_type in home_types:
            each_data_dict = {}
            query = (
                "select index_value, year_month "
                "from state_timeseries inner join state on state_timeseries.state_id = state.id "
                "where home_type_id = (select id from home_type where type=%s and feature=%s) "
                "and state.id = %s and year_month in (" + all_last_year_months_str + ")"
            )

            with connection.cursor() as cursor:
                cursor.execute(query, ["purchase", each_home_type, state_id])
                home_data_rows = cursor.fetchall()

            home_data = []
            for each_home_data_row in home_data_rows:
                each_home_data_dict = {}
                each_home_data_dict["list_price"] = each_home_data_row[0]
                each_home_data_dict["year"] = int(each_home_data_row[1][0:4])
                home_data.append(each_home_data_dict)

            each_data_dict[each_home_type] = home_data
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_state_data_rental(request):
    if request.method == "GET":
        state_id = request.GET.get("state_id", 47)

        home_types = ["singleFamilyResidenceRental", "multiFamilyResidenceRental"]
        data = []
        for each_home_type in home_types:
            last_year_query = (
                "select year_month, index_value from state_timeseries where state_id = %s "
                "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id "
                "in (select id from home_type where type=%s and feature=%s) order by year_month desc"
            )

            with connection.cursor() as cursor:
                cursor.execute(
                    last_year_query,
                    [state_id, "%-12", "2019-09", "rental", each_home_type],
                )
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict["list_price"] = each_row[1]
                each_data_dict["year"] = each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_county_data_purchase(request):
    if request.method == "GET":
        county_id = request.GET.get("county_id", 1290)

        home_types = [
            "condoCoOp",
            "oneBedroom",
            "twoBedroom",
            "threeBedroom",
            "fourBedroom",
            "fivePlusBedroom",
            "singleFamilyHome",
        ]
        data = []
        for each_home_type in home_types:
            last_year_query = (
                "select year_month, index_value from county_timeseries where county_id = %s "
                "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id "
                "in (select id from home_type where type=%s and feature=%s) order by year_month desc"
            )

            with connection.cursor() as cursor:
                cursor.execute(
                    last_year_query,
                    [county_id, "201%-12", "2019-09", "purchase", each_home_type],
                )
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict["list_price"] = each_row[1]
                each_data_dict["year"] = each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_county_data_rental(request):
    if request.method == "GET":
        county_id = request.GET.get("county_id", 706)

        home_types = ["singleFamilyResidenceRental", "multiFamilyResidenceRental"]
        data = []
        for each_home_type in home_types:
            last_year_query = (
                "select year_month, index_value from county_timeseries where county_id = %s "
                "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id "
                "in (select id from home_type where type=%s and feature=%s) order by year_month desc"
            )

            with connection.cursor() as cursor:
                cursor.execute(
                    last_year_query,
                    [county_id, "%-12", "2019-09", "rental", each_home_type],
                )
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict["list_price"] = each_row[1]
                each_data_dict["year"] = each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_zip_data_purchase(request):
    if request.method == "GET":
        zipcode_id = request.GET.get("zipcode_id", 14101)

        home_types_map = {}

        home_types_map[1] = "condoCoOp"
        home_types_map[2] = "oneBedroom"
        home_types_map[3] = "twoBedroom"
        home_types_map[4] = "threeBedroom"
        home_types_map[5] = "fourBedroom"
        home_types_map[6] = "fivePlusBedroom"
        home_types_map[9] = "singleFamilyHome"

        data_query = (
            "select year_month, index_value, home_type_id from zip_timeseries where zipcode_id = %s "
            "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id in (1, 2, 3, 4, 5, 6, 9) "
            "order by home_type_id, year_month desc"
        )
        data = []
        with connection.cursor() as cursor:
            cursor.execute(data_query, [zipcode_id, "201%-12", "2019-09"])
            data_rows = cursor.fetchall()

        dictionary = {}
        for each_row in data_rows:
            key = home_types_map.get(int(each_row[2]), None)
            print("Key ", key, each_row[2])
            arr_data = []
            if key is not None and key in dictionary.keys():
                arr_data = dictionary.get(key)
            arr_data.append({"list_price": each_row[1], "year": each_row[0][0:4]})
            dictionary[key] = arr_data

        for each_key in dictionary.keys():
            current_data_dict = {}
            current_data_dict[each_key] = dictionary[each_key]
            data.append(current_data_dict)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_node_stats(request):
    if request.method == "GET":
        node_data = request.GET.get("node_data", "state_Alabama")
        node_type, node_id = node_data.split("_")
        statistics = {}
        if node_type == "state":
            state_query = "select id from state where name = %s"
            with connection.cursor() as cursor:
                cursor.execute(state_query, [node_id])
                state_row = cursor.fetchone()

            node_id = state_row[0]

            crime_data_query = (
                "select avg(violent_crime), avg(property_crime) from crime_data where zipcode_id "
                "in (select id from zipcode where zipcode.state_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            if violent_crime is not None:
                statistics["violent_crime"] = round(violent_crime, 2)
            if property_crime is not None:
                statistics["property_crime"] = round(property_crime, 2)

            schools_query = (
                "select count(*) from school_data where schooldigger_rating is not null "
                "and schooldigger_rating >= 3 and zipcode_id in (select id from zipcode where state_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics["num_of_schools"] = num_of_schools

            annual_income_query = (
                "select avg(avg_annual_income), avg(median_annual_income) from annual_income where zipcode_id "
                "in (select id from zipcode where state_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]
            if avg_avg_annual_income is not None:
                statistics["avg_avg_annual_income"] = round(avg_avg_annual_income, 2)
                us_avg = Decimal(28555.0)
                is_affordable = False
                avg_diff = avg_avg_annual_income - us_avg

                if avg_diff < 0 or avg_diff < 10000:
                    is_affordable = True
                statistics["is_affordable"] = is_affordable
            if avg_median_annual_income is not None:
                statistics["avg_median_annual_income"] = round(
                    avg_median_annual_income, 2
                )

        elif node_type == "county":
            node_id = int(node_id)
            crime_data_query = (
                "select avg(violent_crime), avg(property_crime) from crime_data where zipcode_id "
                "in (select id from zipcode where county_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            if violent_crime is not None:
                statistics["violent_crime"] = round(violent_crime, 2)
            if property_crime is not None:
                statistics["property_crime"] = round(property_crime, 2)

            schools_query = (
                "select count(*) from school_data where schooldigger_rating is not null "
                "and schooldigger_rating >= 3 and zipcode_id in (select id from zipcode where county_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics["num_of_schools"] = num_of_schools

            annual_income_query = (
                "select avg(avg_annual_income), avg(median_annual_income) from annual_income where zipcode_id "
                "in (select id from zipcode where county_id = %s)"
            )

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]

            if avg_avg_annual_income is not None:
                statistics["avg_avg_annual_income"] = round(avg_avg_annual_income, 2)
                us_avg = Decimal(28555.0)
                is_affordable = False
                avg_diff = avg_avg_annual_income - us_avg
                if avg_diff < 0 or avg_diff < 10000:
                    is_affordable = True

                statistics["is_affordable"] = is_affordable

            if avg_median_annual_income is not None:
                statistics["avg_median_annual_income"] = round(
                    avg_median_annual_income, 2
                )

        elif node_type == "zipcode":
            node_id = int(node_id)
            print("Zipcode Id ", node_id)
            crime_data_query = "select violent_crime, property_crime from crime_data where zipcode_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            if violent_crime is not None:
                statistics["violent_crime"] = round(violent_crime, 2)
            if property_crime is not None:
                statistics["property_crime"] = round(property_crime, 2)

            schools_query = (
                "select count(*) from school_data where schooldigger_rating is not null "
                "and schooldigger_rating >= 3 and zipcode_id = %s"
            )

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics["num_of_schools"] = num_of_schools

            annual_income_query = "select avg_annual_income, median_annual_income from annual_income where zipcode_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]
            if avg_avg_annual_income is not None:
                statistics["avg_avg_annual_income"] = round(avg_avg_annual_income, 2)
                us_avg = Decimal(28555.0)
                is_affordable = False
                avg_diff = avg_avg_annual_income - us_avg
                if avg_diff < 0 or avg_diff < 10000:
                    is_affordable = True

                statistics["is_affordable"] = is_affordable

            if avg_median_annual_income is not None:
                statistics["avg_median_annual_income"] = round(
                    avg_median_annual_income, 2
                )

        return JsonResponse(statistics, safe=False)


def list_best_counties(state_name):
    # Find counties with least crime rate
    final_county_ids = set()
    limit = 40

    total_ids = 0
    iteration = 0
    while total_ids < 5:
        iteration += 1
        crime_data_query = (
            "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from "
            "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
            "inner join county on zipcode.county_id = county.id "
            "inner join state on zipcode.state_id = state.id where state.name = %s  "
            "group by county.name, zipcode.county_id "
            "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc limit %s"
        )
        with connection.cursor() as cursor:
            cursor.execute(crime_data_query, [state_name, limit])
            crime_data_row = cursor.fetchall()

        county_ids1 = []
        for each_row in crime_data_row:
            county_ids1.append(each_row[2])

        school_data_row = (
            "select count(*), zipcode.county_id, county.name from school_data "
            "inner join zipcode on school_data.zipcode_id = zipcode.id "
            "inner join county on zipcode.county_id = county.id "
            "inner join state on zipcode.state_id = state.id "
            "where state.name = %s and schooldigger_rating is not null "
            "and schooldigger_rating > %s group by county.name, zipcode.county_id order by count(*) desc limit %s"
        )

        with connection.cursor() as cursor:
            cursor.execute(school_data_row, [state_name, 2, limit])
            school_data_row = cursor.fetchall()

        county_ids2 = []

        for each_row in school_data_row:
            county_ids2.append(each_row[1])

        annual_income_query = (
            "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from "
            "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
            "inner join county on zipcode.county_id = county.id "
            "inner join state on zipcode.state_id = state.id where state.name = %s  "
            "group by county.name, zipcode.county_id "
            "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc limit %s"
        )
        with connection.cursor() as cursor:
            cursor.execute(annual_income_query, [state_name, limit])
            annual_income_data_row = cursor.fetchall()

        county_ids3 = []
        for each_row in annual_income_data_row:
            county_ids3.append(each_row[2])

        first_common_data = []

        for i in range(len(county_ids1)):
            if county_ids1[i] in county_ids2:
                first_common_data.append(county_ids1[i])
        final_list = []
        for i in range(len(first_common_data)):
            if first_common_data[i] in county_ids3:
                final_list.append(first_common_data[i])

        total_ids = len(final_list)
        final_county_ids = final_list
        if total_ids < 5:
            limit += 100
        else:
            break

        if iteration > 4:
            break

    county_str = ""
    for each in final_county_ids:
        county_str = county_str + "'" + str(each) + "',"
    county_str = county_str[:-1]

    county_query = "select id, name from county where id in (" + county_str + ")"
    with connection.cursor() as cursor:
        cursor.execute(county_query)
        county_data_rows = cursor.fetchall()

    data = []

    for each_row in county_data_rows:
        each_data_dict = {}
        each_data_dict["id"] = each_row[0]

        each_data_dict["name"] = each_row[1]
        data.append(each_data_dict)

    data = data[0:5]
    return data


def list_best_zips(state_name):
    # Find zips with least crime rate
    final_zip_ids = set()
    limit = 40

    total_ids = 0
    iteration = 0
    while total_ids < 5:
        iteration += 1
        crime_data_query = (
            "select violent_crime, property_crime, zipcode_id, zipcode.zip_code from "
            "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id where state.name = %s  "
            "order by crime_data.violent_crime asc, crime_data.property_crime asc limit %s"
        )
        with connection.cursor() as cursor:
            cursor.execute(crime_data_query, [state_name, limit])
            crime_data_row = cursor.fetchall()

        zipcode_ids1 = []
        for each_row in crime_data_row:
            zipcode_ids1.append(each_row[2])

        school_data_row = (
            "select count(*), zipcode_id, zipcode.zip_code from school_data "
            "inner join zipcode on school_data.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id "
            "where state.name = %s and schooldigger_rating is not null "
            "and schooldigger_rating > %s group by zipcode_id, zipcode.zip_code order by count(*) desc limit %s"
        )

        with connection.cursor() as cursor:
            cursor.execute(school_data_row, [state_name, 2, limit])
            school_data_row = cursor.fetchall()

        zipcode_ids2 = []

        for each_row in school_data_row:
            zipcode_ids2.append(each_row[1])

        annual_income_query = (
            "select avg_annual_income, median_annual_income, zipcode_id, zipcode.zip_code from "
            "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id where state.name = %s  "
            "order by annual_income.avg_annual_income asc, annual_income.median_annual_income asc limit %s"
        )
        with connection.cursor() as cursor:
            cursor.execute(annual_income_query, [state_name, limit])
            annual_income_data_row = cursor.fetchall()

        zipcode_ids3 = []
        for each_row in annual_income_data_row:
            zipcode_ids3.append(each_row[2])

        first_common_data = []

        for i in range(len(zipcode_ids1)):
            if zipcode_ids1[i] in zipcode_ids2:
                first_common_data.append(zipcode_ids1[i])
        final_list = []
        for i in range(len(first_common_data)):
            if first_common_data[i] in zipcode_ids3:
                final_list.append(first_common_data[i])

        total_ids = len(final_list)
        final_zip_ids = final_list
        if total_ids < 5:
            limit += 100
        else:
            break

        if iteration > 10:
            break

    zip_str = ""
    for each in final_zip_ids:
        zip_str = zip_str + "'" + str(each) + "',"
    zip_str = zip_str[:-1]

    zip_query = "select id, zip_code from zipcode where id in (" + zip_str + ")"
    with connection.cursor() as cursor:
        cursor.execute(zip_query)
        zip_data_rows = cursor.fetchall()

    data = []

    for each_row in zip_data_rows:
        each_data_dict = {}
        each_data_dict["id"] = each_row[0]
        each_data_dict["name"] = each_row[1]
        data.append(each_data_dict)

    data = data[0:5]

    return data


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_best_counties(request):
    if request.method == "GET":
        state_name = request.GET.get("state_name", "Alabama")
        data = list_best_counties(state_name)

        return JsonResponse(data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_best_zips(request):
    if request.method == "GET":
        state_name = request.GET.get("state_name", "Alabama")

        data = list_best_zips(state_name)

        return JsonResponse(data, safe=False)


def list_safe_counties(state_name):
    crime_data_query = (
        "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from "
        "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
        "inner join county on zipcode.county_id = county.id "
        "inner join state on zipcode.state_id = state.id where state.name = %s  "
        "group by county.name, zipcode.county_id "
        "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc limit %s"
    )
    with connection.cursor() as cursor:
        cursor.execute(crime_data_query, [state_name, 5])
        crime_data_row = cursor.fetchall()

    data = []

    for each_row in crime_data_row:
        each_data_dict = {}
        each_data_dict["id"] = each_row[2]
        each_data_dict["name"] = each_row[3]
        data.append(each_data_dict)

    return data


def list_affordable_counties(state_name):
    min_price_query = (
        "select index_value from state_timeseries inner join state on state_timeseries.state_id = state.id where state.name='"
        + state_name
        + "' and index_value is not null and (year_month like '2019-%') "
    )

    with connection.cursor() as cursor:
        cursor.execute(min_price_query)
        min_price_row = cursor.fetchall()
    values = []
    for each in min_price_row:
        values.append(each[0])
    if len(values) == 0:
        min_value = 28555
    else:
        min_value = np.min(values)

    annual_income_query = (
        "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from "
        "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
        "inner join county on zipcode.county_id = county.id "
        "inner join state on zipcode.state_id = state.id where state.name = %s  "
        "group by county.name, zipcode.county_id having avg(median_annual_income) > %s "
        "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc limit %s"
    )

    with connection.cursor() as cursor:
        cursor.execute(annual_income_query, [state_name, int(min_value * 2), 5])
        annual_data_row = cursor.fetchall()

    data = []

    for each_row in annual_data_row:
        each_data_dict = {}
        each_data_dict["id"] = each_row[2]
        each_data_dict["name"] = each_row[3]
        data.append(each_data_dict)

    return data


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_safe_counties(request):
    if request.method == "GET":
        state_name = request.GET.get("state_name", "Alabama")

        data = list_safe_counties(state_name)

        return JsonResponse(data, safe=False)


def get_affordable_counties(request):
    if request.method == "GET":
        state_name = request.GET.get("state_name", "Alabama")

        data = list_affordable_counties(state_name)

        return JsonResponse(data, safe=False)


def get_similar_states(request):
    if request.method == "GET":
        selected_state = request.GET.get("state_name", "Alabama")

        # Get data for all three states and aggregate this data into one dataset
        crime_data_query = (
            "select avg(violent_crime), avg(property_crime), zipcode.state_id, state.name from "
            "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id  "
            "group by state.name, zipcode.state_id "
            "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc"
        )

        school_data_query = (
            "select count(*), zipcode.state_id, state.name from school_data "
            "inner join zipcode on school_data.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id "
            "where schooldigger_rating is not null "
            "and schooldigger_rating > %s group by state.name, zipcode.state_id order by count(*) desc"
        )

        annual_income_query = (
            "select avg(avg_annual_income), avg(median_annual_income), zipcode.state_id, state.name from "
            "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
            "inner join state on zipcode.state_id = state.id "
            "group by state.name, zipcode.state_id "
            "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc"
        )
        median_prices_query = (
            "select index_value, state_id, state.name from state_timeseries "
            "inner join state on state_timeseries.state_id = state.id where year_month = %s and home_type_id = %s"
        )

        with connection.cursor() as cursor:
            cursor.execute(crime_data_query)
            crime_data_rows = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(school_data_query, [2])
            school_data_rows = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(annual_income_query)
            annual_data_rows = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(median_prices_query, ["2019-09", 2])
            median_prices_rows = cursor.fetchall()

        # Now merge all this data into one

        crime_data_map_by_state = {}

        for each_row in crime_data_rows:
            crime_data_map_by_state[each_row[3]] = each_row

        school_data_map_by_state = {}

        for each_row in school_data_rows:
            school_data_map_by_state[each_row[2]] = each_row

        annual_data_map_by_state = {}

        for each_row in annual_data_rows:
            annual_data_map_by_state[each_row[3]] = each_row

        median_price_map_by_state = {}
        for each_row in median_prices_rows:
            median_price_map_by_state[each_row[2]] = each_row

        keys = crime_data_map_by_state.keys()
        full_dataset = []
        idx = 0
        states = {}
        for each_key in keys:
            each_data_instance = []
            crime_data = crime_data_map_by_state.get(each_key, None)
            school_data = school_data_map_by_state.get(each_key, None)
            annual_data = annual_data_map_by_state.get(each_key, None)
            median_price = median_price_map_by_state.get(each_key, None)

            if (
                crime_data is None
                or school_data is None
                or annual_data is None
                or median_price is None
            ):
                continue

            each_data_instance.append(crime_data[0])
            each_data_instance.append(crime_data[1])
            each_data_instance.append(school_data[0])
            each_data_instance.append(annual_data[0])
            each_data_instance.append(annual_data[1])
            each_data_instance.append(median_price[0])
            states[idx] = each_key
            idx += 1
            full_dataset.append(each_data_instance)

        numpy_dataset = np.array(full_dataset, dtype=np.float)

        similarity_values = dst.squareform(dst.pdist(numpy_dataset, "euclidean"))

        current_state_idx = None
        for idx in range(len(states)):
            state_name = states[idx]
            if selected_state == state_name:
                current_state_idx = idx

        interested_row = similarity_values[current_state_idx, :]

        dict = {}
        idx = 0
        for each in interested_row:
            dict[each] = idx
            idx += 1

        sorted_vals = sorted(dict.keys())

        similar_states = []

        for val in sorted_vals:
            if val == 0.0:
                continue
            if len(similar_states) < 3:
                current_idx = dict.get(val)
                state_name = states[current_idx]
                similar_states.append(state_name)
            else:
                break

        states_query = (
            "select id, state_code, name from state where name in (%s, %s, %s)"
        )
        with connection.cursor() as cursor:
            cursor.execute(states_query, similar_states)
            state_rows = cursor.fetchall()

        data = []

        for each_row in state_rows:
            each_data_dict = {}
            each_data_dict["name"] = each_row[2]
            each_data_dict["state_code"] = each_row[1]
            each_data_dict["id"] = each_row[0]

            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


def similar_counties(bucket_data, all_counties_str):

    # Get data for all best counties and aggregate this data into one dataset
    crime_data_query = (
        "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from "
        "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
        "inner join county on zipcode.county_id = county.id "
        "where zipcode.county_id in (" + all_counties_str + ") "
        "group by county.name, zipcode.county_id"
    )

    school_data_query = (
        "select count(*), zipcode.county_id, county.name from school_data "
        "inner join zipcode on school_data.zipcode_id = zipcode.id "
        "inner join county on zipcode.county_id = county.id where zipcode.county_id in ("
        + all_counties_str
        + ") "
        "and schooldigger_rating is not null "
        "and schooldigger_rating > 2 group by county.name, zipcode.county_id"
    )

    annual_income_query = (
        "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from "
        "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
        "inner join county on zipcode.county_id = county.id where zipcode.county_id in ("
        + all_counties_str
        + ") "
        "group by county.name, zipcode.county_id"
    )

    median_prices_query = (
        "select list_price, county_id, county.name from county_median_price "
        "inner join county on county_median_price.county_id = county.id where year_month = '2019-09' "
        "and home_type_id = 10 and county.id in (" + all_counties_str + ")"
    )

    with connection.cursor() as cursor:
        cursor.execute(crime_data_query)
        crime_data_rows = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(school_data_query)
        school_data_rows = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(annual_income_query)
        annual_data_rows = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(median_prices_query)
        median_price_rows = cursor.fetchall()

    # Now merge all this data into one

    crime_data_map = OrderedDict()

    for each_row in crime_data_rows:
        crime_data_map[each_row[2]] = each_row

    school_data_map = {}

    for each_row in school_data_rows:
        school_data_map[each_row[1]] = each_row

    annual_data_map = {}

    for each_row in annual_data_rows:
        annual_data_map[each_row[2]] = each_row

    median_data_map = {}

    for each_row in median_price_rows:
        median_data_map[each_row[1]] = each_row

    full_dataset = []
    idx = 0
    entities = {}
    entities_map = {}
    for each_bucket in bucket_data.keys():
        for county_id in bucket_data[each_bucket]:
            each_data_instance = []
            crime_data = crime_data_map.get(county_id, None)
            school_data = school_data_map.get(county_id, None)
            annual_data = annual_data_map.get(county_id, None)
            median_data = median_data_map.get(county_id, None)

            if (
                crime_data is None
                or school_data is None
                or annual_data is None
                or median_data is None
            ):
                continue

            each_data_instance.append(crime_data[0])
            each_data_instance.append(crime_data[1])
            each_data_instance.append(school_data[0])
            each_data_instance.append(annual_data[0])
            each_data_instance.append(annual_data[1])
            each_data_instance.append(median_data[0])
            entities[idx] = county_id
            entities_map[county_id] = crime_data[3]
            idx += 1
            full_dataset.append(each_data_instance)

    numpy_dataset = np.array(full_dataset, dtype=np.float)

    similarity_values = dst.squareform(dst.pdist(numpy_dataset, "euclidean"))

    rows = similarity_values.shape[0]
    all_idx_similarity_data = []
    for row in range(rows):
        full_column = similarity_values[row, :]
        current_map = {}
        idx = 0
        for each in full_column:
            current_map[each] = idx
            idx += 1

        sorted_keys = sorted(current_map.keys())
        each_idx_data = []
        for key in sorted_keys:
            each_idx_data.append(current_map.get(key))

        all_idx_similarity_data.append(each_idx_data)

    max_indexes = []
    indexes1 = []
    indexes2 = []
    indexes3 = []

    for idxes in entities.keys():
        county_id = entities[idxes]
        if county_id in bucket_data[0]:
            indexes1.append(idxes)
        elif county_id in bucket_data[1]:
            indexes2.append(idxes)
        elif county_id in bucket_data[2]:
            indexes3.append(idxes)

    if len(indexes1) > 0:
        max_indexes.append(np.max(indexes1))
    else:
        max_indexes.append(0)

    if len(indexes2) > 0:
        max_indexes.append(np.max(indexes2))
    else:
        max_indexes.append(0)

    if len(indexes3) > 0:
        max_indexes.append(np.max(indexes3))
    else:
        max_indexes.append(0)

    current_values = []
    bucket1_data = all_idx_similarity_data[0 : max_indexes[0] + 1]
    bucket2_data = all_idx_similarity_data[max_indexes[0] + 1 : max_indexes[1] + 1]
    if max_indexes[0] != 0:

        vals_1 = np.argwhere(
            (bucket1_data > max_indexes[0]) & (bucket1_data <= max_indexes[1])
        )
        similar_values_1 = []

        idx = 0
        for val_rows in range(vals_1.shape[0]):
            row_val = vals_1[val_rows, :][0]
            col_val = vals_1[val_rows, :][1]
            if row_val == idx:
                similar_values_1.append(bucket1_data[row_val][col_val])
                idx += 1

        vals_2 = np.argwhere(bucket1_data > max_indexes[1])
        similar_values_2 = []

        idx = 0

        for val_rows in range(vals_2.shape[0]):
            row_val = vals_2[val_rows, :][0]
            col_val = vals_2[val_rows, :][1]
            if row_val == idx:
                similar_values_2.append(bucket1_data[row_val][col_val])
                idx += 1

        if len(similar_values_1) == len(similar_values_2):
            for idx in range(len(similar_values_1)):
                current_values.append([similar_values_1[idx], similar_values_2[idx]])
        elif len(similar_values_1) == 0:
            for idx in range(len(similar_values_2)):
                current_values.append([similar_values_2[idx]])
        elif len(similar_values_2) == 0:
            for idx in range(len(similar_values_1)):
                current_values.append([similar_values_1[idx]])
        elif len(similar_values_1) < len(similar_values_2):
            for idx in range(len(similar_values_1)):
                current_values.append([similar_values_1[idx], similar_values_2[idx]])
            next_idx = idx
            while next_idx < len(similar_values_2):
                current_values.append([similar_values_2[next_idx]])
                next_idx += 1
        elif len(similar_values_2) < len(similar_values_1):
            for idx in range(len(similar_values_2)):
                current_values.append([similar_values_1[idx], similar_values_2[idx]])
            next_idx = idx
            while next_idx < len(similar_values_1):
                current_values.append([similar_values_1[next_idx]])
                next_idx += 1

    if max_indexes[2] != 0:
        vals_3 = np.argwhere(bucket2_data > max_indexes[1])

        similar_values_3 = []

        idx = 0
        for val_rows in range(vals_3.shape[0]):
            row_val = vals_3[val_rows, :][0]
            col_val = vals_3[val_rows, :][1]
            if row_val == idx:
                similar_values_3.append(bucket2_data[row_val][col_val])
                idx += 1

        for each in similar_values_3:
            current_values.append([each])

    data = []
    for each_row in range(len(current_values)):
        each_data_dict = {}
        each_data_dict["id"] = entities[each_row]
        each_data_dict["name"] = entities_map[each_data_dict["id"]]
        current_value = current_values[each_row]
        if len(current_value) == 2:
            similars = [current_value[0], current_value[1]]
        else:
            similars = [current_value[0]]

        similar_values = []
        for similar in similars:
            similar_data_dict = {}
            similar_data_dict["id"] = entities[similar]
            similar_data_dict["name"] = entities_map[similar_data_dict["id"]]
            similar_values.append(similar_data_dict)

        each_data_dict["similars"] = similar_values
        data.append(each_data_dict)

    return data


def similar_zips(bucket_data, all_zips_str):

    # Get data for all best zipcodes and aggregate this data into one dataset
    crime_data_query = (
        "select violent_crime, property_crime, zipcode.id, zipcode.zip_code from "
        "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id "
        "where zipcode.id in (" + all_zips_str + ")"
    )

    school_data_query = (
        "select count(*), zipcode.id, zipcode.zip_code from school_data "
        "inner join zipcode on school_data.zipcode_id = zipcode.id "
        "where zipcode.id in (" + all_zips_str + ") "
        "and schooldigger_rating is not null and schooldigger_rating > 2 "
        "group by zipcode.id, zipcode.zip_code"
    )

    annual_income_query = (
        "select avg_annual_income, median_annual_income, zipcode.id, zipcode.zip_code from "
        "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id "
        "where zipcode.id in (" + all_zips_str + ")"
    )

    with connection.cursor() as cursor:
        cursor.execute(crime_data_query)
        crime_data_rows = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(school_data_query)
        school_data_rows = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(annual_income_query)
        annual_data_rows = cursor.fetchall()

    # Now merge all this data into one

    crime_data_map = {}

    for each_row in crime_data_rows:
        crime_data_map[each_row[2]] = each_row

    school_data_map = {}

    for each_row in school_data_rows:
        school_data_map[each_row[1]] = each_row

    annual_data_map = {}

    for each_row in annual_data_rows:
        annual_data_map[each_row[2]] = each_row

    full_dataset = []
    idx = 0
    entities = {}
    entities_map = {}
    for each_bucket in bucket_data.keys():
        for zip_id in bucket_data[each_bucket]:

            each_data_instance = []
            crime_data = crime_data_map.get(zip_id, None)
            school_data = school_data_map.get(zip_id, None)
            annual_data = annual_data_map.get(zip_id, None)

            if crime_data is None or school_data is None or annual_data is None:
                continue

            each_data_instance.append(crime_data[0])
            each_data_instance.append(crime_data[1])
            each_data_instance.append(school_data[0])
            each_data_instance.append(annual_data[0])
            each_data_instance.append(annual_data[1])
            # each_data_instance.append(median_data[0])
            entities[idx] = zip_id
            entities_map[zip_id] = crime_data[3]
            idx += 1
            full_dataset.append(each_data_instance)

    numpy_dataset = np.array(full_dataset, dtype=np.float)

    similarity_values = dst.squareform(dst.pdist(numpy_dataset, "euclidean"))

    rows = similarity_values.shape[0]
    all_idx_similarity_data = []
    for row in range(rows):
        full_column = similarity_values[row, :]
        current_map = {}
        idx = 0
        for each in full_column:
            current_map[each] = idx
            idx += 1

        sorted_keys = sorted(current_map.keys())
        each_idx_data = []
        for key in sorted_keys:
            each_idx_data.append(current_map.get(key))

        all_idx_similarity_data.append(each_idx_data)

    max_indexes = []
    indexes1 = []
    indexes2 = []
    indexes3 = []

    for idxes in entities.keys():
        county_id = entities[idxes]
        if county_id in bucket_data[0]:
            indexes1.append(idxes)
        elif county_id in bucket_data[1]:
            indexes2.append(idxes)
        elif county_id in bucket_data[2]:
            indexes3.append(idxes)

    if len(indexes1) > 0:
        max_indexes.append(np.max(indexes1))
    else:
        max_indexes.append(0)

    if len(indexes2) > 0:
        max_indexes.append(np.max(indexes2))
    else:
        max_indexes.append(0)

    if len(indexes3) > 0:
        max_indexes.append(np.max(indexes3))
    else:
        max_indexes.append(0)

    bucket1_data = all_idx_similarity_data[0 : max_indexes[0] + 1]
    bucket2_data = all_idx_similarity_data[max_indexes[0] + 1 : max_indexes[1] + 1]

    vals_1 = np.argwhere(
        (bucket1_data > max_indexes[0]) & (bucket1_data <= max_indexes[1])
    )
    similar_values_1 = []

    idx = 0
    for val_rows in range(vals_1.shape[0]):
        row_val = vals_1[val_rows, :][0]
        col_val = vals_1[val_rows, :][1]
        if row_val == idx:
            similar_values_1.append(bucket1_data[row_val][col_val])
            idx += 1

    vals_2 = np.argwhere(bucket1_data > max_indexes[1])
    similar_values_2 = []

    idx = 0

    for val_rows in range(vals_2.shape[0]):
        row_val = vals_2[val_rows, :][0]
        col_val = vals_2[val_rows, :][1]
        if row_val == idx:
            similar_values_2.append(bucket1_data[row_val][col_val])
            idx += 1

    current_values = []
    if len(similar_values_1) == len(similar_values_2):
        for idx in range(len(similar_values_1)):
            current_values.append([similar_values_1[idx], similar_values_2[idx]])
    elif len(similar_values_1) == 0:
        for idx in range(len(similar_values_2)):
            current_values.append([similar_values_2[idx]])
    elif len(similar_values_2) == 0:
        for idx in range(len(similar_values_1)):
            current_values.append([similar_values_1[idx]])
    elif len(similar_values_1) < len(similar_values_2):
        for idx in range(len(similar_values_1)):
            current_values.append([similar_values_1[idx], similar_values_2[idx]])
        next_idx = idx
        while next_idx < len(similar_values_2):
            current_values.append([similar_values_2[next_idx]])
            next_idx += 1
    elif len(similar_values_2) < len(similar_values_1):
        for idx in range(len(similar_values_2)):
            current_values.append([similar_values_1[idx], similar_values_2[idx]])
        next_idx = idx
        while next_idx < len(similar_values_1):
            current_values.append([similar_values_1[next_idx]])
            next_idx += 1

    if max_indexes[2] != 0:
        vals_3 = np.argwhere(bucket2_data > max_indexes[1])

        similar_values_3 = []

        idx = 0
        for val_rows in range(vals_3.shape[0]):
            row_val = vals_3[val_rows, :][0]
            col_val = vals_3[val_rows, :][1]
            if row_val == idx:
                similar_values_3.append(bucket2_data[row_val][col_val])
                idx += 1

        for each in similar_values_3:
            current_values.append([each])

    data = []
    for each_row in range(len(current_values)):
        each_data_dict = {}
        each_data_dict["id"] = entities[each_row]
        each_data_dict["name"] = entities_map[each_data_dict["id"]]
        current_value = current_values[each_row]
        if len(current_value) == 2:
            similars = [current_value[0], current_value[1]]
        else:
            similars = [current_value[0]]

        similar_values = []
        for similar in similars:
            similar_data_dict = {}
            similar_data_dict["id"] = entities[similar]
            similar_data_dict["name"] = entities_map[similar_data_dict["id"]]
            similar_values.append(similar_data_dict)

        each_data_dict["similars"] = similar_values
        data.append(each_data_dict)

    return data


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_similar_all(request):
    if request.method == "GET":
        selected_states = request.GET.get("states", "Alabama_Texas_Kentucky")

        all_states = selected_states.split("_")

        all_counties = []

        county_id_state_map = {}
        bucket_data = {}
        index = 0
        for each_state in all_states:
            best_counties = list_best_counties(each_state)
            each_bucket_ids = []
            for each in best_counties:
                county_id_state_map[each["id"]] = each_state
                all_counties.append(each["id"])
                each_bucket_ids.append(each["id"])

            bucket_data[index] = each_bucket_ids

            index += 1

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(bucket_data, all_counties_str)

        final_data = dict()

        for each_data in data:
            county_id = each_data["id"]
            state_name = county_id_state_map[county_id]
            each_data["state_name"] = state_name
            similars = each_data["similars"]
            for each_similar in similars:
                state_name = county_id_state_map[each_similar["id"]]
                each_similar["state_name"] = state_name

        final_data["best_counties"] = data

        all_counties = []

        county_id_state_map = {}
        bucket_data = {}
        index = 0
        for each_state in all_states:
            best_counties = list_safe_counties(each_state)
            each_bucket_ids = []
            for each in best_counties:
                county_id_state_map[each["id"]] = each_state
                all_counties.append(each["id"])
                each_bucket_ids.append(each["id"])

            bucket_data[index] = each_bucket_ids

            index += 1

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(bucket_data, all_counties_str)

        for each_data in data:
            county_id = each_data["id"]
            state_name = county_id_state_map[county_id]
            each_data["state_name"] = state_name
            similars = each_data["similars"]
            for each_similar in similars:
                state_name = county_id_state_map[each_similar["id"]]
                each_similar["state_name"] = state_name

        final_data["safe_counties"] = data

        all_counties = []

        county_id_state_map = {}
        bucket_data = {}
        index = 0
        for each_state in all_states:
            best_counties = list_affordable_counties(each_state)
            each_bucket_ids = []
            for each in best_counties:
                county_id_state_map[each["id"]] = each_state
                all_counties.append(each["id"])
                each_bucket_ids.append(each["id"])

            bucket_data[index] = each_bucket_ids

            index += 1

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(bucket_data, all_counties_str)

        for each_data in data:
            county_id = each_data["id"]
            state_name = county_id_state_map[county_id]
            each_data["state_name"] = state_name
            similars = each_data["similars"]
            for each_similar in similars:
                state_name = county_id_state_map[each_similar["id"]]
                each_similar["state_name"] = state_name

        final_data["affordable_counties"] = data

        all_zips = []
        bucket_data = {}
        index = 0
        zip_id_state_map = {}
        for each_state in all_states:
            best_zips = list_best_zips(each_state)
            each_bucket_ids = []
            for each in best_zips:
                zip_id_state_map[each["id"]] = each_state
                all_zips.append(each["id"])
                each_bucket_ids.append(each["id"])
            bucket_data[index] = each_bucket_ids
            index += 1

        all_zips_str = ""

        for each in all_zips:
            all_zips_str = all_zips_str + "'" + str(each) + "',"

        all_zips_str = all_zips_str[:-1]

        data = similar_zips(bucket_data, all_zips_str)

        final_data["best_zips"] = data

        for each_data in data:
            zip_id = each_data["id"]
            state_name = zip_id_state_map[zip_id]
            each_data["state_name"] = state_name
            similars = each_data["similars"]
            for each_similar in similars:
                state_name = zip_id_state_map[each_similar["id"]]
                each_similar["state_name"] = state_name

        return JsonResponse(final_data, safe=False)


@api_view(["GET"])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_all_data(request):
    if request.method == "GET":
        state_name = request.GET.get("state_name", "Arkansas")

        best_counties = list_best_counties(state_name)
        safe_counties = list_safe_counties(state_name)
        affordable_counties = list_affordable_counties(state_name)
        best_zips = list_best_zips(state_name)

        data = {}

        data["best_counties"] = best_counties
        data["safe_counties"] = safe_counties
        data["affordable_counties"] = affordable_counties
        data["best_zips"] = best_zips

        return JsonResponse(data, safe=False)
