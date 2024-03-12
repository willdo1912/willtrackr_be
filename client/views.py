import requests
import json
import os
from dotenv import load_dotenv
from bson import json_util
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from django.utils.datastructures import MultiValueDictKeyError
from .serializers import (
    CustomerSerializer,
    DailyFormResponseSerializer,
    QuoteSerializer,
    TypeformResponseSerializer,
)
from .models import (
    DailyFormResponse,
    Quote,
    Customer,
    TypeformResponse,
    typeform_answer_collection,
    daily_form_answer_collecton,
    boots_perfume_product_collection,
)

from .misc.sort_field_data_label import *
from .misc.group_and_count_field import *
from .misc.mongo_aggregation import *
from .misc.filter_field_data_type import *

load_dotenv()


# Create your views here.
class QuoteView(viewsets.ModelViewSet):
    serializer_class = QuoteSerializer
    queryset = Quote.objects.all()


class CustomerView(viewsets.ModelViewSet):
    serializer_class = CustomerSerializer
    queryset = Customer.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        name="Check for login credential",
        url_path="login",
    )
    def login(self, request, *args, **kwargs):
        email = request.data["email"]
        password = request.data["password"]
        try:
            serializer = CustomerSerializer(
                instance=get_object_or_404(Customer, email=email, password=password)
            )
            return Response(data=serializer.data, status=200)
        except:
            return Response(data={"msg": "Wrong email or password."}, status=404)

    @action(
        detail=False,
        methods=["POST"],
        name="Check for register credential",
        url_path="register",
    )
    def register(self, request, *args, **kwargs):
        new_serializer = CustomerSerializer(data=request.data)
        try:
            get_object_or_404(Customer, new_serializer.data["email"])
            return Response(data={"msg": "Email already existed."}, status=404)
        except:
            if new_serializer.is_valid():
                new_serializer.save()
                return Response(data=new_serializer.data, status=200)


class TypeformResponseView(viewsets.ModelViewSet):
    serializer_class = TypeformResponseSerializer
    queryset = TypeformResponse.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        name="Add response",
        url_path="response",
    )
    def add_response(self, request, *args, **kwargs):
        typeform_access_key = os.getenv("TYPEFORM_ACCESS_KEY")
        serializer = TypeformResponseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            path = f"https://api.typeform.com/forms/{request.data['form_id']}/responses?included_response_ids={request.data['response_id']}"
            typeform_answer = requests.get(
                path,
                headers={"Authorization": f"Bearer {typeform_access_key}"},
            ).json()
            typeform_answer_collection.insert_one(
                {
                    "_id": request.data["response_id"],
                    "item": typeform_answer["items"][0],
                }
            )
            return Response({"msg": "Succeeded"}, status=200)
        return Response({"msg": serializer.is_valid()}, status=400)


class DailyFormResponseView(viewsets.ModelViewSet):
    serializer_class = DailyFormResponseSerializer
    queryset = DailyFormResponse.objects.all()

    @action(
        detail=False,
        methods=["POST"],
        name="Add daily form attempt",
        url_path="answer",
    )
    def add_daily_form(self, request, *args, **kwargs):
        serializer = DailyFormResponseSerializer(data=request.data)
        if serializer.is_valid():
            daily_form = serializer.save()
            daily_form_answer_collecton.insert_one(
                {
                    "_id": str(daily_form.id),
                    "item": request.data["item"],
                }
            )
            return Response(serializer.data)
        return Response({"msg": "Error"}, status=400)

    @action(
        detail=False,
        methods=["GET"],
        name="Get daily form answers",
        url_path="answer/(?P<answer_id>[^/.]+)",
    )
    def get_daily_form(self, request, answer_id, *args, **kwargs):
        answer = daily_form_answer_collecton.find_one({"_id": answer_id})
        return Response(json.loads(json_util.dumps(answer)))

    @action(
        detail=False,
        methods=["GET"],
        name="Latest daily form attempt",
        url_path="(?P<customer_id>[^/.]+)/latest",
    )
    def get_latest(self, request, customer_id, *args, **kwargs):
        queryset = DailyFormResponse.objects.filter(customer_id=customer_id).latest(
            "start_at"
        )
        return Response({"today": queryset.completed_today()})

    @action(
        detail=False,
        methods=["GET"],
        name="All daily form attempts",
        url_path="(?P<customer_id>[^/.]+)",
    )
    def get_all_responses(self, request, customer_id, *args, **kwargs):
        queryset = DailyFormResponse.objects.filter(customer_id=customer_id)
        serializer = DailyFormResponseSerializer(queryset, many=True)
        latest_queryset = DailyFormResponse.objects.filter(
            customer_id=customer_id
        ).latest("start_at")
        return Response(
            {
                "attempts": serializer.data,
                "completed_today": latest_queryset.completed_today(),
            }
        )


