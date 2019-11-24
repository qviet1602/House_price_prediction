from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from django.db import connection
from django.http import JsonResponse

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