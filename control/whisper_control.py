from pyannote.audio import Audio
from sklearn.cluster import AgglomerativeClustering
from faster_whisper import WhisperModel
from pyannote.core import Segment
import numpy as np
import torch
import time
import kss
from mysql.manager.file_manager import FileManager
from pyannote.audio.pipelines.speaker_verification import PretrainedSpeakerEmbedding


hugging_face_token = "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"
embedding_model = PretrainedSpeakerEmbedding(
    "speechbrain/spkrec-ecapa-voxceleb",
    device=torch.device("cuda"))
audio = Audio()
PUNC_SENT_END = ['.', '?', '!']


def get_text_with_timestamp(segments, start_sec):
    timestamp_texts = []
    for item in segments:
        for word in item.words:
            start = word.start + start_sec
            end = word.end + start_sec
            text = word.word
            timestamp_texts.append((Segment(start, end), text))

    return timestamp_texts


def merge_cache(text_cache):
    sentence = ''.join([item[-1] for item in text_cache])
    start = text_cache[0][0].start
    end = text_cache[-1][0].end
    return {'start': start, 'text': sentence, 'end': end}


def merge_sentence(spk_text):
    merged_spk_text = []
    text_cache = []
    for seg, text in spk_text:
        if text[-1] in PUNC_SENT_END:
            text_cache.append((seg, text))
            merged_spk_text.append(merge_cache(text_cache))
            text_cache = []
        else:
            text_cache.append((seg, text))
            sentence_lst = kss.split_sentences(merge_cache(text_cache)['text'])
            if len(sentence_lst) >= 2:
                merged_spk_text.append(merge_cache(text_cache[:-1]))
                text_cache = [text_cache[-1]]
    if len(text_cache) > 0:
        merged_spk_text.append(merge_cache(text_cache))
    return merged_spk_text


def diarize_text(segments, start_sec):
    timestamp_texts = get_text_with_timestamp(segments, start_sec)
    res_processed = merge_sentence(timestamp_texts)
    return res_processed


def segment_embedding(segment, path):
    start = segment["start"]
    # Whisper overshoots the end timestamp in the last segment
    end = segment["end"]
    clip = Segment(start, end)
    waveform, sample_rate = audio.crop(path, clip)
    return embedding_model(waveform[None])


def return_lst(segments, start_sec=0):
    start = time.time()
    seg_list = diarize_text(segments, start_sec)
    return seg_list


def get_embeddings(seg_list, embeddings, path):
    for i, segment in enumerate(seg_list):
        embeddings[i] = segment_embedding(segment, path)
    embeddings = np.nan_to_num(embeddings).reshape(-1, 1)
    return embeddings


def return_spk_lst(seg_list, embeddings):
    clustering = AgglomerativeClustering(2).fit(embeddings)
    labels = clustering.labels_
    for i in range(len(seg_list)):
        seg_list[i]["speaker"] = 'SPEAKER ' + str(labels[i] + 1)
        if seg_list[i]["speaker"] == seg_list[i]["speaker"]:
            seg_list[i]["speaker"]

    return seg_list, embeddings


class WhisperDiarization:

    model = WhisperModel(
        r"C:\Users\jhkim\VoicePhising\KB-Datory\ai_model\K-Module", device="cuda")

    def __init__(self, last_position, file_id):
        self.last_position = last_position
        self.file_id = file_id

    def transcribe(self, file_path, prev_emb):
        seg_bucket, emb_bucket = prev_emb[0], prev_emb[1]
        
        segments, _ = WhisperDiarization.model.transcribe(
            file_path, beam_size=1, language='ko', word_timestamps=True)
        seg_list = return_lst(segments, 0)
        embeddings = np.zeros(shape=(len(seg_list), 192))
        embeddings = list(get_embeddings(seg_list, embeddings, file_path))

        seg_list = seg_list[:-1]
        embeddings = embeddings[:-1]

        seg_bucket += seg_list
        emb_bucket += embeddings

        seg_bucket, emb_bucket = return_spk_lst(seg_bucket, emb_bucket)
        seg_list, count = [], 0
        for segment in seg_bucket:
            count += 1
            if count < len(seg_bucket):
                segment_speaker = segment['speaker']
                speaker = 0
                if segment_speaker is None or "1" in segment_speaker:
                    speaker = 1
                data = dict(start=self.last_position + round(segment['start'] * 1000),
                            end=self.last_position + round(segment['end'] * 1000), speaker=speaker, text=segment['text'])
                seg_list.append(dict(start = segment['start'], end=segment['end'], speaker=speaker, text=segment['text']))
                FileManager.insert_stt(file_id=self.file_id, data=data)
        
        # list of dict : {speaker : int or None, start : int(s), end : int(s), text : str}
        return seg_list, [seg_bucket, emb_bucket]