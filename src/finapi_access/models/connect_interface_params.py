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

from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional
from finapi_access.models.account_reference import AccountReference
from finapi_access.models.account_type import AccountType
from finapi_access.models.banking_interface import BankingInterface
from finapi_access.models.login_credential import LoginCredential
from finapi_access.models.multi_step_authentication_callback import MultiStepAuthenticationCallback
from typing import Optional, Set
from typing_extensions import Self

class ConnectInterfaceParams(BaseModel):
    """
    Container for interface connection parameters
    """ # noqa: E501
    bank_connection_id: StrictInt = Field(description="Bank connection identifier", alias="bankConnectionId")
    banking_interface: BankingInterface = Field(description="The interface to use for connecting with the bank.<br/> <strong>Type:</strong> BankingInterface", alias="bankingInterface")
    source_banking_interface: Optional[BankingInterface] = Field(default=None, description="The source interface that should be used as the source of credentials. Set it to one of already existing bank connection's interfaces and finAPI will try to use the stored credentials of that interface for the current service call. The source interface must fit the following requirements:<br/>- it must have the same set of bank login fields as the main interface (the 'bankingInterface' parameter);<br/>- it must have stored values for all its bank login fields.<br/>If any of those conditions are not met - the service will throw an appropriate error.<br/>Note: the source interface is ignored if any login credentials are given.<br/> <strong>Type:</strong> BankingInterface", alias="sourceBankingInterface")
    login_credentials: Optional[List[LoginCredential]] = Field(default=None, description="Set of login credentials. Must always be passed, unless the respective bank interface does not declare any login fields.<br/> <strong>Type:</strong> LoginCredential", alias="loginCredentials")
    store_secrets: Optional[StrictBool] = Field(default=False, description="Whether to store the secret login fields. If the secret fields are stored, then updates can be triggered without the involvement of the users, as long as the credentials remain valid and the bank consent has not expired. Note that bank consent will be stored regardless of the field value. Default value is false.", alias="storeSecrets")
    skip_balances_download: Optional[StrictBool] = Field(default=False, description="Whether to skip the download of balances or not. May only be set to true if 'skipPositionsDownload' is also true. If set to true, then finAPI will download just the account list with the accounts' information (like account name, number, holder, etc). Default is false.<br/><br/>NOTES:<br/>&bull; Setting this flag to true is only meant to be used if A) you generally never download balances and positions, because you are only interested in the account list, or B) you want to get just the list of accounts in the first step, and then delete unwanted accounts from the bank connection, before you trigger another update that downloads balances and transactions. This approach allows you to download balances only for the accounts that you want.<br/>&bull; If you skip the download of balances during an import or update, you can still download them with a later update.<br/>&bull; If an account was stored with a balance already, and you skip the download of its balance in a subsequent update, then the account's balance will get outdated. Be also aware that certain services (like GET /accounts/dailyBalances) may return incorrect results in such cases.<br/>&bull; If any bank connection gets updated via finAPI's automatic batch update, then all balances (of already imported accounts) <u>will</u> get downloaded in any case!", alias="skipBalancesDownload")
    skip_positions_download: Optional[StrictBool] = Field(default=False, description="Whether to skip the download of transactions and securities or not. If set to true, then finAPI will download just the account list with the accounts' information (like account name, number, holder, etc), as well as the accounts' balances (if possible), but skip the download of transactions and securities. Default is false.<br/>You may also use this flag in combination with 'skipBalancesDownload' = true, to additionally skip the download of balances.<br/><br/>NOTES:<br/>&bull; Setting this flag to true is only meant to be used if A) you generally never download positions, because you are only interested in the account list and/or balances, or B) you want to get just the list of accounts in the first step, and then delete unwanted accounts from the bank connection, before you trigger another update that downloads transactions. This approach allows you to download transactions only for the accounts that you want.<br/>&bull; If you skip the download of transactions and securities during an import or update, you can still download them with a later update (though you might not get all positions at a later point, because the date range in which the bank servers provide this data is usually limited).<br/>&bull; If an account already had any positions imported before an update, and you skip the positions download in the update, then the account's updated balance might not add up to the set of transactions / security positions. Be aware that certain services (like GET /accounts/dailyBalances) may return incorrect results for accounts in such a state.<br/>&bull; If any bank connection gets updated via finAPI's automatic batch update, then all transactions and security positions (of already imported accounts) <u>will</u> get downloaded in any case!<br/>&bull; For security accounts, skipping the downloading of the securities might result in the account's balance also not being downloaded.<br/>&bull; For the WEB_SCRAPER interface, it's technically required to download transactions for Bausparen accounts even if 'skipPositionsDownload' is set to true, but they are not actively processed by finAPI.", alias="skipPositionsDownload")
    load_owner_data: Optional[StrictBool] = Field(default=False, description="Whether to load information about the bank connection owner(s) - see field 'owners'. Default value is 'false'.<br/><br/>NOTE: This feature is supported only by the WEB_SCRAPER interface.", alias="loadOwnerData")
    account_types: Optional[List[AccountType]] = Field(default=None, description="If specified, then finAPI will import only those accounts whose type is one of the given types. Note that when the bank connection does not contain any accounts of the given types, the operation will fail with error code NO_ACCOUNTS_FOR_TYPE_LIST.<br/><br/><b>NOTE</b>: If your client is restricted to certain account types (see <code>ClientConfiguration.accountTypeRestrictions</code>), then you may only specify account types that are enabled for you, otherwise the service will return with an error. If your client has account type restrictions and you do not specify any types, then the service will implicitly limit the types according to your client's configuration.<br/> <strong>Type:</strong> AccountType", alias="accountTypes")
    account_references: Optional[List[AccountReference]] = Field(default=None, description="List of accounts for which access is requested from the bank. It must only be passed if the bank interface has the DETAILED_CONSENT property set.<br/> <strong>Type:</strong> AccountReference", alias="accountReferences")
    multi_step_authentication: Optional[MultiStepAuthenticationCallback] = Field(default=None, description="Container for multi-step authentication data. Required when a previous service call initiated a multi-step authentication.<br/> <strong>Type:</strong> MultiStepAuthenticationCallback", alias="multiStepAuthentication")
    redirect_url: Optional[StrictStr] = Field(default=None, description="Must only be passed when the used interface has the property REDIRECT_APPROACH. The user will be redirected to the given URL from the bank's website after completing the bank login and (possibly) the SCA.", alias="redirectUrl")
    max_days_for_download: Optional[StrictInt] = Field(default=0, description="This setting defines how much of an account's transactions history will get downloaded whenever a new account is imported. More technically, it depicts the number of days to download transactions for, starting from - and including - the date of the account import. For example, on an account import that happens today, the value 30 would instruct finAPI to download transactions from the past 30 days (including today). The minimum allowed value is 14, the maximum value is 3650. Also possible is the value 0 (which is the default value), in which case there will be no limit to the transactions download and finAPI will try to get all transactions that it can. <br/><br/>NOTES:<br/>&bull; There is no guarantee that finAPI will actually download transactions for the entire defined date range, as there may be limitations to the download range (set by the bank or by finAPI, e.g. see ClientConfiguration.transactionImportLimitation). <br/>&bull; This parameter only applies to transactions, not to security positions; For security accounts, finAPI will always download all security positions that it can. <br/>&bull; This setting is stored for each interface individually.<br/>&bull; After an interface has been connected with this setting, there is no way to change the setting for that interface afterwards.<br/>&bull; <b>If you do not limit the download range to a value less than 90 days, the bank is more likely to trigger a strong customer authentication request for the user when finAPI is attempting to download the transactions.</b>", alias="maxDaysForDownload")
    __properties: ClassVar[List[str]] = ["bankConnectionId", "bankingInterface", "sourceBankingInterface", "loginCredentials", "storeSecrets", "skipBalancesDownload", "skipPositionsDownload", "loadOwnerData", "accountTypes", "accountReferences", "multiStepAuthentication", "redirectUrl", "maxDaysForDownload"]

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
        """Create an instance of ConnectInterfaceParams from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of each item in login_credentials (list)
        _items = []
        if self.login_credentials:
            for _item in self.login_credentials:
                if _item:
                    _items.append(_item.to_dict())
            _dict['loginCredentials'] = _items
        # override the default output from pydantic by calling `to_dict()` of each item in account_references (list)
        _items = []
        if self.account_references:
            for _item in self.account_references:
                if _item:
                    _items.append(_item.to_dict())
            _dict['accountReferences'] = _items
        # override the default output from pydantic by calling `to_dict()` of multi_step_authentication
        if self.multi_step_authentication:
            _dict['multiStepAuthentication'] = self.multi_step_authentication.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of ConnectInterfaceParams from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "bankConnectionId": obj.get("bankConnectionId"),
            "bankingInterface": obj.get("bankingInterface"),
            "sourceBankingInterface": obj.get("sourceBankingInterface"),
            "loginCredentials": [LoginCredential.from_dict(_item) for _item in obj["loginCredentials"]] if obj.get("loginCredentials") is not None else None,
            "storeSecrets": obj.get("storeSecrets") if obj.get("storeSecrets") is not None else False,
            "skipBalancesDownload": obj.get("skipBalancesDownload") if obj.get("skipBalancesDownload") is not None else False,
            "skipPositionsDownload": obj.get("skipPositionsDownload") if obj.get("skipPositionsDownload") is not None else False,
            "loadOwnerData": obj.get("loadOwnerData") if obj.get("loadOwnerData") is not None else False,
            "accountTypes": obj.get("accountTypes"),
            "accountReferences": [AccountReference.from_dict(_item) for _item in obj["accountReferences"]] if obj.get("accountReferences") is not None else None,
            "multiStepAuthentication": MultiStepAuthenticationCallback.from_dict(obj["multiStepAuthentication"]) if obj.get("multiStepAuthentication") is not None else None,
            "redirectUrl": obj.get("redirectUrl"),
            "maxDaysForDownload": obj.get("maxDaysForDownload") if obj.get("maxDaysForDownload") is not None else 0
        })
        return _obj


