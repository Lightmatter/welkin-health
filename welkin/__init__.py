"""Welkin Health API wrapper

https://developers.welkinhealth.com/

Introduction
========
When reading this API, we take a liberty and assume that you are familiar with the
following Welkin concepts, but for the sake of clarity will shortly repeat them here:

1. Tenant (Organization) - This is a customer space, dedicated to one customer. Every
customer will have its own tenant that will host customer users, apps and instances
2. Instance (Environment) - This is a separate database inside a tenant. Typical
customer will have 2-3 instances, representing customer development, testing and live
environments, as you build out your Welkin care program
3. API client - this is an auto-generated pair of key and secrets, that allows you to
access variety of API that Welkin exposes
4. Security Policies and Roles - set of rules that dictates what API your client can
access and what actions are allowed to be performed
5. Designer - Codeless editor for configuring Care Program and all the elements of that
program, including Permissions and Roles
6. Admin - Admin app that allows one to assign permissions and roles to API clients
(among other things)
7. Care - Care portal that users will be using to deliver care to patients

For better demonstration of the API, we will use the following setup:

Organization (Tenant): gh
Instance (Environment): sb-demo

Creating API Client
========
Though this is better covered in our User Guide document, we are going to repeat the
steps here, to ensure successful setup

1. Create API client in your Organization
 - Navigate to Admin -> API Clients -> Create Client
 - Copy the Client Name and Secret Key or download it.
2. Navigate to the API Client page you created
 - Configure appropriate access for the client (Instance Access, Roles, Security
 Policies)

Reminder: Security Policies and Roles are defined in the Designer and assigned in the
Admin

For this example we will assume Client Name is VBOPNRYRWJIP and Secret Key is
+}B{KGTG6#zG%P;tQm0C
"""
from welkin.__version__ import (
    __author__,
    __author_email__,
    __copyright__,
    __description__,
    __license__,
    __title__,
    __url__,
    __version__,
)
from welkin.client import Client

__all__ = ["Client"]
