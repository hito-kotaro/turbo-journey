from fastapi import Depends
from routes import router_base as rb
import schema.line_schema as line_sc
from cruds.auth import get_current_user
import libs.line as line

router = rb.create_router("line")


@router.post("/request", responseModel=line_sc.ResponseCode)
def post_request_api(
    params: line_sc.PostRequestTitle,
    current_user: str = Depends(get_current_user),
):
    return line.post_request(
        subject=current_user.name, request_title=params.request_title
    )


@router.post("/complete", responseModel=line_sc.ResponseCode)
def post_complete_api(
    params: line_sc.PostComplete,
    current_user: str = Depends(get_current_user),
):
    return line.post_complete(
        subject=current_user.name,
        request_title=params.request_title,
        owner=params.owner,
    )


@router.post("/approve", responseModel=line_sc.ResponseCode)
def post_approve_api(
    params: line_sc.PostRequestTitle,
    current_user: str = Depends(get_current_user),
):
    return line.post_complete(
        subject=current_user.name,
        request_title=params.request_title,
    )
