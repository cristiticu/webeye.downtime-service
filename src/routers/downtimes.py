from typing import Annotated
from fastapi import APIRouter, Depends

from auth.dependencies import user_token_data
from auth.model import UserTokenData
from context import ApplicationContext


router = APIRouter(prefix="/downtime", tags=["downtimes"])
application_context = ApplicationContext()


@router.get("/{check_type}")
def list_downtimes(check_type: str, url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    downtimes = application_context.downtimes.get_downtimes(
        token.user_guid, url, check_type)
    return downtimes


@router.get("/events/{check_type}")
def list_events(check_type: str, url: str, start_date: str, end_date: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    events = application_context.downtimes.get_events(
        token.user_guid, url, check_type, start_date, end_date)
    return events


@router.get("/status/{check_type}")
def get_current_status(check_type: str, url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    status = application_context.downtimes.get_current_status_or_create(
        token.user_guid, url, check_type)
    return status


@router.post("/http")
def run_http_check(url: str, token: Annotated[UserTokenData, Depends(user_token_data)]):
    response = application_context.downtimes.run_http_uptime(
        token.user_guid, url)
    return response


# @router.get("events/{check_type}/{url:path}")
# def list_events()
