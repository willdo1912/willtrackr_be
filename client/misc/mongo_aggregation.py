def min_max_price_aggregation():
    return [
        {
            "$group": {
                "_id": None,
                "minPrice": {"$min": "$pricing.current.value"},
                "maxPrice": {"$max": "$pricing.current.value"},
            }
        }
    ]


def group_and_count_aggregation(param: str):
    return [
        {"$match": {param: {"$ne": None}}},
        {"$group": {"_id": f"${param}", "count": {"$sum": 1}}},
        {"$sort": {"_id": -1}},
    ]


def group_and_count_arr_aggregation(arr: str, param: str):
    return [
        {"$unwind": f"${arr}"},
        {"$match": {param: {"$ne": None}}},
        {"$group": {"_id": f"${param}", "count": {"$sum": 1}}},
        {"$sort": {"_id": -1}},
    ]


def get_product_between_price_aggregation(price_min: int, price_max: int):
    return [
        {
            "$match": {
                "pricing.current.value": {
                    "$gte": price_min,
                    "$lte": price_max,
                },
            }
        },
    ]


def get_pagination_aggregation(skip_documents: int, page_size: int):
    return [
        {"$skip": skip_documents},
        {"$limit": page_size},
    ]


def get_sort_aggregation(sort_param: str, is_asc: int):
    return [{"$sort": {sort_param: is_asc}}]
