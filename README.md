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
    tenant="gh",
    instance="sb-demo",
    api_client="VBOPNRYRWJIP",
    secret_key="+}B{KGTG6#zG%P;tQm0C",
)


# Patient methods
patient = welkin.Patient(firstName="Foo", lastName="Bar").create()  # Create

patient = welkin.Patient(id="6801d498-26f4-4aee-961b-5daffcf193c8").get()  # Read
patients = welkin.Patients().get()  # Read all/list

patient.update(firstName="Baz")  # Update
patient.delete()  # Delete

# User methods
user = client.User(username="bar", email="bar@foo.com").create()  # Create

user = welkin.User(id="301b2895-cbf0-4cac-b4cf-1d082faee95c").get()  # Read
users = welkin.Users().get()  # Read all/list

user.update(firstName="Baz")  # Update
user.delete()  # Delete
```
