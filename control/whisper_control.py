import torch
from ai.whisper.whisper import *
from pyannote.audio import Pipeline
from faster_whisper import WhisperModel
from mysql.manager.file_manager import FileManager

hugging_face_token = "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"


class WhisperController:

    @staticmethod
    def stt(last_position, file_id, file_path):
        model_name = "ai_model"
        # file_path = "file/minimum.wav"

        whisper_model = WhisperDiarization(
            last_position=last_position,
            file_id=file_id,
            model_name=model_name, device="cuda")

        whisper_model.transcribe(file_path)


class WhisperDiarization:
    def __init__(self, last_position, file_id, model_name, device="cuda"):
        self.last_position = last_position
        self.file_id = file_id
        self.model = WhisperModel(model_name, device=device)
        self.pipeline = Pipeline.from_pretrained(
            "pyannote/speaker-diarization", use_auth_token=hugging_face_token).to(torch.device(device))

    def transcribe(self, file_path):

        segments, _ = self.model.transcribe(
            file_path, beam_size=1, language='ko', word_timestamps=True)

        diarization_result = self.pipeline(
            file_path, min_speakers=1, max_speakers=2)

        final_result = diarize_text(segments, diarization_result)

        print('------ transcribe results ------')
        count = 0
        for seg, spk, sent in final_result:
            count += 1
            # line = f'{seg.start:.2f} -> {seg.end:.2f} {spk}: {sent}'
            # print(line)
            if count < len(final_result):
                speaker = 0
                if spk is None or "1" in spk:
                    speaker = 1
                data = dict(start=self.last_position + round(seg.start * 1000),
                            end=self.last_position + round(seg.end * 1000), speaker=speaker, text=sent)
                FileManager.insert_stt(file_id=self.file_id, data=data)
