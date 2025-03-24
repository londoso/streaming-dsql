INPUT = {
    "$schema": "http://json-schema.org/draft-04/schema#",
    "title": "StreamingDSQLInput",
    "description": "Input schema for the StreamingDSQL Lambda function",
    "type": "object",
    "properties": {
        "index": {
            "type": "string"
        },
        "customer_id": {
            "type": "string"
        },
        "first_name": {
            "type": "string"
        },
        "last_name": {
            "type": "string"
        },
        "company": {
            "type": "string"
        },
        "city": {
            "type": "string"
        },
        "country": {
            "type": "string"
        },
        "phone1": {
            "type": "string"
        },
        "phone2": {
            "type": "string"
        },
        "email": {
            "type": "string"
        },
        "subscription_date": {
            "type": "string"
        },
        "website": {
            "type": "string"
        }
    },
    "required": [
        "index",
        "customer_id",
        "first_name",
        "last_name",
        "company",
        "city",
        "country",
        "phone1",
        "phone2",
        "email",
        "subscription_date",
        "website"    
    ]
}