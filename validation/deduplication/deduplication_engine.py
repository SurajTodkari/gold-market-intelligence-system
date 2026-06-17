import hashlib

seen_events = set()

def generate_event_hash(event):

   unique_string = (

      event["source_event_id"] +

      event["event_name"] +

      event["country"]
    )

   return hashlib.md5(

      unique_string.encode()

    ).hexdigest()

def is_duplicate(event):

    event_hash = generate_event_hash(event)

    if event_hash in seen_events:

     return True

    seen_events.add(event_hash)

    return False