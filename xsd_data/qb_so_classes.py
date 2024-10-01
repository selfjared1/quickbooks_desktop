from dataclasses import dataclass, field
from typing import List, Optional


@dataclass
class SignonAppCertRqType:
    client_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientDateTime",
            "type": "Element",
            "required": True,
        },
    )
    application_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApplicationLogin",
            "type": "Element",
            "required": True,
        },
    )
    connection_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectionTicket",
            "type": "Element",
            "required": True,
        },
    )
    installation_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstallationID",
            "type": "Element",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "required": True,
        },
    )
    app_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppID",
            "type": "Element",
            "required": True,
        },
    )
    app_ver: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppVer",
            "type": "Element",
            "required": True,
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )


@dataclass
class SignonAppCertRsType:
    server_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServerDateTime",
            "type": "Element",
            "required": True,
        },
    )
    session_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "SessionTicket",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    status_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusCode",
            "type": "Attribute",
            "required": True,
        },
    )
    status_severity: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusSeverity",
            "type": "Attribute",
            "required": True,
        },
    )
    status_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusMessage",
            "type": "Attribute",
        },
    )


@dataclass
class SignonDesktopRqType:
    client_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientDateTime",
            "type": "Element",
            "required": True,
        },
    )
    application_login: Optional[str] = field(
        default=None,
        metadata={
            "name": "ApplicationLogin",
            "type": "Element",
            "required": True,
        },
    )
    connection_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "ConnectionTicket",
            "type": "Element",
            "required": True,
        },
    )
    installation_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstallationID",
            "type": "Element",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "required": True,
        },
    )
    app_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppID",
            "type": "Element",
            "required": True,
        },
    )
    app_ver: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppVer",
            "type": "Element",
            "required": True,
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )


@dataclass
class SignonDesktopRsType:
    server_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServerDateTime",
            "type": "Element",
            "required": True,
        },
    )
    session_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "SessionTicket",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    status_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusCode",
            "type": "Attribute",
            "required": True,
        },
    )
    status_severity: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusSeverity",
            "type": "Attribute",
            "required": True,
        },
    )
    status_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusMessage",
            "type": "Attribute",
        },
    )


@dataclass
class SignonTicketRqType:
    client_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ClientDateTime",
            "type": "Element",
            "required": True,
        },
    )
    session_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "SessionTicket",
            "type": "Element",
            "required": True,
        },
    )
    auth_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AuthID",
            "type": "Element",
        },
    )
    installation_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "InstallationID",
            "type": "Element",
        },
    )
    language: Optional[str] = field(
        default=None,
        metadata={
            "name": "Language",
            "type": "Element",
            "required": True,
        },
    )
    app_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppID",
            "type": "Element",
            "required": True,
        },
    )
    app_ver: Optional[str] = field(
        default=None,
        metadata={
            "name": "AppVer",
            "type": "Element",
            "required": True,
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )


@dataclass
class SignonTicketRsType:
    server_date_time: Optional[str] = field(
        default=None,
        metadata={
            "name": "ServerDateTime",
            "type": "Element",
            "required": True,
        },
    )
    session_ticket: Optional[str] = field(
        default=None,
        metadata={
            "name": "SessionTicket",
            "type": "Element",
        },
    )
    request_id: Optional[str] = field(
        default=None,
        metadata={
            "name": "requestID",
            "type": "Attribute",
        },
    )
    status_code: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusCode",
            "type": "Attribute",
            "required": True,
        },
    )
    status_severity: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusSeverity",
            "type": "Attribute",
            "required": True,
        },
    )
    status_message: Optional[str] = field(
        default=None,
        metadata={
            "name": "statusMessage",
            "type": "Attribute",
        },
    )


@dataclass
class SignonMsgsRq:
    signon_app_cert_rq: List[SignonAppCertRqType] = field(
        default_factory=list,
        metadata={
            "name": "SignonAppCertRq",
            "type": "Element",
        },
    )
    signon_desktop_rq: List[SignonDesktopRqType] = field(
        default_factory=list,
        metadata={
            "name": "SignonDesktopRq",
            "type": "Element",
        },
    )
    signon_ticket_rq: List[SignonTicketRqType] = field(
        default_factory=list,
        metadata={
            "name": "SignonTicketRq",
            "type": "Element",
        },
    )


@dataclass
class SignonMsgsRs:
    signon_app_cert_rs: List[SignonAppCertRsType] = field(
        default_factory=list,
        metadata={
            "name": "SignonAppCertRs",
            "type": "Element",
        },
    )
    signon_desktop_rs: List[SignonDesktopRsType] = field(
        default_factory=list,
        metadata={
            "name": "SignonDesktopRs",
            "type": "Element",
        },
    )
    signon_ticket_rs: List[SignonTicketRsType] = field(
        default_factory=list,
        metadata={
            "name": "SignonTicketRs",
            "type": "Element",
        },
    )
