

import boto3


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



AWS_ACCESS_KEY_ID = 'AKIASAFP3RY6AJDLGRG6'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'N/A'  # Reemplaza con tu región us-east-1
S3_BUCKET_NAME = 'jesusmorabucket'

from fastapi import FastAPI, UploadFile, File
from fastapi.responses import JSONResponse
import os


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload/")
async def upload_file(file: UploadFile):
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        with file.file as f:
            s3_client.upload_fileobj(f, S3_BUCKET_NAME, file.filename)
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

    return JSONResponse(content={"message": "Archivo cargado exitosamente"})

@app.get("/list/")
async def list_files():
    s3_client = boto3.client(
        's3',
        aws_access_key_id=AWS_ACCESS_KEY_ID,
        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
        region_name=AWS_REGION
    )

    try:
        response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)
        files = [obj['Key'] for obj in response.get('Contents', [])]
        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)

