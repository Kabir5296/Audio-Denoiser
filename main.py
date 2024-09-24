from denoiser import DenoiserAudio
import os, shutil
from fastapi.responses import FileResponse
from fastapi import FastAPI, UploadFile, File, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
import uvicorn, torchaudio
import torch

denoise = DenoiserAudio(device='cuda' if torch.cuda.is_available() else 'cpu', chunk_length_s=3, max_batch_size=20)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/")
def read_root():
    return {
        "status": 200,
        "message": "Welcome to Speech Denoiser Module. Module developed by, Mahfuzul Kabir, MIS-MLE, ACI Limited"
    }

@app.post("/denoise/")
async def create_denoised_file(file: UploadFile = File(...)):
    
    temp_file_name = os.path.join('Temp',f"temp_{file.filename}")
    output_filename = os.path.join('Temp',f"denoised_{file.filename}")

    with open(temp_file_name, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    denoised_audio = denoise(temp_file_name)
    
    # Temporary save
    torchaudio.save(output_filename, torch.from_numpy(denoised_audio).unsqueeze(0), 16000)
    
    # Clean
    os.remove(temp_file_name)
    
    # return
    return FileResponse(output_filename, media_type="audio/wav", filename=output_filename)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8877)