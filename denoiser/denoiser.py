from cleanunet import CleanUNet
import torchaudio, torch
import numpy as np
from typing import Union
from denoiser.utils import chunk_audio, unchunk_audio
from tqdm import tqdm

class DenoiserAudio():
    """
    Denoiser module.
    
    Args:
        device (str, Optional): Device to use. Defaults to GPU if available.
        chunk_length_s (int, Optional): Length of a single chunk in second.
        max_batch_size (int, Optional): Maximum size of a batch to infer in one instance.
    """
    
    def __init__(self,
                 device : str = 'cuda' if torch.cuda.is_available() else 'cpu',
                 chunk_length_s : int = 2,
                 max_batch_size : int = 20) -> None:
        
        self.device = device
        self.chunk_length_s = chunk_length_s
        self.max_batch_size = max_batch_size
        self.model = CleanUNet.from_pretrained(device=device)
        
    @staticmethod
    def load_audio_and_resample(audio_path : str, target_sr : int = 16000) -> torch.Tensor:
        """
        Loads audio and resamples to target sampling rate. Returns single channel.

        Args:
            audio_path (str): Path to audio file.
            target_sr (int, optional): Target sampling rate. Defaults to 16000.

        Returns:
            torch.Tensor: Tensor of audio file, returns single channel only.
        """
        audio_wav, s_rate = torchaudio.load(audio_path)
        if s_rate is not target_sr:
            audio_wav = torchaudio.transforms.Resample(s_rate, new_freq=target_sr)(audio_wav)
        return audio_wav[0]
    
    @staticmethod
    def audio_processing(audio_wav : Union[torch.Tensor, np.ndarray]) -> np.ndarray:
        """
        Process audio. Trims all zero.

        Args:
            audio_wav (torch.Tensor | np.ndarray): Audio wave loaded.

        Raises:
            TypeError: If file is not a Tensor or an Array.

        Returns:
            np.ndarray: Zero trimmed audio array. In future, vad will be used.
        """
        if isinstance(audio_wav, torch.Tensor):
            return np.trim_zeros(audio_wav.numpy())
        elif isinstance(audio_wav, np.ndarray):
            return np.trim_zeros(audio_wav)
        else:
            raise TypeError('Only supports numpy.ndarray or torch.Tensor file types.')
    
    def denoise(self, audio_chunks: torch.Tensor, max_batch_size: int = 20) -> torch.Tensor:
        """
        Denoises noisy audio chunks.

        Args:
            audio_chunks (torch.Tensor): Tensor of all noisy audio chunks.
            max_batch_size (int, optional): Same as for model initialization. Defaults to 20.

        Returns:
            torch.Tensor: Denoised audio tensors.
        """
        num_chunks = audio_chunks.shape[0]
        batches = torch.split(audio_chunks, max_batch_size)
        
        print("*"*20)
        print(f"Total number of chunks is {num_chunks}")
        print(f"Running system on {len(batches)} batches with each batch containing {max_batch_size} chunks")
        print("*"*20)
        
        denoised_audio = []
        for batch in tqdm(batches):
            batch = batch.to(self.device)
            with torch.no_grad():
                batch_output = self.model(batch)
            batch_output, batch = batch_output.to('cpu'), batch.to('cpu')
            torch.cuda.empty_cache()
            denoised_audio.append(unchunk_audio(batch_output))
            
        denoised_audio = torch.cat(denoised_audio, dim=1)
        return denoised_audio
    
    def __call__(self, 
                 noisy_audio_path: str,
                 target_sr: int = 16000) -> np.ndarray:
        """
        Denoises a given audio. Loads the audio, trims zeros, creates chunks and uses batching mechanism for less computation expense. The denoised audio waveform is returned.

        Args:
            noisy_audio_path (str): Path to the audio file.
            target_sr (int, optional): Target sampling rate. Defaults to 16000.

        Returns:
            np.ndarray: Denoised audio waveform. Single channel.
        """
        
        noisy_audio = DenoiserAudio.load_audio_and_resample(audio_path=noisy_audio_path,target_sr = target_sr)
        noisy_audio = DenoiserAudio.audio_processing(audio_wav = noisy_audio)

        audio_chunks = chunk_audio(audio_signal = noisy_audio, sampling_rate=target_sr, chunk_length_sec = self. chunk_length_s)
        
        denoised_audio = self.denoise(audio_chunks=audio_chunks, max_batch_size= self.max_batch_size)

        return DenoiserAudio.audio_processing(denoised_audio[0])