from validation.deduplication.deduplication_engine import is_duplicate


event = {

    "title": "US CPI Released",

    "country": "US",

    "event_type": "CPI_RELEASE"
}


print(is_duplicate(event))

print(is_duplicate(event))