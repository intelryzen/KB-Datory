from ai.whisper.whisper import Whisper_Diarization


class WhisperController:

    @staticmethod
    def stt(file_path):
        model_name = "ai_model"
        file_path = "temp-test.wav"

        print("tes")

        whisper_model = Whisper_Diarization(
            model_name=model_name, device="cpu")
        print("tes2")

        whisper_model.transcribe(file_path)
        print("test6")
