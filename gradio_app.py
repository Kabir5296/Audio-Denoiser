import gradio as gr
import os
import shutil, torch, torchaudio
from denoiser import DenoiserAudio

denoise = DenoiserAudio(device='cuda' if torch.cuda.is_available() else 'cpu', chunk_length_s=3, max_batch_size=20)

def process_audio(audio):
    global created_files
    if audio is None:
        return None, "No audio file uploaded."
    
    os.makedirs("Temp", exist_ok=True)
    original_filename = os.path.basename(audio)
    
    original_filepath = os.path.join("Temp", original_filename)
    denoised_filepath = os.path.join("Temp", f"denoised_{original_filename}")
    
    shutil.copy(audio, original_filepath)
    
    denoised_audio = denoise(original_filepath)
    torchaudio.save(denoised_filepath, torch.from_numpy(denoised_audio).unsqueeze(0), 16000)
    os.remove(original_filepath)
    
    return denoised_filepath

custom_css = """
    .gradio-container {
        background-color: #E6F3FF;
    }
"""

title = """ <center>
        <p style="font-size: 275%; font-weight: bold;"> Audio Denoiser - NVIDIA's CleanUNet Based </p>
        </center>
        """
        
with gr.Blocks(css = custom_css) as demo:
    gr.Markdown(title)
    
    with gr.Row(variant="compact"):
        audio_input = gr.Audio(type="filepath", label="Upload Audio")
        audio_output = gr.Audio(label="Denoised Audio", show_download_button=True)
        
    with gr.Row():
        process_button = gr.Button("Denoise Audio", variant="secondary")
    
    process_button.click(
        fn=process_audio,
        inputs=audio_input,
        outputs=[audio_output]
    )
    
    description = """
    <center>
    <p style="font-size: 150%; font-weight: bold;"> Developed by,</p> \n
    <p style="font-size: 150%; font-weight: bold;"> <a href="https://mahfuzulkabir.com">A F M Mahfuzul Kabir</a> </p> \n
    <p style="font-size: 150%; font-weight: bold;"> Please give it a star in the <a href="https://github.com/Kabir5296/Speech-Denoiser-System">GitHub repo</a> if you find it useful.</p>
    </center>
    """
    
    gr.Markdown(description)

    demo.load(lambda: None)
    
demo.launch(server_name="0.0.0.0", server_port=7862)