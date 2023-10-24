

import boto3


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware



AWS_ACCESS_KEY_ID = 'AKIASAFP3RY6AJDLGRG6'
AWS_SECRET_ACCESS_KEY = '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'
AWS_REGION = 'us-east-1'  # Reemplaza con tu región us-east-1
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

#@app.get("/list/")
#async def list_files():
#    s3_client = boto3.client(
#        's3',
#        aws_access_key_id=AWS_ACCESS_KEY_ID,
#        aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
#        region_name=AWS_REGION
#    )
#
#    try:
#        response = s3_client.list_objects(Bucket=S3_BUCKET_NAME)
#        files = [obj['Key'] for obj in response.get('Contents', [])]
#        return JSONResponse(content={"files": files})
#    except Exception as e:
#        return JSONResponse(content={"error": str(e)}, status_code=500)


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
        objects = response.get('Contents', [])

        # Crear una lista con información detallada de cada objeto
        files = []

        for obj in objects:
            key = obj['Key']
            size = obj['Size']
            last_modified = obj['LastModified'].strftime("%Y-%m-%d %H:%M:%S")  # Formatea el objeto datetime como una cadena

            # Genera un enlace de descarga prefirmado
            s3_client = boto3.client(
                's3',
                aws_access_key_id=AWS_ACCESS_KEY_ID,
                aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                region_name=AWS_REGION
            )
            url = s3_client.generate_presigned_url('get_object', Params={'Bucket': S3_BUCKET_NAME, 'Key': key}, ExpiresIn=3600)

            files.append({
                'Key': key,
                'Size': size,
                'LastModified': last_modified,
                'DownloadLink': url  # Agrega el enlace de descarga como un cuarto atributo
            })

        return JSONResponse(content={"files": files})
    except Exception as e:
        return JSONResponse(content={"error": str(e)}, status_code=500)
