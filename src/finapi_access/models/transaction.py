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

from datetime import date, datetime
from pydantic import BaseModel, ConfigDict, Field, StrictBool, StrictFloat, StrictInt, StrictStr
from typing import Any, ClassVar, Dict, List, Optional, Union
from typing_extensions import Annotated
from finapi_access.models.category import Category
from finapi_access.models.certis_transaction_data import CertisTransactionData
from finapi_access.models.currency import Currency
from finapi_access.models.label import Label
from finapi_access.models.paypal_transaction_data import PaypalTransactionData
from typing import Optional, Set
from typing_extensions import Self

class Transaction(BaseModel):
    """
    Container for a transaction's data
    """ # noqa: E501
    id: StrictInt = Field(description="Transaction identifier")
    parent_id: Optional[StrictInt] = Field(default=None, description="Parent transaction identifier", alias="parentId")
    account_id: StrictInt = Field(description="Account identifier", alias="accountId")
    value_date: date = Field(description="<strong>Format:</strong> 'YYYY-MM-DD'<br/>Value date.", alias="valueDate")
    bank_booking_date: date = Field(description="<strong>Format:</strong> 'YYYY-MM-DD'<br/>Bank booking date.", alias="bankBookingDate")
    finapi_booking_date: date = Field(description="<strong>Format:</strong> 'YYYY-MM-DD'<br/>finAPI Booking date. NOTE: In some cases, banks may deliver transactions that are booked in future, but already included in the current account balance. To keep the account balance consistent with the set of transactions, such \"future transactions\" will be imported with their finapiBookingDate set to the current date (i.e.: date of import). The finapiBookingDate will automatically get adjusted towards the bankBookingDate each time the associated bank account is updated. Example: A transaction is imported on July, 3rd, with a bank reported booking date of July, 6th. The transaction will be imported with its finapiBookingDate set to July, 3rd. Then, on July 4th, the associated account is updated. During this update, the transaction's finapiBookingDate will be automatically adjusted to July 4th. This adjustment of the finapiBookingDate takes place on each update until the bank account is updated on July 6th or later, in which case the transaction's finapiBookingDate will be adjusted to its final value, July 6th.<br/> The finapiBookingDate is the date that is used by the finAPI PFM services. E.g. when you calculate the spendings of an account for the current month, and have a transaction with finapiBookingDate in the current month but bankBookingDate at the beginning of the next month, then this transaction is included in the calculations (as the bank has this transaction's amount included in the current account balance as well).", alias="finapiBookingDate")
    amount: Union[StrictFloat, StrictInt] = Field(description="Transaction amount")
    currency: Optional[Currency] = Field(default=None, description="Transaction currency in ISO 4217 format.This field can be null if not explicitly provided the bank. In this case it can be assumed as account’s currency.<br/> <strong>Type:</strong> Currency")
    purpose: Optional[StrictStr] = Field(default=None, description="Transaction purpose. Maximum length: 2000")
    counterpart_name: Optional[StrictStr] = Field(default=None, description="Counterpart name. Maximum length: 80", alias="counterpartName")
    counterpart_account_number: Optional[StrictStr] = Field(default=None, description="Counterpart account number", alias="counterpartAccountNumber")
    counterpart_iban: Optional[StrictStr] = Field(default=None, description="Counterpart IBAN", alias="counterpartIban")
    counterpart_blz: Optional[StrictStr] = Field(default=None, description="Counterpart BLZ", alias="counterpartBlz")
    counterpart_bic: Optional[StrictStr] = Field(default=None, description="Counterpart BIC", alias="counterpartBic")
    counterpart_bank_name: Optional[StrictStr] = Field(default=None, description="Counterpart Bank name", alias="counterpartBankName")
    counterpart_mandate_reference: Optional[StrictStr] = Field(default=None, description="The mandate reference of the counterpart", alias="counterpartMandateReference")
    counterpart_customer_reference: Optional[StrictStr] = Field(default=None, description="The customer reference of the counterpart", alias="counterpartCustomerReference")
    counterpart_creditor_id: Optional[StrictStr] = Field(default=None, description="The creditor ID of the counterpart. Exists only for SEPA direct debit transactions (\"Lastschrift\").", alias="counterpartCreditorId")
    counterpart_debitor_id: Optional[StrictStr] = Field(default=None, description="The originator's identification code. Exists only for SEPA money transfer transactions (\"Überweisung\").", alias="counterpartDebitorId")
    type: Optional[StrictStr] = Field(default=None, description="Transaction type, according to the bank. If set, this will contain a term in the language of the bank, that you can display to the user. Some examples of common values are: \"Lastschrift\", \"Auslands&uuml;berweisung\", \"Geb&uuml;hren\", \"Zinsen\". The maximum possible length of this field is 255 characters.")
    type_code_zka: Optional[StrictStr] = Field(default=None, description="ZKA business transaction code which relates to the transaction's type. Possible values range from 1 through 999. If no information about the ZKA type code is available, then this field will be null.", alias="typeCodeZka")
    type_code_swift: Optional[StrictStr] = Field(default=None, description="SWIFT transaction type code. If no information about the SWIFT code is available, then this field will be null.", alias="typeCodeSwift")
    sepa_purpose_code: Optional[StrictStr] = Field(default=None, description="SEPA purpose code, according to ISO 20022", alias="sepaPurposeCode")
    bank_transaction_code: Optional[StrictStr] = Field(default=None, description="Bank transaction code, according to ISO 20022", alias="bankTransactionCode")
    bank_transaction_code_description: Optional[Annotated[str, Field(strict=True, max_length=256)]] = Field(default=None, description="Bank transaction code description, according to ISO 20022.<br/>The field is dynamic and can be initialized in different languages depending on the `Accept-Language` header provided within the request. Currently, only English and German are implemented, but this can get extended on demand.", alias="bankTransactionCodeDescription")
    primanota: Optional[StrictStr] = Field(default=None, description="Transaction primanota (bank side identification number)")
    category: Optional[Category] = Field(default=None, description="Transaction category, if any is assigned. Note: Recently imported transactions that have currently no category assigned might still get categorized by the background categorization process. To check the status of the background categorization, see GET /bankConnections. Manual category assignments to a transaction will remove the transaction from the background categorization process (i.e. the background categorization process will never overwrite a manual category assignment).<br/> <strong>Type:</strong> Category")
    labels: List[Label] = Field(description="Array of assigned labels<br/> <strong>Type:</strong> Label")
    is_potential_duplicate: StrictBool = Field(description="While finAPI uses a well-elaborated algorithm for uniquely identifying transactions, there is still the possibility that during an account update, a transaction that was imported previously may be imported a second time as a new transaction. For example, this can happen if some transaction data changes on the bank server side. However, finAPI also includes an algorithm of identifying such \"potential duplicate\" transactions. If this field is set to true, it means that finAPI detected a similar transaction that might actually be the same. It is recommended to communicate this information to the end user, and give him an option to delete the transaction in case he confirms that it really is a duplicate.", alias="isPotentialDuplicate")
    is_adjusting_entry: StrictBool = Field(description="Indicating whether this transaction is an adjusting entry ('Zwischensaldo').<br/><br/>Adjusting entries do not originate from the bank, but are added by finAPI during an account update when the bank reported account balance does not add up to the set of transactions that finAPI receives for the account. In this case, the adjusting entry will fix the deviation between the balance and the received transactions so that both adds up again.<br/><br/>Possible causes for such deviations are:<br/>- Inconsistencies in how the bank calculates the balance, for instance when not yet booked transactions are already included in the balance, but not included in the set of transactions<br/>- Gaps in the transaction history that finAPI receives, for instance because the account has not been updated for a while and older transactions are no longer available", alias="isAdjustingEntry")
    is_new: StrictBool = Field(description="Indicating whether this transaction is 'new' or not. Any newly imported transaction will have this flag initially set to true. How you use this field is up to your interpretation. For example, you might want to set it to false once a user has clicked on/seen the transaction. You can change this flag to 'false' with the PATCH method.", alias="isNew")
    import_date: datetime = Field(description="<strong>Format:</strong> 'YYYY-MM-DD'T'HH:MM:SS.SSSXXX' (RFC 3339, section 5.6)<br/>Date of transaction import.", alias="importDate")
    children: Optional[List[StrictInt]] = Field(default=None, description="Sub-transactions identifiers (if this transaction is split)")
    paypal_data: Optional[PaypalTransactionData] = Field(default=None, description="Additional, PayPal-specific transaction data.<br/> <strong>Type:</strong> PaypalTransactionData", alias="paypalData")
    certis_data: Optional[CertisTransactionData] = Field(default=None, description="Fields as defined by <a href='https://www.cnb.cz/en/payments/certis/' target='_blank'>CERTIS</a>.<br/> <strong>Type:</strong> CertisTransactionData", alias="certisData")
    end_to_end_reference: Optional[StrictStr] = Field(default=None, description="End-To-End reference", alias="endToEndReference")
    compensation_amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Compensation Amount. Sum of reimbursement of out-of-pocket expenses plus processing brokerage in case of a national return / refund debit as well as an optional interest equalisation. Exists predominantly for SEPA direct debit returns.", alias="compensationAmount")
    original_amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Original Amount of the original direct debit. Exists predominantly for SEPA direct debit returns.", alias="originalAmount")
    original_currency: Optional[Currency] = Field(default=None, description="Currency of the original amount in ISO 4217 format. This field can be null if not explicitly provided the bank. In this case it can be assumed as account’s currency.<br/> <strong>Type:</strong> Currency", alias="originalCurrency")
    fee_amount: Optional[Union[StrictFloat, StrictInt]] = Field(default=None, description="Amount of the transaction fee. Some banks charge a specific fee per transaction. Only returned by a few banks.", alias="feeAmount")
    fee_currency: Optional[Currency] = Field(default=None, description="Currency of the transaction fee in ISO 4217 format.<br/> <strong>Type:</strong> Currency", alias="feeCurrency")
    different_debitor: Optional[StrictStr] = Field(default=None, description="Payer's/debtor's reference party (in the case of a credit transfer) or payee's/creditor's reference party (in the case of a direct debit)", alias="differentDebitor")
    different_creditor: Optional[StrictStr] = Field(default=None, description="Payee's/creditor's reference party (in the case of a credit transfer) or payer's/debtor's reference party (in the case of a direct debit)", alias="differentCreditor")
    __properties: ClassVar[List[str]] = ["id", "parentId", "accountId", "valueDate", "bankBookingDate", "finapiBookingDate", "amount", "currency", "purpose", "counterpartName", "counterpartAccountNumber", "counterpartIban", "counterpartBlz", "counterpartBic", "counterpartBankName", "counterpartMandateReference", "counterpartCustomerReference", "counterpartCreditorId", "counterpartDebitorId", "type", "typeCodeZka", "typeCodeSwift", "sepaPurposeCode", "bankTransactionCode", "bankTransactionCodeDescription", "primanota", "category", "labels", "isPotentialDuplicate", "isAdjustingEntry", "isNew", "importDate", "children", "paypalData", "certisData", "endToEndReference", "compensationAmount", "originalAmount", "originalCurrency", "feeAmount", "feeCurrency", "differentDebitor", "differentCreditor"]

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
        """Create an instance of Transaction from a JSON string"""
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
        # override the default output from pydantic by calling `to_dict()` of category
        if self.category:
            _dict['category'] = self.category.to_dict()
        # override the default output from pydantic by calling `to_dict()` of each item in labels (list)
        _items = []
        if self.labels:
            for _item in self.labels:
                if _item:
                    _items.append(_item.to_dict())
            _dict['labels'] = _items
        # override the default output from pydantic by calling `to_dict()` of paypal_data
        if self.paypal_data:
            _dict['paypalData'] = self.paypal_data.to_dict()
        # override the default output from pydantic by calling `to_dict()` of certis_data
        if self.certis_data:
            _dict['certisData'] = self.certis_data.to_dict()
        return _dict

    @classmethod
    def from_dict(cls, obj: Optional[Dict[str, Any]]) -> Optional[Self]:
        """Create an instance of Transaction from a dict"""
        if obj is None:
            return None

        if not isinstance(obj, dict):
            return cls.model_validate(obj)

        _obj = cls.model_validate({
            "id": obj.get("id"),
            "parentId": obj.get("parentId"),
            "accountId": obj.get("accountId"),
            "valueDate": obj.get("valueDate"),
            "bankBookingDate": obj.get("bankBookingDate"),
            "finapiBookingDate": obj.get("finapiBookingDate"),
            "amount": obj.get("amount"),
            "currency": obj.get("currency"),
            "purpose": obj.get("purpose"),
            "counterpartName": obj.get("counterpartName"),
            "counterpartAccountNumber": obj.get("counterpartAccountNumber"),
            "counterpartIban": obj.get("counterpartIban"),
            "counterpartBlz": obj.get("counterpartBlz"),
            "counterpartBic": obj.get("counterpartBic"),
            "counterpartBankName": obj.get("counterpartBankName"),
            "counterpartMandateReference": obj.get("counterpartMandateReference"),
            "counterpartCustomerReference": obj.get("counterpartCustomerReference"),
            "counterpartCreditorId": obj.get("counterpartCreditorId"),
            "counterpartDebitorId": obj.get("counterpartDebitorId"),
            "type": obj.get("type"),
            "typeCodeZka": obj.get("typeCodeZka"),
            "typeCodeSwift": obj.get("typeCodeSwift"),
            "sepaPurposeCode": obj.get("sepaPurposeCode"),
            "bankTransactionCode": obj.get("bankTransactionCode"),
            "bankTransactionCodeDescription": obj.get("bankTransactionCodeDescription"),
            "primanota": obj.get("primanota"),
            "category": Category.from_dict(obj["category"]) if obj.get("category") is not None else None,
            "labels": [Label.from_dict(_item) for _item in obj["labels"]] if obj.get("labels") is not None else None,
            "isPotentialDuplicate": obj.get("isPotentialDuplicate"),
            "isAdjustingEntry": obj.get("isAdjustingEntry"),
            "isNew": obj.get("isNew"),
            "importDate": obj.get("importDate"),
            "children": obj.get("children"),
            "paypalData": PaypalTransactionData.from_dict(obj["paypalData"]) if obj.get("paypalData") is not None else None,
            "certisData": CertisTransactionData.from_dict(obj["certisData"]) if obj.get("certisData") is not None else None,
            "endToEndReference": obj.get("endToEndReference"),
            "compensationAmount": obj.get("compensationAmount"),
            "originalAmount": obj.get("originalAmount"),
            "originalCurrency": obj.get("originalCurrency"),
            "feeAmount": obj.get("feeAmount"),
            "feeCurrency": obj.get("feeCurrency"),
            "differentDebitor": obj.get("differentDebitor"),
            "differentCreditor": obj.get("differentCreditor")
        })
        return _obj


