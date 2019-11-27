from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from django.db import connection
from django.http import JsonResponse
from decimal import Decimal
import numpy as np
import scipy.spatial.distance as dst

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_states(request):
    if request.method == 'GET':
        #Get all states
        states_query = 'select name, state_code, id from state order by name asc'
        with connection.cursor() as cursor:
            cursor.execute(states_query)
            states_rows = cursor.fetchall()

        data = []

        for each_state in states_rows:
            each_data_dict = {}
            each_data_dict['name'] = each_state[0]
            each_data_dict['state_code'] = each_state[1]
            each_data_dict['id'] = each_state[2]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_counties_purchase(request):
    if request.method == 'GET':
        zillow_id_string = "('3101', '139', '1090', '2402', '2841', '1286', '581', '2964', '978', '1347', " \
                           "'2832', '3250', '445', '207', '791', '3136', '1561', '386', '2452', '3175', '1510', '2801', '2046', " \
                           "'3017', '401', '1252', '2993', '2241', '3165', '2614', '1950', '2288', '2339', '1287', '1694', " \
                           "'3159', '2840', '1440', '3130', '281', '2975', '2347', '2804', '1018', '1388', '1020', '3102', '1682', " \
                           "'2694', '2480', '874', '1165', '2337', '489', '3246', '2815', '1155', '204', '2061', '2802', '2314', " \
                           "'3227', '2626', '2322', '1690', '2981', '2879', '1322', '504', '1776', '503', '2742', '2810', '2045', " \
                           "'2463', '2842', '2847', '220', '984', '135', '3134', '330', '1804', '1948', '988', '2889', '2732', " \
                           "'1106', '2441', '2243', '3001', '414', '1689', '80', '757', '201', '285', '3289', '989', '659', '2127', " \
                           "'2251', '1558', '1822', '1556', '1404', '2986', '3152', '771', '2980', '2734', '3069', '2776', '1676', " \
                           "'322', '197', '3033', '911', '1349', '1964', '1611', '2537', '221', '2482', '2063', '1241', '2312', " \
                           "'146', '1396', '2033', '2511', '2465', '669', '1746', '2983', '2934', '2896', '1442', '616', '353', " \
                           "'3286', '343', '2743', '215', '287', '1721', '448', '3229', '3081', '1485', '2444', '1395', '1208', " \
                           "'385', '3247', '3166', '971', '2596', '2507', '2528', '685', '730', '1290', '904', '1201', '3200', " \
                           "'367', '231', '1712', '2897', '1146', '1325', '2869', '1953', '1272', '2323', '1161', '373', '2552', " \
                           "'1916', '1638', '1893', '2912', '3158', '1171', '1887', '2515', '1922', '1771', '470', '823', '1150', " \
                           "'1849', '3112', '2259', '1701', '2877', '3013', '1549', '2616', '2702', '2929', '1101', '1670', '2775', " \
                           "'2911', '1110', '159', '3131', '232', '1057', '2318', '2133', '2987', '3122', '3261', '563', '1900', " \
                           "'1957', '999', '1608', '1300', '2779', '3025', '1196', '2668', '329', '625', '1138', '1509', '562', " \
                           "'1761', '1503', '3173', '2399', '2156', '3061', '2914', '1283', '3225', '2699', '802', '225', '2967', " \
                           "'344', '3254', '418', '2744', '2885', '2188', '1480', '2112', '2583', '3070', '2619', '3219', '3048', " \
                           "'3109', '2086', '2648', '1210', '2526', '2206', '1412', '341', '347', '1348', '1381', '3043', '3128', " \
                           "'2955', '913', '1314', '1092', '905', '1448', '1525', '2959', '2460', '3278', '3146', '2159', '2023', " \
                           "'2141', '1380', '2820', '2249', '3041', '2341', '1191', '2449', '860', '1225', '1186', '2360', '67', " \
                           "'283', '1595', '1837', '202', '2800', '706', '1330', '3123', '395', '2138', '1975', '1407', '1802', " \
                           "'2650', '1133', '1789', '3004', '2714', '2679', '178', '2913', '2569', '1544', '2901', '250', '3137', " \
                           "'1604', '2824', '2054', '3026', '2117', '113', '1413', '3059', '251', '1607', '2799', '1176', '2695', " \
                           "'2722', '1951', '2527', '2495', '1351', '938', '78', '1782', '1821', '2368', '701', '446', '3074', " \
                           "'3168', '1218', '3164', '1703', '2923', '255', '2207', '1289', '1854', '3077', '1901', '1634', '2628', " \
                           "'1819', '711', '2556', '2729', '3071', '335', '1500', '2506', '2851', '884', '3072', '794', '2364', " \
                           "'1972', '394', '2097', '2247', '1548', '1393', '940', '238', '1203', '1835', '2767', '797', '1496', " \
                           "'2371', '1474', '422', '2370', '1513', '620', '2855', '2434', '1478', '323', '2905', '68', '493', " \
                           "'3151', '1678', '1253', '2640', '2719', '371', '1657', '3132', '2892', '2872', '641', '1644', '2592', " \
                           "'2624', '429', '855', '1856', '1758', '1343', '2724', '1261', '2924', '3290', '2174', '1652', '512', " \
                           "'1718', '1707', '3260', '1409', '1033', '2405', '3044', '1998', '2386', '924', '2168', '1376', '735', " \
                           "'2299', '1326', '1729', '2235', '485', '1581', '1142', '649', '1961', '2812', '870', '3126', '1929', " \
                           "'2163', '1945', '1100', '2865', '2783', '2157', '525', '1112', '2733', '2659', '2766', '2195', '158', " \
                           "'3084', '2860', '137', '3237', '3243', '1628', '1755', '514', '1338', '737', '1251', '1214', '1619', '2281', " \
                           "'1566', '531', '1976', '1751', '1233', '1063', '1538', '3015', '356', '2942', '3093', '2179', '976', '1479', '345', " \
                           "'2261', '841', '304', '2554', '2891', '1605', '1859', '3258', '1745', '2201', '314', '2525', '1279', '2928', '1539', " \
                           "'2070', '3076', '382', '1769', '3147', '173', '2871', '86', '1305', '923', '1768', '2218', '1374', '393', '2300', '2915', " \
                           "'2894', '2479', '1044', '1468', '3075', '392', '259', '1519', '947', '2074', '773', '1313', '491', '741', '2880', '2753', " \
                           "'2369', '543', '2073', '1068', '2244', '1559', '1668', '205', '1387', '1151', '1944', '1598', '3118', '2293', '2818', '3024', " \
                           "'2772', '2408', '1471', '1562', '1880', '2134', '851', '611', '2643', '1537', '2548', '1430', '2098', '262', '1384', '3089', " \
                           "'909', '152', '2566', '2343', '3288', '1926', '1025', '1798', '1385', '2022', '3038', '1301', '468', '885', '1202', '234', " \
                           "'2170', '2920', '1806', '2990', '211', '505', '1093', '2185', '2245', '2956', '2208', '783', '2199', '2972', '1341', '1111', " \
                           "'593', '1621', '546', '1508', '1189', '2348', '1405', '824', '1284', '3218', '896', '1659', '2038', '1117', '1163', '2091', " \
                           "'3197', '141', '2084', '501', '2922', '733', '658', '1127', '2295', '1720', '2755', '827', '224', '1884', '628', '635', '149', " \
                           "'1076', '1246', '2653', '568', '1725', '2481', '703', '2838', '3283', '891', '729', '1297', '190', '833', '2677', '2071', " \
                           "'699', '3162', '466', '2936', '2390', '782', '878', '745', '1179', '2365', '3086', '1329', '778', '2932', '430', '1606', " \
                           "'873', '2362', '1324', '2681', '1368', '487', '480', '692', '269', '528', '3282', '253', '3279', '107', '950', '3274', " \
                           "'1963', '1067', '3272', '2803', '2813', '743', '1454', '3022')"
        counties_query = "select distinct county_id from county_timeseries where zillow_id in " + zillow_id_string + " and index_value is not null and (year_month like '%-12' or year_month = '2019-09')"
        #counties_query = "select distinct county_id from county_timeseries where index_value is not null and (year_month like '%-12' or year_month = '2019-09') and home_type_id in (1, 2, 3, 4, 5, 6, 9)"
        with connection.cursor() as cursor:
            cursor.execute(counties_query)
            county_rows = cursor.fetchall()

        county_ids = []
        for each_county_row in county_rows:
            county_ids.append(each_county_row[0])


        county_id_string = ""
        for each_county_id in county_ids:
            county_id_string += "'" + str(each_county_id) + "',"

        county_id_string = county_id_string[:-1]

        county_info_query = 'select county.id, county.name, state.name from county inner join state on county.state_id = state.id where county.id in (' + county_id_string + ')'
        with connection.cursor() as cursor:
            cursor.execute(county_info_query)
            county_data_rows = cursor.fetchall()

        data = []
        for each_county in county_data_rows:
            each_data_dict = {}
            each_data_dict['name'] = each_county[1] + " (" + each_county[2] + ")"
            each_data_dict['id'] = each_county[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_counties_rental(request):
    if request.method == 'GET':
        counties_query = "select distinct county_id from county_median_price where list_price is not null and (year_month like '%-12' or year_month = '2019-09') and home_type_id in (11, 12, 13, 14, 15, 16, 9)"
        with connection.cursor() as cursor:
            cursor.execute(counties_query)
            county_rows = cursor.fetchall()

        county_ids = []
        for each_county_row in county_rows:
            county_ids.append(each_county_row[0])


        county_id_string = ""
        for each_county_id in county_ids:
            county_id_string += "'" + str(each_county_id) + "',"

        county_id_string = county_id_string[:-1]

        county_info_query = 'select county.id, county.name, state.name from county inner join state on county.state_id = state.id where county.id in (' + county_id_string + ')'
        with connection.cursor() as cursor:
            cursor.execute(county_info_query)
            county_data_rows = cursor.fetchall()

        data = []
        for each_county in county_data_rows:
            each_data_dict = {}
            each_data_dict['name'] = each_county[1] + " (" + each_county[2] + ")"
            each_data_dict['id'] = each_county[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_zips_purchase(request):
    if request.method == 'GET':
        #zip_query = "select distinct zipcode_id from zip_timeseries where index_value is not null and (year_month like '%-12' or year_month = '2019-09') and home_type_id in (1, 2, 3, 4, 5, 6, 9)"
        home_type_ids = [1, 2, 3, 4, 5, 6, 9]
        zipcodes = []
        for home_type_id in home_type_ids:
            zipcode_ids = set()
            zip_query = "select zipcode_id from zip_timeseries where (year_month like %s or year_month = %s) and index_value is not null and home_type_id = %s group by zipcode_id having count(index_value) > %s"
            with connection.cursor() as cursor:
                cursor.execute(zip_query, ['201%-12', '2019-09', home_type_id, 9])
                zip_rows = cursor.fetchall()

            for zip_row in zip_rows:
                zipcode_ids.add(zip_row[0])

            zipcodes.append(zipcode_ids)

        zipcode_set1 = zipcodes[0]
        zipcode_set2 = zipcodes[1]
        zipcode_set3 = zipcodes[2]
        zipcode_set4 = zipcodes[3]
        zipcode_set5 = zipcodes[4]
        zipcode_set6 = zipcodes[5]
        zipcode_set7 = zipcodes[6]

        set12 = zipcode_set1.intersection(zipcode_set2)

        set123 = set12.intersection(zipcode_set3)

        set1234 = set123.intersection(zipcode_set4)

        set12345 = set1234.intersection(zipcode_set5)

        set123456 = set12345.intersection(zipcode_set6)

        set123457 = set123456.intersection(zipcode_set7)


        zip_id_string = ""
        for each_zip_id in set123457:
            zip_id_string += "'" + str(each_zip_id) + "',"

        zip_id_string = zip_id_string[:-1]

        zip_info_query = 'select zipcode.id, zipcode.zip_code, state.name from zipcode inner join state on zipcode.state_id = state.id where zipcode.id in (' + zip_id_string + ') order by state.name asc, zipcode.zip_code asc'
        with connection.cursor() as cursor:
            cursor.execute(zip_info_query)
            zip_data_rows = cursor.fetchall()

        data = []
        for each_zip in zip_data_rows:
            each_data_dict = {}
            each_data_dict['name'] = each_zip[1] + " (" + each_zip[2] + ")"
            each_data_dict['id'] = each_zip[0]
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_state_data_purchase(request):
    if request.method == 'GET':
        state_id = request.GET.get('state_id', 23)
        all_years_query = "select distinct(substr(year_month, 1, 4)) from state_timeseries where state_id = %s order by substr(year_month, 1, 4)"
        with connection.cursor() as cursor:
            cursor.execute(all_years_query, [state_id])
            years_rows = cursor.fetchall()

        last_year_month_query = "select year_month from state_timeseries where state_id = %s and year_month like %s order by year_month desc limit 1"

        with connection.cursor() as cursor:
            cursor.execute(last_year_month_query, [state_id, '2019%'])
            last_year_row = cursor.fetchone()

        all_last_year_months = []

        for each_year_row in years_rows:
            all_last_year_months.append(each_year_row[0] + "-12")

        all_last_year_months.append(last_year_row[0])

        all_last_year_months_str = ""

        for each in all_last_year_months:
            all_last_year_months_str = all_last_year_months_str + "'" + each + "',"

        all_last_year_months_str = all_last_year_months_str[:-1]

        home_types = ["condoCoOp", "oneBedroom", "twoBedroom", "threeBedroom", "fourBedroom", "fivePlusBedroom", "singleFamilyHome"]
        data = []
        for each_home_type in home_types:
            each_data_dict = {}
            query = 'select index_value, year_month ' \
                    'from state_timeseries inner join state on state_timeseries.state_id = state.id ' \
                    'where home_type_id = (select id from home_type where type=%s and feature=%s) ' \
                    'and state.id = %s and year_month in (' + all_last_year_months_str + ")"

            with connection.cursor() as cursor:
                cursor.execute(query, ['purchase', each_home_type, state_id])
                home_data_rows = cursor.fetchall()

            home_data = []
            for each_home_data_row in home_data_rows:
                each_home_data_dict = {}
                each_home_data_dict['list_price'] = each_home_data_row[0]
                each_home_data_dict['year'] = int(each_home_data_row[1][0:4])
                home_data.append(each_home_data_dict)

            each_data_dict[each_home_type] = home_data
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_state_data_rental(request):
    if request.method == 'GET':
        state_id = request.GET.get('state_id', 23)
        all_years_query = "select distinct(substr(year_month, 1, 4)) from state_median_price where state_id = %s order by substr(year_month, 1, 4)"
        with connection.cursor() as cursor:
            cursor.execute(all_years_query, [state_id])
            years_rows = cursor.fetchall()

        last_year_month_query = "select year_month from state_median_price where state_id = %s and year_month like %s order by year_month desc limit 1"

        with connection.cursor() as cursor:
            cursor.execute(last_year_month_query, [state_id, '2019%'])
            last_year_row = cursor.fetchone()

        all_last_year_months = []

        for each_year_row in years_rows:
            all_last_year_months.append(each_year_row[0] + "-12")

        all_last_year_months.append(last_year_row[0])

        all_last_year_months_str = ""

        for each in all_last_year_months:
            all_last_year_months_str = all_last_year_months_str + "'" + each + "',"

        all_last_year_months_str = all_last_year_months_str[:-1]

        home_types = ["condoCoOp", "oneBedroom", "twoBedroom", "threeBedroom", "fourBedroom", "fivePlusBedroom", "singleFamilyResidenceRental"]
        data = []
        for each_home_type in home_types:
            each_data_dict = {}
            query = 'select list_price, year_month ' \
                    'from state_median_price inner join state on state_median_price.state_id = state.id ' \
                    'where home_type_id = (select id from home_type where type=%s and feature=%s) ' \
                    'and state.id = %s and year_month in (' + all_last_year_months_str + ") and list_price is not null"

            with connection.cursor() as cursor:
                cursor.execute(query, ['rental', each_home_type, state_id])
                home_data_rows = cursor.fetchall()

            home_data = []
            for each_home_data_row in home_data_rows:
                each_home_data_dict = {}
                each_home_data_dict['list_price'] = each_home_data_row[0]
                each_home_data_dict['year'] = int(each_home_data_row[1][0:4])
                home_data.append(each_home_data_dict)

            each_data_dict[each_home_type] = home_data
            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_county_data_purchase(request):
    if request.method == 'GET':
        county_id = request.GET.get('county_id', 1)

        home_types = ["condoCoOp", "oneBedroom", "twoBedroom", "threeBedroom", "fourBedroom", "fivePlusBedroom",
                      "singleFamilyHome"]
        data = []
        for each_home_type in home_types:
            last_year_query = "select year_month, index_value from county_timeseries where county_id = %s " \
                              "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id " \
                              "in (select id from home_type where type=%s and feature=%s) order by year_month desc"

            with connection.cursor() as cursor:
                cursor.execute(last_year_query, [county_id, '%-12', '2019-09', 'purchase', each_home_type])
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict['list_price'] = each_row[1]
                each_data_dict['year'] =  each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_county_data_rental(request):
    if request.method == 'GET':
        county_id = request.GET.get('county_id', 1)

        home_types = ["condoCoOp", "oneBedroom", "twoBedroom", "threeBedroom", "fourBedroom", "fivePlusBedroom",
                      "singleFamilyResidenceRental"]
        data = []
        for each_home_type in home_types:
            last_year_query = "select year_month, list_price from county_median_price where county_id = %s " \
                              "and (year_month like %s or year_month = %s) and  list_price is not null and home_type_id " \
                              "in (select id from home_type where type=%s and feature=%s) order by year_month desc"

            with connection.cursor() as cursor:
                cursor.execute(last_year_query, [county_id, '%-12', '2019-09', 'rental', each_home_type])
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict['list_price'] = each_row[1]
                each_data_dict['year'] =  each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_zip_data_purchase(request):
    if request.method == 'GET':
        county_id = request.GET.get('zipcode_id', 14101)

        home_types = ["condoCoOp", "oneBedroom", "twoBedroom", "threeBedroom", "fourBedroom", "fivePlusBedroom",
                      "singleFamilyHome"]
        data = []
        for each_home_type in home_types:
            last_year_query = "select year_month, index_value from zip_timeseries where zipcode_id = %s " \
                              "and (year_month like %s or year_month = %s) and  index_value is not null and home_type_id " \
                              "in (select id from home_type where type=%s and feature=%s) order by year_month desc"

            with connection.cursor() as cursor:
                cursor.execute(last_year_query, [county_id, '201%-12', '2019-09', 'purchase', each_home_type])
                last_year_rows = cursor.fetchall()
            last_year_data = []

            for each_row in last_year_rows:
                each_data_dict = {}
                each_data_dict['list_price'] = each_row[1]
                each_data_dict['year'] =  each_row[0][0:4]
                last_year_data.append(each_data_dict)

            home_data_dict = {}
            home_data_dict[each_home_type] = last_year_data
            data.append(home_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_node_stats(request):
    if request.method == 'GET':
        node_data = request.GET.get('node_data', 'state_Alabama')
        node_type, node_id = node_data.split("_")
        statistics = {}
        if node_type == 'state':
            state_query = "select id from state where name = %s"
            with connection.cursor() as cursor:
                cursor.execute(state_query, [node_id])
                state_row = cursor.fetchone()

            node_id = state_row[0]

            crime_data_query = "select avg(violent_crime), avg(property_crime) from crime_data where zipcode_id " \
                               "in (select id from zipcode where zipcode.state_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            statistics['violent_crime'] = round(violent_crime, 2)
            statistics['property_crime'] = round(property_crime, 2)

            schools_query = "select count(*) from school_data where schooldigger_rating is not null " \
                            "and schooldigger_rating >= 3 and zipcode_id in (select id from zipcode where state_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics['num_of_schools'] = num_of_schools

            annual_income_query = "select avg(avg_annual_income), avg(median_annual_income) from annual_income where zipcode_id " \
                                  "in (select id from zipcode where state_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]
            statistics['avg_avg_annual_income'] = round(avg_avg_annual_income, 2)
            statistics['avg_median_annual_income'] = round(avg_median_annual_income, 2)

            us_avg = Decimal(28555.0)

            avg_diff = avg_avg_annual_income - us_avg
            is_affordable = False
            if avg_diff < 0 or avg_diff < 10000:
                is_affordable = True

            statistics['is_affordable'] = is_affordable

        elif node_type == 'county':
            node_id = int(node_id)
            crime_data_query = "select avg(violent_crime), avg(property_crime) from crime_data where zipcode_id " \
                               "in (select id from zipcode where county_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            statistics['violent_crime'] = round(violent_crime, 2)
            statistics['property_crime'] = round(property_crime, 2)

            schools_query = "select count(*) from school_data where schooldigger_rating is not null " \
                            "and schooldigger_rating >= 3 and zipcode_id in (select id from zipcode where county_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics['num_of_schools'] = num_of_schools

            annual_income_query = "select avg(avg_annual_income), avg(median_annual_income) from annual_income where zipcode_id " \
                                  "in (select id from zipcode where county_id = %s)"

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]
            statistics['avg_avg_annual_income'] = round(avg_avg_annual_income, 2)
            statistics['avg_median_annual_income'] = round(avg_median_annual_income, 2)

            us_avg = Decimal(28555.0)

            avg_diff = avg_avg_annual_income - us_avg
            is_affordable = False
            if avg_diff < 0 or avg_diff < 10000:
                is_affordable = True

            statistics['is_affordable'] = is_affordable

        elif node_type == 'zipcode':
            node_id = int(node_id)
            print("Zipcode Id ", node_id)
            crime_data_query = "select violent_crime, property_crime from crime_data where zipcode_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(crime_data_query, [node_id])
                crime_data_row = cursor.fetchone()

            violent_crime = crime_data_row[0]
            property_crime = crime_data_row[1]

            statistics['violent_crime'] = round(violent_crime, 2)
            statistics['property_crime'] = round(property_crime, 2)

            schools_query = "select count(*) from school_data where schooldigger_rating is not null " \
                            "and schooldigger_rating >= 3 and zipcode_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(schools_query, [node_id])
                school_data_row = cursor.fetchone()

            num_of_schools = school_data_row[0]
            statistics['num_of_schools'] = num_of_schools

            annual_income_query = "select avg_annual_income, median_annual_income from annual_income where zipcode_id = %s"

            with connection.cursor() as cursor:
                cursor.execute(annual_income_query, [node_id])
                annual_income_data_row = cursor.fetchone()

            avg_avg_annual_income = annual_income_data_row[0]
            avg_median_annual_income = annual_income_data_row[1]
            statistics['avg_avg_annual_income'] = round(avg_avg_annual_income, 2)
            statistics['avg_median_annual_income'] = round(avg_median_annual_income, 2)

            us_avg = Decimal(28555.0)

            avg_diff = avg_avg_annual_income - us_avg
            is_affordable = False
            if avg_diff < 0 or avg_diff < 10000:
                is_affordable = True

            statistics['is_affordable'] = is_affordable

        return JsonResponse(statistics, safe=False)

def list_best_counties(state_name):
    # Find counties with least crime rate
    final_county_ids = set()
    limit = 40

    total_ids = 0
    iteration = 0
    while total_ids < 5:
        iteration += 1
        crime_data_query = "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from " \
                           "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                           "inner join county on zipcode.county_id = county.id " \
                           "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                           "group by county.name, zipcode.county_id " \
                           "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc limit %s"
        with connection.cursor() as cursor:
            cursor.execute(crime_data_query, [state_name, limit])
            crime_data_row = cursor.fetchall()

        county_ids1 = []
        for each_row in crime_data_row:
            county_ids1.append(each_row[2])

        school_data_row = "select count(*), zipcode.county_id, county.name from school_data " \
                          "inner join zipcode on school_data.zipcode_id = zipcode.id " \
                          "inner join county on zipcode.county_id = county.id " \
                          "inner join state on zipcode.state_id = state.id " \
                          "where state.name = %s and schooldigger_rating is not null " \
                          "and schooldigger_rating > %s group by county.name, zipcode.county_id order by count(*) desc limit %s"

        with connection.cursor() as cursor:
            cursor.execute(school_data_row, [state_name, 2, limit])
            school_data_row = cursor.fetchall()

        county_ids2 = []

        for each_row in school_data_row:
            county_ids2.append(each_row[1])

        annual_income_query = "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from " \
                              "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                              "inner join county on zipcode.county_id = county.id " \
                              "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                              "group by county.name, zipcode.county_id " \
                              "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc limit %s"
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

        print("Len ", len(final_list))
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
        each_data_dict['id'] = each_row[0]
        each_data_dict['name'] = each_row[1][:-6]
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
        crime_data_query = "select violent_crime, property_crime, zipcode_id, zipcode.zip_code from " \
                           "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                           "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                           "order by crime_data.violent_crime asc, crime_data.property_crime asc limit %s"
        with connection.cursor() as cursor:
            cursor.execute(crime_data_query, [state_name, limit])
            crime_data_row = cursor.fetchall()

        zipcode_ids1 = []
        for each_row in crime_data_row:
            zipcode_ids1.append(each_row[2])

        school_data_row = "select count(*), zipcode_id, zipcode.zip_code from school_data " \
                          "inner join zipcode on school_data.zipcode_id = zipcode.id " \
                          "inner join state on zipcode.state_id = state.id " \
                          "where state.name = %s and schooldigger_rating is not null " \
                          "and schooldigger_rating > %s group by zipcode_id, zipcode.zip_code order by count(*) desc limit %s"

        with connection.cursor() as cursor:
            cursor.execute(school_data_row, [state_name, 2, limit])
            school_data_row = cursor.fetchall()

        zipcode_ids2 = []

        for each_row in school_data_row:
            zipcode_ids2.append(each_row[1])

        annual_income_query = "select avg_annual_income, median_annual_income, zipcode_id, zipcode.zip_code from " \
                              "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                              "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                              "order by annual_income.avg_annual_income asc, annual_income.median_annual_income asc limit %s"
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
        each_data_dict['id'] = each_row[0]
        each_data_dict['name'] = each_row[1]
        data.append(each_data_dict)

    data = data[0:5]

    return data

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_best_counties(request):
    if request.method == 'GET':
        state_name = request.GET.get('state_name', 'Alabama')
        data = list_best_counties(state_name)

        return JsonResponse(data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_best_zips(request):
    if request.method == 'GET':
        state_name = request.GET.get('state_name', 'Alabama')

        data = list_best_zips(state_name)

        return JsonResponse(data, safe=False)


def list_safe_counties(state_name):
    crime_data_query = "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from " \
                       "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                       "inner join county on zipcode.county_id = county.id " \
                       "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                       "group by county.name, zipcode.county_id " \
                       "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc limit %s"
    with connection.cursor() as cursor:
        cursor.execute(crime_data_query, [state_name, 5])
        crime_data_row = cursor.fetchall()

    data = []

    for each_row in crime_data_row:
        each_data_dict = {}
        each_data_dict['id'] = each_row[2]
        each_data_dict['name'] = each_row[3]
        data.append(each_data_dict)

    return data

def list_affordable_counties(state_name):
    annual_income_query = "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from " \
                          "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                          "inner join county on zipcode.county_id = county.id " \
                          "inner join state on zipcode.state_id = state.id where state.name = %s  " \
                          "group by county.name, zipcode.county_id having avg(avg_annual_income) <= %s" \
                          "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc limit %s"
    with connection.cursor() as cursor:
        cursor.execute(annual_income_query, [state_name, 38555, 5])
        annual_data_row = cursor.fetchall()

    data = []

    for each_row in annual_data_row:
        each_data_dict = {}
        each_data_dict['id'] = each_row[2]
        each_data_dict['name'] = each_row[3]
        data.append(each_data_dict)

    return data

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_safe_counties(request):
    if request.method == 'GET':
        state_name = request.GET.get('state_name', 'Alabama')

        data = list_safe_counties(state_name)

        return JsonResponse(data, safe=False)

def get_affordable_counties(request):
    if request.method == 'GET':
        state_name = request.GET.get('state_name', 'Alabama')

        data = list_affordable_counties(state_name)

        return JsonResponse(data, safe=False)

def get_similar_states(request):
    if request.method == 'GET':
        selected_state = request.GET.get('state_name', 'Alabama')

        #Get data for all three states and aggregate this data into one dataset
        crime_data_query = "select avg(violent_crime), avg(property_crime), zipcode.state_id, state.name from " \
                           "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                           "inner join state on zipcode.state_id = state.id  " \
                           "group by state.name, zipcode.state_id " \
                           "order by avg(crime_data.violent_crime) asc, avg(crime_data.property_crime) asc"

        school_data_query = "select count(*), zipcode.state_id, state.name from school_data " \
                          "inner join zipcode on school_data.zipcode_id = zipcode.id " \
                          "inner join state on zipcode.state_id = state.id " \
                          "where schooldigger_rating is not null " \
                          "and schooldigger_rating > %s group by state.name, zipcode.state_id order by count(*) desc"

        annual_income_query = "select avg(avg_annual_income), avg(median_annual_income), zipcode.state_id, state.name from " \
                              "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                              "inner join state on zipcode.state_id = state.id " \
                              "group by state.name, zipcode.state_id " \
                              "order by avg(annual_income.avg_annual_income) asc, avg(annual_income.median_annual_income) asc"
        median_prices_query = "select list_price, state_id, state.name from state_median_price " \
                              "inner join state on state_median_price.state_id = state.id where year_month = %s and home_type_id = %s"

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
            cursor.execute(median_prices_query, ['2019-09', 10])
            median_prices_rows = cursor.fetchall()

        #Now merge all this data into one

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
            crime_data = crime_data_map_by_state[each_key]
            school_data = school_data_map_by_state[each_key]
            annual_data = annual_data_map_by_state[each_key]
            median_price = median_price_map_by_state[each_key]

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

        similarity_values = dst.squareform(dst.pdist(numpy_dataset, 'euclidean'))

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

        states_query = "select id, state_code, name from state where name in (%s, %s, %s)"
        with connection.cursor() as cursor:
            cursor.execute(states_query, similar_states)
            state_rows = cursor.fetchall()

        data = []

        for each_row in state_rows:
            each_data_dict = {}
            each_data_dict['name'] = each_row[2]
            each_data_dict['state_code'] = each_row[1]
            each_data_dict['id'] = each_row[0]

            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

def similar_counties(all_counties_str, counties_list):

    # Get data for all best counties and aggregate this data into one dataset
    crime_data_query = "select avg(violent_crime), avg(property_crime), zipcode.county_id, county.name from " \
                       "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                       "inner join county on zipcode.county_id = county.id where zipcode.county_id in (" + all_counties_str + ") " \
                       "group by county.name, zipcode.county_id "

    school_data_query = "select count(*), zipcode.county_id, county.name from school_data " \
                        "inner join zipcode on school_data.zipcode_id = zipcode.id " \
                        "inner join county on zipcode.county_id = county.id where zipcode.county_id in (" + all_counties_str + ") " \
                        "and schooldigger_rating is not null " \
                        "and schooldigger_rating > 2 group by county.name, zipcode.county_id"

    annual_income_query = "select avg(avg_annual_income), avg(median_annual_income), zipcode.county_id, county.name from " \
                          "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                          "inner join county on zipcode.county_id = county.id where zipcode.county_id in (" + all_counties_str + ") " \
                          "group by county.name, zipcode.county_id"

    median_prices_query = "select list_price, county_id, county.name from county_median_price " \
                          "inner join county on county_median_price.county_id = county.id where year_month = '2019-09' " \
                          "and home_type_id = 10 and county.id in (" + all_counties_str + ")"


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

    crime_data_map = {}

    for each_row in crime_data_rows:
        crime_data_map[each_row[3]] = each_row

    school_data_map = {}

    for each_row in school_data_rows:
        school_data_map[each_row[2]] = each_row

    annual_data_map = {}

    for each_row in annual_data_rows:
        annual_data_map[each_row[3]] = each_row

    median_data_map = {}

    for each_row in median_price_rows:
        median_data_map[each_row[2]] = each_row


    min_keys_length = len(crime_data_rows)
    keys = crime_data_map.keys()
    if len(school_data_rows) < min_keys_length:
        min_keys_length = len(school_data_rows)
        keys = school_data_map.keys()
    if len(annual_data_rows) < min_keys_length:
        min_keys_length = len(annual_data_rows)
        keys = annual_data_map.keys()
    if len(median_price_rows) < min_keys_length:
        keys = median_data_map.keys()

    full_dataset = []
    idx = 0
    entities = {}
    entities_map = {}
    for each_key in keys:
        each_data_instance = []
        crime_data = crime_data_map.get(each_key, None)
        school_data = school_data_map.get(each_key, None)
        annual_data = annual_data_map.get(each_key, None)
        median_data = median_data_map.get(each_key, None)

        if crime_data is None or school_data is None or annual_data is None or median_data is None:
            continue

        each_data_instance.append(crime_data[0])
        each_data_instance.append(crime_data[1])
        each_data_instance.append(school_data[0])
        each_data_instance.append(annual_data[0])
        each_data_instance.append(annual_data[1])
        each_data_instance.append(median_data[0])
        entities[idx] = each_key
        entities_map[each_key] = crime_data[2]
        idx += 1
        full_dataset.append(each_data_instance)

    numpy_dataset = np.array(full_dataset, dtype=np.float)

    similarity_values = dst.squareform(dst.pdist(numpy_dataset, 'euclidean'))

    rows = similarity_values.shape[0]
    cols = similarity_values.shape[1]
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

    main_similarities = []
    count_down = 3
    for each_row_idx in range(len(all_idx_similarity_data)):
        each_col = all_idx_similarity_data[each_row_idx]
        similarites = []
        for col_idx in range(len(each_col)):
            if each_row_idx < int(rows/3):
                if each_col[col_idx] < int(rows/3):
                    continue
                elif each_col[col_idx] >= int(rows/3):
                    similarites.append(each_col[col_idx])
            elif each_row_idx < 10:
                if each_col[col_idx] < 2 * int(rows/3):
                    continue
                elif each_col[col_idx] >= 2 * int(rows/3):
                    similarites.append(each_col[col_idx])

        if len(similarites) != 0:
            if each_row_idx % int(rows/3) == 0:
                count_down -= 1
            if len(similarites[0:count_down]) != 0:
                main_similarities.append(similarites[0:count_down])

    data = []
    for each_row in range(len(main_similarities)):
        each_data_dict = {}
        each_data_dict['name'] = entities[each_row]
        each_data_dict['id'] = entities_map[each_data_dict['name']]
        similars = main_similarities[each_row]

        similar_values = []
        for similar in similars:
            similar_data_dict = {}
            similar_data_dict['name'] = entities[similar]
            similar_data_dict['id'] = entities_map[each_data_dict['name']]
            similar_values.append(similar_data_dict)

        each_data_dict['similars'] = similar_values
        data.append(each_data_dict)

    return data

def similar_zips(all_zips_str):

    # Get data for all best zipcodes and aggregate this data into one dataset
    crime_data_query = "select violent_crime, property_crime, zipcode.id, zipcode.zip_code from " \
                       "crime_data inner join zipcode on crime_data.zipcode_id = zipcode.id " \
                       "where zipcode.id in (" + all_zips_str + ")"

    school_data_query = "select count(*), zipcode.id, zipcode.zip_code from school_data " \
                        "inner join zipcode on school_data.zipcode_id = zipcode.id " \
                        "where zipcode.id in (" + all_zips_str + ") " \
                        "and schooldigger_rating is not null and schooldigger_rating > 2 " \
                        "group by zipcode.id, zipcode.zip_code"


    annual_income_query = "select avg_annual_income, median_annual_income, zipcode.id, zipcode.zip_code from " \
                          "annual_income inner join zipcode on annual_income.zipcode_id = zipcode.id " \
                          "where zipcode.id in (" + all_zips_str + ")"


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
        crime_data_map[each_row[3]] = each_row

    school_data_map = {}

    for each_row in school_data_rows:
        school_data_map[each_row[2]] = each_row

    annual_data_map = {}

    for each_row in annual_data_rows:
        annual_data_map[each_row[3]] = each_row

    min_keys_length = len(crime_data_rows)
    keys = crime_data_map.keys()
    if len(school_data_rows) < min_keys_length:
        min_keys_length = len(school_data_rows)
        keys = school_data_map.keys()
    if len(annual_data_rows) < min_keys_length:
        keys = annual_data_map.keys()

    full_dataset = []
    idx = 0
    entities = {}
    entities_map = {}
    for each_key in keys:
        each_data_instance = []
        crime_data = crime_data_map.get(each_key, None)
        school_data = school_data_map.get(each_key, None)
        annual_data = annual_data_map.get(each_key, None)

        if crime_data is None or school_data is None or annual_data is None:
            continue

        each_data_instance.append(crime_data[0])
        each_data_instance.append(crime_data[1])
        each_data_instance.append(school_data[0])
        each_data_instance.append(annual_data[0])
        each_data_instance.append(annual_data[1])
        #each_data_instance.append(median_data[0])
        entities[idx] = each_key
        entities_map[each_key] = crime_data[2]
        idx += 1
        full_dataset.append(each_data_instance)

    numpy_dataset = np.array(full_dataset, dtype=np.float)

    similarity_values = dst.squareform(dst.pdist(numpy_dataset, 'euclidean'))

    rows = similarity_values.shape[0]
    cols = similarity_values.shape[1]
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

    main_similarities = []
    count_down = 3
    for each_row_idx in range(len(all_idx_similarity_data)):
        each_col = all_idx_similarity_data[each_row_idx]
        similarites = []
        for col_idx in range(len(each_col)):
            if each_row_idx == col_idx:
                continue
            if each_row_idx < 5:
                if each_col[col_idx] < int(rows/3):
                    continue
                elif each_col[col_idx] >= int(rows/3):
                    similarites.append(each_col[col_idx])
            elif each_row_idx < 10:
                if each_col[col_idx] < 2 * int(rows/3):
                    continue
                elif each_col[col_idx] >= 2 * int(rows/3):
                    similarites.append(each_col[col_idx])

        if len(similarites) != 0:
            if each_row_idx % int(rows/3) == 0:
                count_down -= 1
            main_similarities.append(similarites[0:count_down])

    data = []
    for each_row in range(len(main_similarities)):
        each_data_dict = {}
        each_data_dict['name'] = entities[each_row]
        each_data_dict['id'] = entities_map[each_data_dict['name']]
        similars = main_similarities[each_row]

        similar_values = []
        for similar in similars:
            similar_data_dict = {}
            similar_data_dict['name'] = entities[similar]
            similar_data_dict['id'] = entities_map[each_data_dict['name']]
            similar_values.append(similar_data_dict)

        each_data_dict['similars'] = similar_values
        data.append(each_data_dict)

    return data

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_similar_all(request):
    if request.method == 'GET':
        selected_states = request.GET.get('states', 'Arkansas_Ohio_Mississippi')

        all_states = selected_states.split("_")
        best_counties1 = list_best_counties(all_states[0])
        best_counties2 = list_best_counties(all_states[1])
        best_counties3 = list_best_counties(all_states[2])

        all_counties = []

        for each in best_counties1:
            all_counties.append(each['id'])

        for each in best_counties2:
            all_counties.append(each['id'])

        for each in best_counties3:
            all_counties.append(each['id'])

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(all_counties_str, all_counties)

        final_data = dict()
        final_data['best_counties'] = data


        #Safe counties
        safe_counties1 = list_safe_counties(all_states[0])
        safe_counties2 = list_safe_counties(all_states[1])
        safe_counties3 = list_safe_counties(all_states[2])

        print("Len ", len(safe_counties1), len(safe_counties2), len(safe_counties3))

        all_counties = []

        for each in safe_counties1:
            all_counties.append(each['id'])

        for each in safe_counties2:
            all_counties.append(each['id'])

        for each in safe_counties3:
            all_counties.append(each['id'])

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(all_counties_str, all_counties)

        final_data['safe_counties'] = data

        # Affordable counties
        affordable_counties1 = list_affordable_counties(all_states[0])
        affordable_counties2 = list_affordable_counties(all_states[1])
        affordable_counties3 = list_affordable_counties(all_states[2])

        all_counties = []

        for each in affordable_counties1:
            all_counties.append(each['id'])

        for each in affordable_counties2:
            all_counties.append(each['id'])

        for each in affordable_counties3:
            all_counties.append(each['id'])

        all_counties_str = ""

        for each in all_counties:
            all_counties_str = all_counties_str + "'" + str(each) + "',"

        all_counties_str = all_counties_str[:-1]

        data = similar_counties(all_counties_str, all_counties)

        final_data['affordable_counties'] = data


        # best zips
        best_zips1 = list_best_zips(all_states[0])
        best_zips2 = list_best_zips(all_states[1])
        best_zips3 = list_best_zips(all_states[2])

        all_zips = []

        for each in best_zips1:
            all_zips.append(each['id'])

        for each in best_zips2:
            all_zips.append(each['id'])

        for each in best_zips3:
            all_zips.append(each['id'])

        all_zips_str = ""

        for each in all_zips:
            all_zips_str = all_zips_str + "'" + str(each) + "',"

        all_zips_str = all_zips_str[:-1]

        print("Zip IDs ", all_zips_str)
        data = similar_zips(all_zips_str)

        final_data['best_zips'] = data

        return JsonResponse(final_data, safe=False)


@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def get_all_data(request):
    if request.method == 'GET':
        state_name = request.GET.get('state', 'Arkansas')

        best_counties = list_best_counties(state_name)
        safe_counties = list_safe_counties(state_name)
        affordable_counties = list_affordable_counties(state_name)
        best_zips = list_best_zips(state_name)

        data = {}

        data['best_counties'] = best_counties
        data['safe_counties'] = safe_counties
        data['affordable_counties'] = affordable_counties
        data['best_zips'] = best_zips

        return JsonResponse(data, safe=False)
