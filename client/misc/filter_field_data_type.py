filter_field_data_type = {
    "brand": {"data_type": str, "param": "brand"},
    "rating": {"data_type": int, "param": "reviews.rounded"},
    "promotions": {
        "data_type": str,
        "param": "offers.text",
    },
    "product_type": {
        "data_type": str,
        "param": "attributes.product_type",
    },
    "gender": {"data_type": str, "param": "attributes.gender"},
    "size": {"data_type": str, "param": "attributes.size"},
    "gift_type": {
        "data_type": str,
        "param": "attributes.gift_type",
    },
    "recipient": {"data_type": str, "param": "attributes.recipient"},
    "body_area": {"data_type": str, "param": "attributes.body_area"},
    "product_format": {"data_type": str, "param": "attributes.format"},
    "fragrance_type": {"data_type": str, "param": "attributes.fragrance_type"},
    "fragrance_scent": {
        "data_type": str,
        "param": "attributes.fragrance_scent",
    },
}
