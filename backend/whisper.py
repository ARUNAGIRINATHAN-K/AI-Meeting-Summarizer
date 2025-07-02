from transformers import WhisperProcessor, WhisperForConditionalGeneration
import librosa
import soundfile as sf

def transcribe_audio(file_path):
    # Load Whisper model and processor
    processor = WhisperProcessor.from_pretrained("openai/whisper-base")
    model = WhisperForConditionalGeneration.from_pretrained("openai/whisper-base")
    
    # Load audio file
    audio, sr = librosa.load(file_path, sr=16000)  # Whisper expects 16kHz
    input_features = processor(audio, sampling_rate=16000, return_tensors="pt").input_features

    # Generate transcription
    predicted_ids = model.generate(input_features)
    transcription = processor.batch_decode(predicted_ids, skip_special_tokens=True)[0]
    return transcription