
import uuid
from decimal import Decimal
from datetime import datetime
from typing import Literal, Optional, get_args
from sqlalchemy import Column
from sqlalchemy.ext.mutable import MutableDict
from sqlmodel import SQLModel, Field, Relationship, JSON, Enum

UUIDField  = lambda **kwargs: Field(default_factory=uuid.uuid4, primary_key=True, **kwargs)
IndexField = lambda **kwargs: Field(index=True, **kwargs)
JSONField  = lambda **kwargs: Field(sa_column=Column(MutableDict.as_mutable(JSON)), **kwargs)
EnumField  = lambda args, **kwargs: Field(sa_column=Column(Enum(*get_args(args))))

MerchantIdField        = lambda **kwargs: Field(foreign_key="merchants.merchant_id", **kwargs)
PaymentProviderIdField = lambda **kwargs: Field(foreign_key="payment_providers.provider_id", **kwargs)
TransactionIdField     = lambda **kwargs: Field(foreign_key="transactions.transaction_id", **kwargs)

TransactionStatus = Literal['PENDING', 'CLOSED', 'SUCCESS', 'FAILED']
EndpointDirection = Literal['REQUEST', 'RESPONSE']
WebhookDirection  = Literal['INBOUND', 'OUTBOUND']

get_timestamp = lambda: datetime.now()

class Merchant(SQLModel, table=True):
    __tablename__ = "merchants"

    merchant_id  : uuid.UUID     = UUIDField()
    mercant_name : str           = IndexField(unique=True)
    created_at   : datetime      = IndexField()
    username     : str           = IndexField(unique=True)
    password     : str           = Field(max_length=256)
    email        : Optional[str] = None

class PaymentProvider(SQLModel, table=True):
    __tablename__ = "payment_providers"

    provider_id : str  = UUIDField()
    name        : str  = IndexField()
    base_url    : str  = Field(max_length=256)
    api_key     : dict = JSONField()

class MerchantsProviderDetails(SQLModel, table=True):
    __tablename__ = "merchant_provider_details"

    merchant_id         : uuid.UUID = MerchantIdField(primary_key = True)
    payment_provider_id : uuid.UUID = PaymentProviderIdField(primary_key = True)
    details             : dict      = JSONField()

    merchant         : Optional[Merchant]        = Relationship(back_populates="merchant_provider_details")
    payment_provider : Optional[PaymentProvider] = Relationship(back_populates="merchant_provider_details")

class Transaction(SQLModel, table=True):
    __tablename__ = "transactions"

    transaction_id      : str               = Field(primary_key=True)
    merchant_id         : uuid.UUID         = MerchantIdField()
    payment_provider_id : uuid.UUID         = PaymentProviderIdField()
    amount              : Decimal           = Field()
    currency            : str               = Field(max_length=5)
    status              : TransactionStatus = EnumField(TransactionStatus)
    created_at          : datetime          = Field(default_factory=get_timestamp)
    updated_at          : datetime          = Field(default_factory=get_timestamp)

    merchant         : Optional[Merchant]        = Relationship(back_populates="transactions")
    payment_provider : Optional[PaymentProvider] = Relationship(back_populates="transactions")
    api_logs         : Optional[list["APILogs"]] = Relationship(back_populates="transactions")

class APILogs(SQLModel, table=True):
    __tablename__ = "api_logs"

    log_id         : uuid.UUID         = MerchantIdField(primary_key = True)
    transaction_id : str               = TransactionIdField()
    direction      : EndpointDirection = EnumField(EndpointDirection)
    endpoint       : str               = Field(max_length=256)
    headers        : dict              = JSONField()
    payload        : dict              = JSONField()
    status_code    : Optional[int]     = None
    timestamp      : datetime          = Field(default_factory=get_timestamp)

    transaction : Optional[Transaction] = Relationship(back_populates="api_logs")

class Webhooks(SQLModel, table=True):
    __tablename__ = "webhooks"

    log_id         : uuid.UUID        = MerchantIdField(primary_key = True)
    transaction_id : str              = TransactionIdField()
    direction      : WebhookDirection = EnumField(WebhookDirection)
    endpoint       : str              = Field(max_length=256)
    headers        : dict             = JSONField()
    payload        : dict             = JSONField()
    status_code    : Optional[int]    = None
    timestamp      : datetime         = Field(default_factory=get_timestamp)

    transaction : Optional[Transaction] = Relationship(back_populates="api_logs")
