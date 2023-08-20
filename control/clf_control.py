# import os
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence
from transformers import AutoModel, SEWModel, AutoTokenizer, AutoProcessor

import soundfile as sf

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL_PATH = r"C:\Users\jhkim\VoicePhising\KB-Datory\ai_model\B-Module\model_epoch1.pt"
text_tokenizer = AutoTokenizer.from_pretrained("BaekRok/kb_albert")
audio_processor = AutoProcessor.from_pretrained("asapp/sew-tiny-100k-ft-ls100h")

class Classification_Model(nn.Module):
    def __init__(self,
                 text_model="BaekRok/kb_albert",
                 w2v_model="asapp/sew-tiny-100k-ft-ls100h",
                 speaker_model="BaekRok/kb_albert",
                 pooler=False,
                 num_classes=2):
        super().__init__()
        self.text_model = AutoModel.from_pretrained(text_model)
        self.w2v_model = SEWModel.from_pretrained(w2v_model)
        self.speaker_model = AutoModel.from_pretrained(speaker_model)
        self.linear = nn.Linear(512, 768)
        self.concat_linear = nn.Linear(2304, 768)

        # LSTM Layer
        self.lstm = nn.LSTM(input_size=768, hidden_size=384, num_layers=1, batch_first=True, bidirectional=True)

        # Classifier Layer
        self.classifier = nn.Linear(768, num_classes)
    def forward(self, data, lengths, prev_hn=None, prev_cn=None):
        concat_tensors = []
        audio, text, speaker = data
        for audio_seg, text_seg, speaker_seg in zip(audio, text, speaker):
            audio_outputs = self.w2v_model(**audio_seg)
            text_outputs = self.text_model(**text_seg)
            speaker_outputs = self.speaker_model(**speaker_seg)

            # Use attention masks to exclude padded tokens
            text_mask = text_seg['attention_mask'].unsqueeze(-1).expand(text_outputs.last_hidden_state.size())
            speaker_mask = speaker_seg['attention_mask'].unsqueeze(-1).expand(speaker_outputs.last_hidden_state.size())

            # Compute mean over tokens, excluding padding tokens
            audio_emb = self.linear(audio_outputs.last_hidden_state.mean(1))
            text_emb = (text_outputs.last_hidden_state * text_mask).sum(1) / text_mask.sum(1)
            speaker_emb = (speaker_outputs.last_hidden_state * speaker_mask).sum(1) / speaker_mask.sum(1)

            print(audio_emb[0].size, text_emb[0].size, speaker_emb[0].size)
            concat_feature = torch.cat((audio_emb, text_emb, speaker_emb), dim=1)
            concat_feature = self.concat_linear(concat_feature)
            concat_tensors.append(concat_feature)

        # Padding
        padded_concat_tensors = nn.utils.rnn.pad_sequence(concat_tensors, batch_first=True)

        # Packing
        packed_input = pack_padded_sequence(padded_concat_tensors, lengths, batch_first=True, enforce_sorted=False)

        # LSTM
        if prev_hn is None or prev_cn is None:
            packed_output, (hn, cn) = self.lstm(packed_input)
        else:
            packed_output, (hn, cn) = self.lstm(packed_input, (prev_hn, prev_cn))

        # Unpacking
        output, _ = pad_packed_sequence(packed_output, batch_first=True)

        # Classification
        logits = self.classifier(output[:, -1, :])

        return logits, hn, cn
    
model = Classification_Model()
ckpt = torch.load(MODEL_PATH)
model.load_state_dict(ckpt['model_state_dict'])
model.to(device)

class Classifier:
    def __init__(self):
        pass
        
    def inference(self, data, audio_path):
        with torch.no_grad():
            model.eval()
                        
            text_inputs = [text_tokenizer([tx['text'] for tx in data], padding=True, truncation=True, return_tensors="pt")]
            speaker_inputs = [text_tokenizer(['speaker'+str(sp['speaker']) for sp in data], padding=True, truncation=True, return_tensors="pt")]
            audio_total_segment = sf.read(audio_path)[0]
            all_audio_segments = [audio_total_segment[int(seg['start'] * 16000) : int(seg['end'] * 16000)] for seg in data]
            
            audio_inputs = [audio_processor(audio_segments, return_attention_mask=True, sampling_rate=16000, truncation=True, max_length = 160000, padding=True, return_tensors="pt") for audio_segments in all_audio_segments]
            
            text_inputs = [text.to(device) for text in text_inputs]
            speaker_inputs = [speaker.to(device) for speaker in speaker_inputs]
            audio_inputs = [audio.to(device) for audio in audio_inputs]
            
            print(*audio_inputs)
            
            logit, hn, cn = model((audio_inputs, text_inputs, speaker_inputs), len(text_inputs))
            score = torch.sigmoid(logit)
            print(score)
            
            
        return score
            
    
    