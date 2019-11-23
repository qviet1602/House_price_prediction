from rest_framework.decorators import api_view
from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from django.db import connection
from django.http import JsonResponse

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_purchase_median_prices(request):
    if request.method == 'GET':
        #Get all states
        states_query = 'select id from state'
        with connection.cursor() as cursor:
            cursor.execute(states_query)
            states_rows = cursor.fetchall()

        data = []
        for each_state in states_rows:
            query = 'select state.name as name, state.state_code as state_code, ' \
                    'list_price from state_median_price inner join state on state_median_price.state_id = state.id ' \
                    'where home_type_id = (select id from home_type where type=%s and feature=%s) and state.id = %s order by state.id asc, state_median_price.created_date desc limit 1'

            with connection.cursor() as cursor:
                cursor.execute(query, ['purchase', 'all', each_state[0]])
                row = cursor.fetchone()

            each_data_dict = {}
            each_data_dict['name'] = row[0]
            each_data_dict['state_code'] = row[1]
            each_data_dict['list_price'] = row[2]

            data.append(each_data_dict)

        return JsonResponse(data, safe=False)

@api_view(['GET'])
@csrf_exempt
@authentication_classes([])
@permission_classes([])
def list_rental_median_prices(request):
    if request.method == 'GET':
        #Get all states
        states_query = 'select id from state'
        with connection.cursor() as cursor:
            cursor.execute(states_query)
            states_rows = cursor.fetchall()

        data = []
        for each_state in states_rows:
            query = 'select state.name as name, state.state_code as state_code, ' \
                    'list_price from state_median_price inner join state on state_median_price.state_id = state.id ' \
                    'where home_type_id = (select id from home_type where type=%s and feature=%s) and state.id = %s order by state.id asc, state_median_price.created_date desc limit 1'

            with connection.cursor() as cursor:
                cursor.execute(query, ['rental', 'all', each_state[0]])
                row = cursor.fetchone()

            if row is not None:
                each_data_dict = {}
                each_data_dict['name'] = row[0]
                each_data_dict['state_code'] = row[1]
                each_data_dict['list_price'] = row[2]

                data.append(each_data_dict)

        return JsonResponse(data, safe=False)
