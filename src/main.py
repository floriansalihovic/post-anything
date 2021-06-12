from typing import Optional

from fastapi import FastAPI, HTTPException, status
from fastapi.encoders import jsonable_encoder
from lib import (
    create_or_update,
    find_in_collection_by,
    new_mongo_client,
    remove_document,
)
from starlette.responses import JSONResponse, Response

mongo_client = new_mongo_client()
api = FastAPI()


def document_filter(resource_path: str = "") -> dict:
    return {"resource_path": resource_path}


def create_or_update_resource(
    resource_path: str, document_data: dict, response: Response
) -> dict:
    document, created = create_or_update(
        mongo_client,
        document_filter(resource_path),
        document_data,
    )
    response.status_code = 201 if created else 200
    return document


@api.get("/{resource_path:path}")
async def read(resource_path: str):
    document: Optional[dict] = find_in_collection_by(
        mongo_client,
        document_filter(resource_path),
    )
    if document is None:
        raise HTTPException(status_code=404, detail="Resource not found")
    return document


@api.post("/{resource_path:path}", status_code=status.HTTP_201_CREATED)
async def create(resource_path: str, document_body: dict, response: Response):
    return create_or_update_resource(resource_path, document_body, response)


@api.put("/{resource_path:path}", status_code=status.HTTP_200_OK)
async def update(resource_path: str, document_body: dict, response: Response):
    return create_or_update_resource(resource_path, document_body, response)


@api.delete("/{resource_path:path}")
async def delete(resource_path: str) -> Response:
    document, document_deleted = remove_document(
        mongo_client, document_filter(resource_path)
    )
    return (
        Response(status_code=status.HTTP_204_NO_CONTENT)
        if document is None
        else JSONResponse(content=jsonable_encoder(document))
    )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:api", host="0.0.0.0", port=8000, debug=True)
