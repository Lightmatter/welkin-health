# welkin-health

## A Python wrapper of the Welkin Health API

[![Version](https://img.shields.io/pypi/v/welkin-health)](https://pypi.org/project/welkin-health/)

This package allows Python developers to write software that makes use of the Welkin Health API. Functions available in the API are mirrored in this package as closely as possible, translating JSON responses to Python objects. You can find the current documentation for the Welkin Health API here:

[Welkin Health API Documentation](https://developers.welkinhealth.com/)

### Installing

```
pip install welkin
```

### Quick Start

```python
from welkin import Client

welkin = Client(
    tenant="gh", api_client="VBOPNRYRWJIP", secret_key="+}B{KGTG6#zG%P;tQm0C"
)

# Create a calendar event
patient = welkin.Patient(id="6801d498-26f4-4aee-961b-5daffcf193c8")
user = welkin.User(username="johndoe")
event = welkin.Calendar(
    start="2020-01-01T00:00:00.000Z",
    end="2020-01-31T23:59:59.000Z",
    patient=patient,
    host=user,
).post()

# Get a calendar event by ID
event = welkin.Calendar(id="313c2029-493b-4114-8b86-788d631a1851").get()

# Get a single calendar event
event = welkin.Calendar().get(id="313c2029-493b-4114-8b86-788d631a1851")

# Search for calendar events with pagination
events = welkin.Calendar().get(
    from_date="2020-01-15T14:00:00.000Z",
    to_date="2020-02-11T00:00:00.000Z",
    paginate=True,
)
for event in events:
    print(event)
```
