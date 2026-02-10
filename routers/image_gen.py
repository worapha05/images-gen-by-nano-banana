from fastapi import APIRouter, UploadFile, File, Form, Request, status
from fastapi.responses import JSONResponse
from typing import List
import os
import uuid
import os
from services import ImageGenService, ImageGenServiceError
# from dotenv import load_dotenv

router = APIRouter()

@router.post("/images-gen")
async def upload(
    request: Request,  
    files: List[UploadFile] = File(default=[]),
    prompt: str = Form(default=None),
    aspect_ratio: str = Form(default=None),
    resolution: str = Form(default=None)):

    # load_dotenv()
    api_key = os.getenv("GEMINI_API_IMAGE_KEY")
    image_gen_service = ImageGenService(api_key=api_key)

    api_version = request.headers.get("x-api-version", None)
    correlation_id = request.headers.get("x-correlation-id", None)

    if correlation_id is None:
        correlation_id = f"corr_{uuid.uuid4()}"    
    
    headers = {
        "x-correlation-id": correlation_id
    }

    if api_version != "1":
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            headers=headers,
            content={
                    "code": "INVALID_FIELD_VALUE", 
                    "message": f"Unsupported X-API-Version: {api_version}",
                    "correlationId": correlation_id
                },
        )

    headers = {
        "x-correlation-id": correlation_id,
        "x-api-version": api_version
    }

    valid_files = []
    try:
        for file in files:
            if image_gen_service.is_valid_image_type(file.content_type):
                valid_files.append(file)
            else:
                raise ImageGenServiceError(
                    f"Invalid content type: {file.content_type} not supported. allowed types are image/jpeg, image/png",
                    code="INVALID_CONTENT_TYPE"
                )

    except ImageGenServiceError as e:
        return JSONResponse(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            headers=headers,
            content={
                "code": e.code, 
                "message": e.message,
                "correlationId": correlation_id
            },
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=headers,
            content={
                "code": "INTERNAL_ERROR", 
                "message": f"Internal server error: {str(e)}",
                "correlationId": correlation_id
            },
        )

    try:
        files_bytes = await image_gen_service.convert_files_to_bytes(files=valid_files)
        
        final_prompt = image_gen_service.create_prompt(
            prompt=prompt,
            files=valid_files
        )

        generated_image = image_gen_service.generate_image(
            files_bytes=files_bytes,
            prompt=final_prompt,
            aspect_ratio=aspect_ratio,
            resolution=resolution
        )

        contents = {
            "code": "SUCCESS",
            "message": "Image generated successfully",
            "correlationId": correlation_id,
            "image": generated_image.get("image"),
            "size": generated_image.get("size"),
        }

        return JSONResponse(content=contents, headers=headers)
    
    except ImageGenServiceError as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=headers,
            content={
                "code": e.code, 
                "message": e.message,
                "correlationId": correlation_id
            },
        )
    
    except Exception as e:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            headers=headers,
            content={
                "code": "INTERNAL_ERROR", 
                "message": f"Internal server error: {str(e)}",
                "correlationId": correlation_id
            },
        )