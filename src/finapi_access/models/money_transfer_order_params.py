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

from pydantic import BaseModel, ConfigDict, Field, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from finapi_access.models.counterpart_address_data import CounterpartAddressData
from finapi_access.models.currency import Currency
from typing import Optional, Set
from typing_extensions import Self

class MoneyTransferOrderParams(BaseModel):
    """
    Parameters for a money transfer order
    """ # noqa: E501
    counterpart_name: Optional[Annotated[str, Field(min_length=1, strict=True, max_length=70)]] = Field(default=None, description="Name of the counterpart. Has to be provided for the SEPA EUR transfers (see BankInterface.paymentConstraints.sepaMoneyTransfer.mandatoryFields.counterpartName). Note: Neither finAPI nor the involved bank servers are guaranteed to validate the counterpart name. Even if the name does not depict the actual registered account holder of the target account, the order might still be successful.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/payment-data-validation' target='_blank'> Payment Data Validation documentation </a> for more details.", alias="counterpartName")
    counterpart_iban: StrictStr = Field(description="IBAN of the counterpart's account.", alias="counterpartIban")
    counterpart_bic: Optional[StrictStr] = Field(default=None, description="BIC of the counterpart's account. This field is required for SEPA payments (i.e. payments in EUR currency), when there is no 'IBAN_ONLY'-capability in the respective account/interface combination that is to be used when submitting the payment.<br/>Bank-specific constraints may apply to this field. Please refer to BankInterface.paymentConstraints to make sure the payment you are creating won't get rejected.", alias="counterpartBic")
    counterpart_bank_name: Optional[Annotated[str, Field(min_length=1, strict=True, max_length=128)]] = Field(default=None, description="Name of the counterpart's bank. Only required for banks that have BankInterface.paymentConstraints.sepaMoneyTransfer.mandatoryFields.counterpartBankName constraint. <br/>Note: Neither finAPI nor the involved bank servers are guaranteed to validate the counterpart bank name.", alias="counterpartBankName")
    amount: Union[StrictFloat, StrictInt] = Field(description="The amount of the payment. Must be a positive decimal number with at most two decimal places.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/payment-data-validation' target='_blank'> Payment Data Validation documentation </a> for more details.")
    currency: Optional[Currency] = Field(default=None, description="The currency code of the 'amount'. To be provided in the ISO 4217 Alpha 3 format.<br/><strong>NOTES:</strong><br/>&bull; If not set, then for money transfers over the XS2A interface, finAPI will interpret the amount to be in the currency of the related account. For money transfers over other interfaces (FINTS_SERVER, WEB_SCRAPER), as well as for standalone money transfers (finAPI Payment product) over all interfaces (FINTS_SERVER, WEB_SCRAPER, XS2A), finAPI will consider the amount to be in EUR.<br/>&bull; If set in the context of a collective money transfer, then all orders must have the same currency.<br/>&bull; If set for money transfers with an accountId, then the currency must match the account currency.<br/> <strong>Type:</strong> Currency")
    purpose: Optional[Annotated[str, Field(min_length=1, strict=True, max_length=2000)]] = Field(default=None, description="The purpose of the transfer transaction.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/payment-data-validation' target='_blank'> Payment Data Validation documentation </a> for more details.<br/>Bank-specific constraints may apply to this field. Please refer to BankInterface.paymentConstraints to make sure the payment you are creating won't get rejected.")
    sepa_purpose_code: Optional[StrictStr] = Field(default=None, description="SEPA purpose code, according to ISO 20022, external codes set.<br/>Please note that the SEPA purpose code may be ignored by some banks and will be discarded for the non-SEPA payments.", alias="sepaPurposeCode")
    counterpart_address: Optional[CounterpartAddressData] = Field(default=None, description="Counterpart Address. These address fields are only relevant in very few cases if the debtor bank requires the counterpart's address.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/czech-republic-sepa-transfers' target='_blank'> Czech Republic SEPA Transfers documentation </a> for more details.<br/> <strong>Type:</strong> CounterpartAddressData", alias="counterpartAddress")
    end_to_end_id: Optional[Annotated[str, Field(min_length=1, strict=True, max_length=35)]] = Field(default=None, description="End-To-End ID for the transfer transaction.<br/>Only applicable for the SEPA EUR transfers and will be discarded for other transfers.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/payment-data-validation' target='_blank'> Payment Data Validation documentation </a> for more details.<br/>Bank-specific constraints may apply to this field. Please refer to BankInterface.paymentConstraints to make sure the payment you are creating won't get rejected.", alias="endToEndId")
    structured_remittance_information: List[Annotated[str, Field(min_length=1, strict=True, max_length=2000)]] = Field(description="Structure Remittance Information.<br/>This attribute is used to submit structured remittance information for the domestic payments.<br/>Please refer to the <a href='https://documentation.finapi.io/payments/Czech-Republic-Domestic-Transfers.3045916711.html' target='_blank'>documentation</a> for more details.", alias="structuredRemittanceInformation")
    __properties: ClassVar[List[str]] = ["counterpartName", "counterpartIban", "counterpartBic", "counterpartBankName", "amount", "currency", "purpose", "sepaPurposeCode", "counterpartAddress", "endToEndId", "structuredRemittanceInformation"]

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
        """Create an instance of MoneyTransferOrderParams from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of counterpart_address
        if self.counterpart_address:
            _dict['counterpartAddress'] = self.counterpart_address.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of MoneyTransferOrderParams from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "counterpartName": obj.get("counterpartName"),
            "counterpartIban": obj.get("counterpartIban"),
            "counterpartBic": obj.get("counterpartBic"),
            "counterpartBankName": obj.get("counterpartBankName"),
            "amount": obj.get("amount"),
            "currency": obj.get("currency"),
            "purpose": obj.get("purpose"),
            "sepaPurposeCode": obj.get("sepaPurposeCode"),
            "counterpartAddress": CounterpartAddressData.from_dict(obj["counterpartAddress"]) if obj.get("counterpartAddress") is not None else None,
            "endToEndId": obj.get("endToEndId"),
            "structuredRemittanceInformation": obj.get("structuredRemittanceInformation")
        })
        return _obj