class BootsPerfumeProductView(viewsets.ModelViewSet):
    @action(
        detail=False,
        methods=["GET"],
        name="Get all product filters",
        url_path="count/all",
    )
    def group_and_count_all(self, request, *args, **kwargs):
        result_dict = count_product_each_filter()
        return Response(result_dict, status=200)

    @action(
        detail=False,
        methods=["GET"],
        name="Get products based on filter",
        url_path="product",
    )
    def get_products(self, request, *args, **kwargs):
        # Get all query non-filter params
        search_substring = get_query_param_without_error(request, "search", "")
        current_page = get_query_param_without_error(request, "page", 1)
        price_min = get_query_param_without_error(request, "min", 0)
        price_max = get_query_param_without_error(request, "max", 1000)
        page_size = get_query_param_without_error(request, "page_size", 48)
        sort_field = get_query_param_without_error(request, "sort", "title")
        is_asc = get_query_param_without_error(request, "order", 1)

        # Match aggregation for price, search and other filters
        aggregation_str = match_aggregation(
            request, search_substring, price_min, price_max
        )

        skip_documents = (current_page - 1) * page_size
        result = boots_perfume_product_collection.aggregate(
            aggregation_str
            + get_sort_aggregation(sort_field_data_label[sort_field], is_asc)
            + get_pagination_aggregation(skip_documents, page_size)
        )

        # Count total of products with the aggregation conditions
        total = list(
            boots_perfume_product_collection.aggregate(
                aggregation_str + [{"$count": "total"}]
            )
        )

        # Count total of products for each filter with the aggregation conditions
        filter_count = count_product_each_filter(aggregation_str)

        if not total:
            total = [{"total": 0}]

        print(aggregation_str)
        return Response(
            {
                "product": json.loads(json_util.dumps(result)),
                "page": current_page,
                "size": page_size,
                "total": total[0]["total"],
                "filter_count": filter_count,
            },
            status=200,
        )


# utils
def get_query_param_without_error(request, query_param, default):
    try:
        return type(default)(request.query_params[query_param])
    except MultiValueDictKeyError:
        return default
    except ValueError:
        return default


def split_str(string: str, data_type):
    str_list = string.split(";")
    return [data_type(item) for item in str_list]


def match_aggregation(request, search_substring, price_min, price_max):
    aggregation_str = get_product_between_price_aggregation(price_min, price_max)

    if search_substring != "":
        aggregation_str[0]["$match"]["title"] = {
            "$regex": search_substring,
            "$options": "i",
        }

    for field_type in filter_field_data_type:
        string = get_query_param_without_error(request, field_type, "")
        if string != "":
            arr = split_str(string, filter_field_data_type[field_type]["data_type"])
            aggregation_str[0]["$match"][
                filter_field_data_type[field_type]["param"]
            ] = {"$in": arr}

    return aggregation_str


def count_product_each_filter(extra_query=[]):
    result_dict = {}
    for field_name in group_and_count_field:
        aggregation_str = group_and_count_arr_aggregation(
            group_and_count_field[field_name]["arr"],
            group_and_count_field[field_name]["param"],
        )
        result = boots_perfume_product_collection.aggregate(
            extra_query + aggregation_str
        )
        result_dict[field_name] = result

    result_dict["price_range"] = boots_perfume_product_collection.aggregate(
        min_max_price_aggregation()
    )
    return result_dict
