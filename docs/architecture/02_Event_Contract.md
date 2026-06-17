# Canonical Event Contract

Version: 1.0

Status: Mandatory

---

# Purpose

All ingestion sources must publish events using the same structure.

No source-specific fields are allowed inside downstream services.

---

# Canonical Event

{
"source_event_id": str,

```
"source": str,

"event_name": str,

"country": str,

"currency": str,

"impact": str,

"actual": str,

"forecast": str,

"previous": str,

"source_event_date": str,

"source_event_time": str,

"published_at": str,

"ingested_at": str,

"trace": dict
```

}

---

# Required Fields

source_event_id
source
event_name
published_at
ingested_at

---

# Ownership

Any change to this contract requires architecture approval.

No engineer may modify this structure unilaterally.

---

# Rationale

A canonical contract enables:

* source replacement
* source expansion
* validation reuse
* persistence reuse
* monitoring reuse
* intelligence reuse
