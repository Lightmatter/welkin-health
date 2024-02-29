# welkin-health

## A Python wrapper of the Welkin Health API

[![Version](https://img.shields.io/pypi/v/welkin?style=for-the-badge&logo=pypi&logoColor=fff)](https://pypi.org/project/welkin/)
[![Python](https://img.shields.io/pypi/pyversions/welkin?style=for-the-badge&logo=python&logoColor=fff)](https://pypi.org/project/welkin/)
[![License: GPL v3](https://img.shields.io/badge/License-GPLv3-blue.svg?style=for-the-badge&logo=gnu&logoColor=fff)](https://www.gnu.org/licenses/gpl-3.0)
[![Tests](https://img.shields.io/github/actions/workflow/status/lightmatter/welkin-health/ci.yaml?branch=develop&style=for-the-badge&logo=githubactions&logoColor=fff&label=Tests)](https://github.com/Lightmatter/welkin-health/actions)

[![codecov](https://img.shields.io/codecov/c/gh/Lightmatter/welkin-health?logo=codecov&logoColor=fff&style=for-the-badge)](https://codecov.io/gh/Lightmatter/welkin-health)

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


### Patient methods
patient = welkin.Patient(firstName="Foo", lastName="Bar").create()  # Create

patient = welkin.Patient(id="6801d498-26f4-4aee-961b-5daffcf193c8").get()  # Read
patients = welkin.Patients().get()  # Read all/list

patient.update(firstName="Baz")  # Update
patient.delete()  # Delete

### User methods
user = client.User(username="bar", email="bar@foo.com").create()  # Create

user = welkin.User(id="301b2895-cbf0-4cac-b4cf-1d082faee95c").get()  # Read
users = welkin.Users().get()  # Read all/list
uasers = welkin.Users().get(
    search="lightmatter", region="east-coast", seat_assigned=True, user_state="ACTIVE"
)  # Filtered read all/list

user.update(firstName="Baz")  # Update
user.delete()  # Delete
```
