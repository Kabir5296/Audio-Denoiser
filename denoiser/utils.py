import torch, numpy, torchaudio

def chunk_audio(audio_signal: numpy.ndarray, 
                sampling_rate: int, 
                chunk_length_sec: int = 3) -> torch.Tensor:
    '''
    Creates a chunk of audios from a long audio file. Converts from torch.tensor to numpy.ndarray.
    '''
    
    samples_per_chunk = int(sampling_rate * chunk_length_sec)
    num_chunks = len(audio_signal) // samples_per_chunk
    truncated_signal = audio_signal[:num_chunks * samples_per_chunk]
    chunks = truncated_signal.reshape(num_chunks, samples_per_chunk)
    chunks_tensor = torch.from_numpy(chunks).float()
    return chunks_tensor

def unchunk_audio(chunked_audio: torch.Tensor, 
                  overlap: int = 0) -> torch.Tensor:
    '''
    Combines a batch of audio chunks into one single audio file. Converts from numpy.ndarray to torch.tensor.
    '''
    
    if chunked_audio.dim() != 3 or chunked_audio.shape[1] != 1:
        raise ValueError("Input must be a 3D tensor with shape (num_chunks, 1, chunk_length)")
    
    num_chunks, _, chunk_length = chunked_audio.shape
    if overlap >= chunk_length:
        raise ValueError("Overlap must be less than chunk length")
    
    output_length = (num_chunks - 1) * (chunk_length - overlap) + chunk_length
    output = torch.zeros(1, output_length, device=chunked_audio.device)
    
    for i in range(num_chunks):
        start = i * (chunk_length - overlap)
        end = start + chunk_length
        output[0, start:end] += chunked_audio[i, 0, :]
    
    if overlap > 0:
        taper = torch.linspace(0, 1, overlap, device=chunked_audio.device)
        for i in range(1, num_chunks):
            start = i * (chunk_length - overlap)
            output[0, start:start+overlap] *= taper
            output[0, start-overlap:start] *= (1 - taper)
    
    return output