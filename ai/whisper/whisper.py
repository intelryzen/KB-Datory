from huggingface_hub import notebook_login
import torch
from pyannote.audio import Pipeline
from pyannote.core import Segment, Annotation, Timeline
import os
import librosa
import numpy as np
from faster_whisper import WhisperModel

hugging_face_token = "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"


def get_text_with_timestamp(segments):
    timestamp_texts = []
    for item in segments:
        last_start, last_end = -1, -1
        last_text = '-1'

        for word in item.words:
            start = word.start
            end = word.end
            text = word.word
            if (last_start == start) & (last_end == end) & (last_text == text):
                continue
            timestamp_texts.append((Segment(start, end), text))

            last_start = start
            last_end = end
            last_text = text
    return timestamp_texts


def add_speaker_info_to_text(timestamp_texts, ann):
    spk_text = []
    for seg, text in timestamp_texts:
        spk = ann.crop(seg).argmax()
        spk_text.append((seg, spk, text))
    return spk_text


def merge_cache(text_cache):
    sentence = ''.join([item[-1] for item in text_cache])
    spk = text_cache[0][1]
    start = text_cache[0][0].start
    end = text_cache[-1][0].end

    return Segment(start, end), spk, sentence


PUNC_SENT_END = ['.', '?', '!']


def merge_sentence(spk_text):
    merged_spk_text = []
    pre_spk = None
    text_cache = []
    for seg, spk, text in spk_text:
        if spk != pre_spk and pre_spk is not None and len(text_cache) > 0:
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = [(seg, spk, text)]
            pre_spk = spk

        elif text[-1] in PUNC_SENT_END:
            text_cache.append((seg, spk, text))
            if (text_cache[-1][0].end - text_cache[0][0].start) < 0.5:
                continue
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
            pre_spk = spk
        else:
            text_cache.append((seg, spk, text))
            pre_spk = spk
    if len(text_cache) > 0:
        merged_spk_text.append(merge_cache(text_cache))
    return merged_spk_text


def diarize_text(segments, diarization_result):
    timestamp_texts = get_text_with_timestamp(segments)
    print("test22")

    spk_text = add_speaker_info_to_text(timestamp_texts, diarization_result)
    print("test23")

    res_processed = merge_sentence(spk_text)
    return res_processed


def write_to_txt(spk_sent, file):
    with open(file, 'w') as fp:
        for seg, spk, sentence in spk_sent:
            line = f'{seg.start:.2f} {seg.end:.2f} {spk} {sentence}\n'
            fp.write(line)


class Whisper_Diarization:
    def __init__(self, model_name, device="cuda"):
        self.model = WhisperModel(model_name, device=device)
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                                 use_auth_token=True).to(torch.device(device))

    def transcribe(self, file_path):
        segments, _ = self.model.transcribe(
            file_path, beam_size=1, language='ko', word_timestamps=True)
        diarization_result = self.pipeline(
            file_path, min_speakers=1, max_speakers=2)

        final_result = diarize_text(segments, diarization_result)
        print('------ transcribe results ------')
        for seg, spk, sent in final_result:
            line = f'{seg.start:.2f} -> {seg.end:.2f} {spk}: {sent}'
            print(line)


class Whisper_Diarization:
    def __init__(self, model_name, device="cuda"):
        self.model = WhisperModel(model_name, device=device)
        self.pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization",
                                                 use_auth_token=hugging_face_token)  # .to(torch.device(device))

    def transcribe(self, file_path):
        print("test")

        segments, _ = self.model.transcribe(
            file_path, beam_size=1, language='ko', word_timestamps=True)
        print("test2")

        diarization_result = self.pipeline(
            file_path, min_speakers=1, max_speakers=2)
        print("test3")

        final_result = diarize_text(segments, diarization_result)

        print("test4")

        print('------ transcribe results ------')
        for seg, spk, sent in final_result:
            line = f'{seg.start:.2f} -> {seg.end:.2f} {spk}: {sent}'
            print(line)
        print("test5")
