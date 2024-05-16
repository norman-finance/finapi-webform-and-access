# coding: utf-8

"""
    finAPI Access V2

    <strong>RESTful API for Account Information Services (AIS) and Payment Initiation Services (PIS)</strong> <br/> <strong>Application Version:</strong> 2.38.0 <br/>  The following pages give you some general information on how to use our APIs.<br/> The actual API services documentation then follows further below. You can use the menu to jump between API sections. <br/> <br/> This page has a built-in HTTP(S) client, so you can test the services directly from within this page, by filling in the request parameters and/or body in the respective services, and then hitting the TRY button. Note that you need to be authorized to make a successful API call. To authorize, refer to the 'Authorization' section of the API, or just use the OAUTH button that can be found near the TRY button. <br/>  <h2 id=\"general-information\">General information</h2>  <h3 id=\"general-error-responses\"><strong>Error Responses</strong></h3> When an API call returns with an error, then in general it has the structure shown in the following example:  <pre> {   \"errors\": [     {       \"message\": \"Interface 'FINTS_SERVER' is not supported for this operation.\",       \"code\": \"BAD_REQUEST\",       \"type\": \"TECHNICAL\"     }   ],   \"date\": \"2020-11-19T16:54:06.854+01:00\",   \"requestId\": \"selfgen-312042e7-df55-47e4-bffd-956a68ef37b5\",   \"endpoint\": \"POST /api/v2/bankConnections/import\",   \"authContext\": \"1/21\",   \"bank\": \"DEMO0002 - finAPI Test Redirect Bank (id: 280002, location: none)\" } </pre>  If an API call requires an additional authentication by the user, HTTP code 510 is returned and the error response contains the additional \"multiStepAuthentication\" object, see the following example:  <pre> {   \"errors\": [     {       \"message\": \"Es ist eine zusätzliche Authentifizierung erforderlich. Bitte geben Sie folgenden Code an: 123456\",       \"code\": \"ADDITIONAL_AUTHENTICATION_REQUIRED\",       \"type\": \"BUSINESS\",       \"multiStepAuthentication\": {         \"hash\": \"678b13f4be9ed7d981a840af8131223a\",         \"status\": \"CHALLENGE_RESPONSE_REQUIRED\",         \"challengeMessage\": \"Es ist eine zusätzliche Authentifizierung erforderlich. Bitte geben Sie folgenden Code an: 123456\",         \"answerFieldLabel\": \"TAN\",         \"redirectUrl\": null,         \"redirectContext\": null,         \"redirectContextField\": null,         \"twoStepProcedures\": null,         \"photoTanMimeType\": null,         \"photoTanData\": null,         \"opticalData\": null,         \"opticalDataAsReinerSct\": false       }     }   ],   \"date\": \"2019-11-29T09:51:55.931+01:00\",   \"requestId\": \"selfgen-45059c99-1b14-4df7-9bd3-9d5f126df294\",   \"endpoint\": \"POST /api/v2/bankConnections/import\",   \"authContext\": \"1/18\",   \"bank\": \"DEMO0001 - finAPI Test Bank\" } </pre>  An exception to this error format are API authentication errors, where the following structure is returned:  <pre> {   \"error\": \"invalid_token\",   \"error_description\": \"Invalid access token: cccbce46-xxxx-xxxx-xxxx-xxxxxxxxxx\" } </pre>  <h3 id=\"general-paging\"><strong>Paging</strong></h3> API services that may potentially return a lot of data implement paging. They return a limited number of entries within a \"page\". Further entries must be fetched with subsequent calls. <br/><br/> Any API service that implements paging provides the following input parameters:<br/> &bull; \"page\": the number of the page to be retrieved (starting with 1).<br/> &bull; \"perPage\": the number of entries within a page. The default and maximum value is stated in the documentation of the respective services.  A paged response contains an additional \"paging\" object with the following structure:  <pre> {   ...   ,   \"paging\": {     \"page\": 1,     \"perPage\": 20,     \"pageCount\": 234,     \"totalCount\": 4662   } } </pre>  <h3 id=\"general-internationalization\"><strong>Internationalization</strong></h3> The finAPI services support internationalization which means you can define the language you prefer for API service responses. <br/><br/> The following languages are available: German, English, Czech, Slovak. <br/><br/> The preferred language can be defined by providing the official HTTP <strong>Accept-Language</strong> header. <br/><br/> finAPI reacts on the official iso language codes &quot;de&quot;, &quot;en&quot;, &quot;cs&quot; and &quot;sk&quot; for the named languages. Additional subtags supported by the Accept-Language header may be provided, e.g. &quot;en-US&quot;, but are ignored. <br/> If no Accept-Language header is given, German is used as the default language. <br/><br/> Exceptions:<br/> &bull; Bank login hints and login fields are only available in the language of the bank and not being translated.<br/> &bull; Direct messages from the bank systems typically returned as BUSINESS errors will not be translated.<br/> &bull; BUSINESS errors created by finAPI directly are available in German and English.<br/> &bull; TECHNICAL errors messages meant for developers are mostly in English, but also may be translated.  <h3 id=\"general-request-ids\"><strong>Request IDs</strong></h3> With any API call, you can pass a request ID via a header with name \"X-Request-Id\". The request ID can be an arbitrary string with up to 255 characters. Passing a longer string will result in an error. <br/><br/> If you don't pass a request ID for a call, finAPI will generate a random ID internally. <br/><br/> The request ID is always returned back in the response of a service, as a header with name \"X-Request-Id\". <br/><br/> We highly recommend to always pass a (preferably unique) request ID, and include it into your client application logs whenever you make a request or receive a response (especially in the case of an error response). finAPI is also logging request IDs on its end. Having a request ID can help the finAPI support team to work more efficiently and solve tickets faster.  <h3 id=\"general-overriding-http-methods\"><strong>Overriding HTTP methods</strong></h3> Some HTTP clients do not support the HTTP methods PATCH or DELETE. If you are using such a client in your application, you can use a POST request instead with a special HTTP header indicating the originally intended HTTP method. <br/><br/> The header's name is <strong>X-HTTP-Method-Override</strong>. Set its value to either <strong>PATCH</strong> or <strong>DELETE</strong>. POST Requests having this header set will be treated either as PATCH or DELETE by the finAPI servers. <br/><br/> Example: <br/><br/> <strong>X-HTTP-Method-Override: PATCH</strong><br/> POST /api/v2/label/51<br/> {\"name\": \"changed label\"}<br/><br/> will be interpreted by finAPI as:<br/><br/> PATCH /api/v2/label/51<br/> {\"name\": \"changed label\"}<br/>  <h3 id=\"general-user-metadata\"><strong>User metadata</strong></h3> With the migration to PSD2 APIs, a new term called \"User metadata\" (also known as \"PSU metadata\") has been introduced to the API. This user metadata aims to inform the banking API if there was a real end-user behind an HTTP request or if the request was triggered by a system (e.g. by an automatic batch update). In the latter case, the bank may apply some restrictions such as limiting the number of HTTP requests for a single consent. Also, some operations may be forbidden entirely by the banking API. For example, some banks do not allow issuing a new consent without the end-user being involved. Therefore, it is certainly necessary and obligatory for the customer to provide the PSU metadata for such operations. <br/><br/> As finAPI does not have direct interaction with the end-user, it is the client application's responsibility to provide all the necessary information about the end-user. This must be done by sending additional headers with every request triggered on behalf of the end-user. <br/><br/> At the moment, the following headers are supported by the API:<br/> &bull; \"PSU-IP-Address\" - the IP address of the user's device. It has to be an IPv4 address, as some banks cannot work with IPv6 addresses. If a non-IPv4 address is passed, we will replace the value with our own IPv4 address as a fallback.<br/> &bull; \"PSU-Device-OS\" - the user's device and/or operating system identification.<br/> &bull; \"PSU-User-Agent\" - the user's web browser or other client device identification.  <h3 id=\"general-faq\"><strong>FAQ</strong></h3> <strong>Is there a finAPI SDK?</strong> <br/> Currently we do not offer a native SDK, but there is the option to generate an SDK for almost any target language via OpenAPI. Use the 'Download SDK' button on this page for SDK generation. <br/> <br/> <strong>How can I enable finAPI's automatic batch update?</strong> <br/> Currently there is no way to set up the batch update via the API. Please contact support@finapi.io for this. <br/> <br/> <strong>Why do I need to keep authorizing when calling services on this page?</strong> <br/> This page is a \"one-page-app\". Reloading the page resets the OAuth authorization context. There is generally no need to reload the page, so just don't do it and your authorization will persist. 

    The version of the OpenAPI document: 2024.18.1
    Contact: kontakt@finapi.io
    Generated by OpenAPI Generator (https://openapi-generator.tech)

    Do not edit the class manually.
"""  # noqa: E501


