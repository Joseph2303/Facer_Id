from typing import Annotated
import datetime
import uvicorn
import ReconocimientoFacial
from fastapi import FastAPI, File, UploadFile
from datetime import UTC
import pytz

app = FastAPI()


@app.post("/files/")
async def create_file(file: Annotated[bytes, File(description="A file read as bytes")]):
    return {"file_size": len(file)}


@app.post("/uploadfile/")
async def create_upload_file(
    file: Annotated[UploadFile, File(description="A file read as UploadFile")],
):
    try: 
        file_path = f"{file.filename}"
        with open(file_path, "wb") as f:
            f.write(file.file.read())
        
        empleado = ReconocimientoFacial.detectFace(file.filename)
        cr_timezone = pytz.timezone('America/Costa_Rica')
        if empleado is not "desconocido":
            return {"message": f"Marca de {empleado} en {datetime.datetime.now(cr_timezone)}"}
        return {"message": f"Desconocido"}
    except Exception as e:
        return {"message": e.args}
    
    
uvicorn.run(app)