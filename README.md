# welkin-health

## A Python wrapper of the Welkin Health API

[![Version](https://img.shields.io/pypi/v/welkin?style=for-the-badge&logo=pypi&logoColor=fff)](https://pypi.org/project/welkin/)
[![Python](https://img.shields.io/pypi/pyversions/welkin?style=for-the-badge&logo=python&logoColor=fff)](https://pypi.org/project/welkin/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge&logo=gnu&logoColor=fff)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests](https://img.shields.io/github/workflow/status/lightmatter/welkin-health/Python%20%F0%9F%90%8D%20package%20%F0%9F%93%A6%20test?style=for-the-badge&logo=githubactions&logoColor=fff&label=Tests)](https://github.com/Lightmatter/welkin-health/actions)
[![codecov](https://img.shields.io/codecov/c/gh/Lightmatter/welkin-health?logo=codecov&logoColor=fff&style=for-the-badge)](https://codecov.io/gh/Lightmatter/welkin-health)

This package allows Python developers to write software that makes use of the Welkin Health API. Functions available in the API are mirrored in this package as closely as possible, translating JSON responses to Python objects. You can find the current documentation for the Welkin Health API here:

[Welkin Health API Documentation](https://developers.welkinhealth.com/)

## Installing

```
pip install welkin
```

## Quick Start

```python
from welkin import Client

client = Client(
    tenant="gh",
    instance="sb-demo",
    api_client="VBOPNRYRWJIP",
    secret_key="+}B{KGTG6#zG%P;tQm0C",
)
patient = client.Patient(
  firstName="Foo",
  lastName="Bar",
).create()
```

## Examples

### Create a Patient

```python
patient = client.Patient(
  firstName="Peter",
  lastName="Parker"
).create()
```

### Get and Update an existing Patient

```python
# single patient
patient = client.Patient(
  id=patient_id
).get()

patient.update(firstName="Miles")
patient.delete()

# list of patients
patients = client.Patients(filter=**filter_kwargs).get()
```

### Update the CDT fields on an existing Patient

```python
patient = client.Patient(id=patient_id).get()
possible_cdts = patient.CDTs(name="Initial Checkup").get()
found_cdt = possible_cdts[0]

# associate the cdt with the patient in memory
# and pull any additional details from welkin
cdt = patient.CDT(**found_cdt).get()
cdt.update(**{
    "cdtf-weight": 190.2,
})
```

### Create a User

```python
user = client.User(username="bar", email="bar@foo.com").create()  # Create
```

### Get or search for a user

```python

# get a single user
user = client.User(id=user_id).get()

# get a list of users
users = client.Users().get()  # Read all/list

# filter/search for a specific subset of user(s)
uasers = client.Users().get(
    search="lightmatter",
    region="east-coast",
    seat_assigned=True,
    user_state="ACTIVE"
)
```

### Update or delete a user

```
user.update(firstName="Spiddy")
user.delete()
```

## Common Issues

1. I keep getting errors about `self` not having an id, or `self._parent` being `None`. Help!
This generally means you are trying to perform an action on an object which was pulled from
welkin but hasn't been properly wrapped by it's parent. This is common when pulling a list of objects
and then trying to perform operations on an object in that list.

The easiest workaround is to initialize a new value in memory that is associated with the parent.
For exmaple, change this:

```python
cdt = patient.CDTs(name="Initial Checkup").get()[0]
cdt.update(**fields)
```

Into this:

```python
found_cdt = patient.CDTs(name="Initial Checkup").get()[0]
cdt = patient.CDT(**found_cdt).get()
cdt.update(**fields)
```
To understand why this happens ref: [`SchemaBase`](https://github.com/Lightmatter/welkin-health/blob/main/welkin/models/base.py)