from __future__ import annotations
import pprint
import re  # noqa: F401
import json

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from typing_extensions import Annotated
from finapi_access.models.account_type import AccountType
from finapi_access.models.bank_interface_login_field import BankInterfaceLoginField
from finapi_access.models.bank_interface_payment_capabilities import BankInterfacePaymentCapabilities
from finapi_access.models.bank_interface_payment_constraints import BankInterfacePaymentConstraints
from finapi_access.models.bank_interface_property import BankInterfaceProperty
from finapi_access.models.banking_interface import BankingInterface
from finapi_access.models.tpp_authentication_group import TppAuthenticationGroup
from typing import Optional, Set
from typing_extensions import Self

class BankInterface(BaseModel):
    """
    Interface used to connect to a bank
    """ # noqa: E501
    banking_interface: BankingInterface = Field(description="Banking interface. Possible values:<br><br>&bull; <code>WEB_SCRAPER</code> - means that finAPI will parse data from the bank's online banking website.<br>&bull; <code>FINTS_SERVER</code> - means that finAPI will download data via the bank's FinTS server.<br>&bull; <code>XS2A</code> - means that finAPI will download data via the bank's XS2A interface.<br><br/> <strong>Type:</strong> BankingInterface", alias="bankingInterface")
    tpp_authentication_group: Optional[TppAuthenticationGroup] = Field(default=None, description="TPP Authentication Group which the bank interface is connected to<br/> <strong>Type:</strong> TppAuthenticationGroup", alias="tppAuthenticationGroup")
    login_credentials: List[BankInterfaceLoginField] = Field(description="Login fields for this interface (in the order that we suggest to show them to the user)<br/> <strong>Type:</strong> BankInterfaceLoginField", alias="loginCredentials")
    properties: List[BankInterfaceProperty] = Field(description="Set of interface properties/specifics. Possible values:<br><br>&bull; <code>REDIRECT_APPROACH</code> - means that the interface uses a redirect approach when authorizing the user. It requires you to pass the 'redirectUrl' field in all services which define the field. If the user already has imported a bank connection of the same bank that he is about to import, we recommend to confront the user with the question: <blockquote>For the selected bank you have already imported successfully the following accounts: &lt;account list&gt;. Are you sure that you want to import another bank connection from &lt;bank name&gt;? </blockquote>&bull; <code>DECOUPLED_APPROACH</code> - means that the interface can trigger a decoupled approval during user authorization.<br/><br/>&bull; <code>DETAILED_CONSENT</code> - means that the interface requires a list of account references when authorizing the user. It requires you to pass the 'accountReferences' field in all services which define the field.<br/><br/>Note that this set will be empty if the interface does not have any specific properties.<br/> <strong>Type:</strong> BankInterfaceProperty")
    login_hint: Optional[StrictStr] = Field(default=None, description="Login hint. Contains a German message for the user that explains what kind of credentials are expected.<br/><br/>Please note that it is essential to always show the login hint to the user if there is one, as the credentials that finAPI requires for the bank might be different to the credentials that the user knows from his online banking.<br/><br/>Also note that the contents of this field should always be interpreted as HTML, as the text might contain HTML tags for highlighted words, paragraphs, etc.", alias="loginHint")
    health: Annotated[int, Field(le=100, strict=True, ge=0)] = Field(description="The health status of this interface. This is a value between 0 and 100, depicting the percentage of successful communication attempts with the bank via this interface during the last couple of bank connection imports or updates (across the entire finAPI system). <br/><br/>Note:<br/>&bull; 'Successful' communication attempt means that there was no technical error trying to establish a communication with the bank. Non-technical errors (like incorrect credentials) are regarded successful communication attempts.<br/>&bull; If an interface is not supported (see fields 'isAisSupported'/'isPisSupported'), the health will always be 0.")
    last_communication_attempt: Optional[datetime] = Field(default=None, description="<strong>Format:</strong> 'YYYY-MM-DD'T'HH:MM:SS.SSSXXX' (RFC 3339, section 5.6)<br/>Time of the last communication attempt with this interface during an import, update or connect interface (across the entire finAPI system).", alias="lastCommunicationAttempt")
    last_successful_communication: Optional[datetime] = Field(default=None, description="<strong>Format:</strong> 'YYYY-MM-DD'T'HH:MM:SS.SSSXXX' (RFC 3339, section 5.6)<br/>Time of the last successful communication with this interface during an import, update or connect interface (across the entire finAPI system).", alias="lastSuccessfulCommunication")
    is_ais_supported: StrictBool = Field(description="Whether this interface has the general capability to perform Account Information Services (AIS), i.e. if this interface can be used to download accounts, balances and transactions. ", alias="isAisSupported")
    is_pis_supported: StrictBool = Field(description="Whether this interface has the general capability to perform Payment Initiation Services (PIS). For more details, see the field 'paymentCapabilities'.", alias="isPisSupported")
    payment_capabilities: BankInterfacePaymentCapabilities = Field(description="The general payment capabilities of this interface. If a capability is 'true', it means that the option is supported, as long as the involved account also supports it (see AccountInterface.capabilities and AccountInterface.paymentCapabilities).<br/><br/>If a capability is 'false', then the option is not supported for any account.<br/> <strong>Type:</strong> BankInterfacePaymentCapabilities", alias="paymentCapabilities")
    payment_constraints: Optional[BankInterfacePaymentConstraints] = Field(default=None, alias="paymentConstraints")
    ais_account_types: List[AccountType] = Field(description="The set of account types that we can confirm can be successfully imported through this interface. This field can help you select the appropriate interface if you want to fetch only specific account types when importing or updating a bank connection (see the field <code>accountTypes</code> in the respective services).<br/><br/>Note:<br/>&bull; The set can change over time. When we learn that a certain account type can be received, it will be added to the set. But an account type can also disappear from the set, when it was no longer received for a while.<br/>&bull; If an account type is not contained in the set, it could still be that the interface will provide such accounts - we just haven't seen this for a while. Accordingly, this field is only meant to hint you at the most promising interface. If none of a bank's interfaces have your desired account type listed, we still advise you to make an attempt.<br/>&bull; The set is not updated in real-time, but rather periodically. When you make a successful import of an account type that is not yet listed, there will be a delay until it appears.<br/> <strong>Type:</strong> AccountType", alias="aisAccountTypes")
    __properties: ClassVar[List[str]] = ["bankingInterface", "tppAuthenticationGroup", "loginCredentials", "properties", "loginHint", "health", "lastCommunicationAttempt", "lastSuccessfulCommunication", "isAisSupported", "isPisSupported", "paymentCapabilities", "paymentConstraints", "aisAccountTypes"]

    model_config = ConfigDict(
        populate_by_name=True,
        validate_assignment=True,
        protected_namespaces=(),
    )


    def to_str(self) -> str:
        """Returns the string representation of the model using alias"""
        return pprint.pformat(self.model_dump(by_alias=True))

    def to_json(self) -> str:
        """Returns the JSON representation of the model using alias"""
        # TODO: pydantic v2: use .model_dump_json(by_alias=True, exclude_unset=True) instead
        return json.dumps(self.to_dict())

    @classmethod
    def from_json(cls, json_str: str) -> Optional[Self]:
        """Create an instance of BankInterface from a JSON string"""
        return cls.from_dict(json.loads(json_str))

    def to_dict(self) -> Dict[str, Any]:
        """Return the dictionary representation of the model using alias.

        This has the following differences from calling pydantic's
        `self.model_dump(by_alias=True)`:

        * `None` is only added to the output dict for nullable fields that
          were set at model initialization. Other fields with value `None`
          are ignored.
        """
        excluded_fields: Set[str] = set([
        ])

        _dict = self.model_dump(
            by_alias=True,
            exclude=excluded_fields,
            exclude_none=True,
        )
        # override the default output from pydantic by calling `to_dict()` of tpp_authentication_group
        if self.tpp_authentication_group:
            _dict['tppAuthenticationGroup'] = self.tpp_authentication_group.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in login_credentials (list)
        _items = []
        if self.login_credentials:
            for _item in self.login_credentials:
                if _item:
                    _items.append(_item.to_dict())
            _dict['loginCredentials'] = _items
        # override the default output from pydantic by calling `to_dict()` of payment_capabilities
        if self.payment_capabilities:
            _dict['paymentCapabilities'] = self.payment_capabilities.to_dict()
        # override the default output from pydantic by calling `to_dict()` of payment_constraints
        if self.payment_constraints:
            _dict['paymentConstraints'] = self.payment_constraints.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of BankInterface from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "bankingInterface": obj.get("bankingInterface"),
            "tppAuthenticationGroup": TppAuthenticationGroup.from_dict(obj["tppAuthenticationGroup"]) if obj.get("tppAuthenticationGroup") is not None else None,
            "loginCredentials": [BankInterfaceLoginField.from_dict(_item) for _item in obj["loginCredentials"]] if obj.get("loginCredentials") is not None else None,
            "properties": obj.get("properties"),
            "loginHint": obj.get("loginHint"),
            "health": obj.get("health"),
            "lastCommunicationAttempt": obj.get("lastCommunicationAttempt"),
            "lastSuccessfulCommunication": obj.get("lastSuccessfulCommunication"),
            "isAisSupported": obj.get("isAisSupported"),
            "isPisSupported": obj.get("isPisSupported"),
            "paymentCapabilities": BankInterfacePaymentCapabilities.from_dict(obj["paymentCapabilities"]) if obj.get("paymentCapabilities") is not None else None,
            "paymentConstraints": BankInterfacePaymentConstraints.from_dict(obj["paymentConstraints"]) if obj.get("paymentConstraints") is not None else None,
            "aisAccountTypes": obj.get("aisAccountTypes")
        })
        return _obj


