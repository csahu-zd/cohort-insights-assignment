from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, Response, status

from app.api.dependencies import current_user
from app.db.mongodb import get_document_collection
from app.schemas.documents import (
    CreateDocument,
    CreateDocumentResponse,
    DocumentStatus,
    ListDocumentResponse,
    UpdateDocument,
)
from app.services.documents import (
    create_document_service,
    get_document_by_client_doc_ref,
    get_document_by_doc_id,
    get_document_service,
    update_document_content,
)

router = APIRouter(tags=["documents"])


@router.post(
    "/documents",
    response_model=CreateDocumentResponse,
    status_code=status.HTTP_201_CREATED,
    responses={
        200: {"description": "Repeat submission of the same client_doc_ref and content"},
        409: {"description": "client_doc_ref already used with different content"},
        429: {"description": "Too many documents in progress"},
    },
)
async def create_document(
    request: CreateDocument,
    response: Response,
    caller: str = Depends(current_user),
    collection=Depends(get_document_collection),
):
    result, created = await create_document_service(request, caller, collection)
    if not created:
        response.status_code = status.HTTP_200_OK
    return result


@router.get("/users/{user_id}/documents", response_model=list[ListDocumentResponse])
async def get_document(
    user_id: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    status_filter: Optional[DocumentStatus] = Query(None, alias="status"),
    caller: str = Depends(current_user),
    collection=Depends(get_document_collection),
):
    if user_id != caller:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return await get_document_service(user_id, collection, page, page_size, status_filter)


@router.get(
    "/documents/by-ref/{client_doc_ref}",
    response_model=ListDocumentResponse,
    responses={404: {"description": "Document not found"}},
)
async def get_document_by_client_ref(
    client_doc_ref: str,
    caller: str = Depends(current_user),
    collection=Depends(get_document_collection),
):
    return await get_document_by_client_doc_ref(client_doc_ref, caller, collection)


@router.get(
    "/documents/{document_id}",
    response_model=ListDocumentResponse,
    responses={404: {"description": "Document not found"}},
)
async def get_document_by_document_id(
    document_id: str,
    caller: str = Depends(current_user),
    collection=Depends(get_document_collection),
):
    return await get_document_by_doc_id(document_id, caller, collection)


@router.patch(
    "/documents/{document_id}",
    response_model=ListDocumentResponse,
    responses={404: {"description": "Document not found"}, 409: {"description": "Version conflict"}},
)
async def update_document(
    document_id: str,
    request: UpdateDocument,
    caller: str = Depends(current_user),
    collection=Depends(get_document_collection),
):
    return await update_document_content(document_id, request, caller, collection)
