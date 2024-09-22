from cleanunet import CleanUNet
import torchaudio, torch
import numpy as np
from denoiser.utils import chunk_audio, unchunk_audio

class DenoiserAudio():
    def __init__(self,
                 device = 'cuda' if torch.cuda.is_available() else 'cpu',
                 chunk_length_s = 2,
                 max_batch_size = 20) -> None:
        
        self.device = device
        self.chunk_length_s = chunk_length_s
        self.max_batch_size = max_batch_size
        self.model = CleanUNet.from_pretrained(device=device)
        
    @staticmethod
    def load_audio_and_resample(audio_path, target_sr = 16000):
        audio_wav, s_rate = torchaudio.load(audio_path)
        if s_rate is not target_sr:
            audio_wav = torchaudio.transforms.Resample(s_rate, new_freq=target_sr)(audio_wav)
        return audio_wav[0]
    
    @staticmethod
    def audio_processing(audio_wav):
        if isinstance(audio_wav, torch.Tensor):
            return np.trim_zeros(audio_wav.numpy())
        elif isinstance(audio_wav, np.ndarray):
            return np.trim_zeros(audio_wav)
        else:
            raise TypeError('Only supports numpy.ndarray or torch.Tensor file types.')
    
    def denoise(self, audio_chunks, max_batch_size = 20):
        num_chunks = audio_chunks.shape[0]
        batches = torch.split(audio_chunks, max_batch_size)
        
        denoised_audio = []
        for batch in batches:
            batch = batch.to(self.device)
            with torch.no_grad():
                batch_output = self.model(batch)
            batch_output, batch = batch_output.to('cpu'), batch.to('cpu')
            torch.cuda.empty_cache()
            denoised_audio.append(unchunk_audio(batch_output))
            
        denoised_audio = torch.cat(denoised_audio, dim=1)
        return denoised_audio
    
    def __call__(self, 
                 noisy_audio_path, 
                 target_sr = 16000,
                 trim_zeros = True):
        
        noisy_audio = DenoiserAudio.load_audio_and_resample(audio_path=noisy_audio_path,target_sr = target_sr)
        noisy_audio = DenoiserAudio.audio_processing(audio_wav = noisy_audio)

        audio_chunks = chunk_audio(audio_signal = noisy_audio, sampling_rate=target_sr, chunk_length_sec = self. chunk_length_s)
        
        denoised_audio = self.denoise(audio_chunks=audio_chunks, max_batch_size= self.max_batch_size)

        if trim_zeros:
            return DenoiserAudio.audio_processing(denoised_audio[0])
        else:
            return denoised_audio[0]