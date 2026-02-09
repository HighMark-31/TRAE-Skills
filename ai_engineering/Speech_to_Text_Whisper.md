# Skill: Speech-to-Text Implementation (Whisper)

## Purpose
To implement robust audio transcription and translation using OpenAI's Whisper model, handling large files, various formats, and specialized vocabulary.

## When to Use
- When converting user voice commands to text in a web/mobile app.
- When transcribing long-form content (podcasts, meetings).
- When you need high-accuracy transcription for non-English languages.

## Procedure

### 1. Handling Large Files (Splitting with FFmpeg)
Whisper API has a 25MB limit. Use FFmpeg to split or compress.

```bash
# Split audio into 10-minute segments
ffmpeg -i input.mp3 -f segment -segment_time 600 -c copy out%03d.mp3

# Compress to low-bitrate mono MP3 (saves space while keeping speech clear)
ffmpeg -i input.wav -ac 1 -ar 16000 -ab 32k output.mp3
```

### 2. Basic Transcription (Node.js)
Integrate the OpenAI SDK for transcription.

```typescript
import fs from 'fs';
import OpenAI from 'openai';

const openai = new OpenAI();

async function transcribe(filePath: string) {
  const response = await openai.audio.transcriptions.create({
    file: fs.createReadStream(filePath),
    model: "whisper-1",
    language: "en", // Optional but improves accuracy
    response_format: "verbose_json", // Gives timestamps
    prompt: "The transcript is about a software architecture meeting.", // Helps with context/acronyms
  });

  return response;
}
```

### 3. Handling Timestamps & Subtitles
Use the `srt` or `vtt` format for video captions.

```typescript
const srtTranscription = await openai.audio.transcriptions.create({
  file: fs.createReadStream("video_audio.mp3"),
  model: "whisper-1",
  response_format: "srt",
});

fs.writeFileSync("subtitles.srt", srtTranscription);
```

### 4. Specialized Vocabulary (Prompts)
Pass technical terms or proper nouns in the `prompt` parameter to ensure correct spelling.

```typescript
// Prompt example to ensure technical terms are spelled correctly
const prompt = "The speakers discuss Kubernetes, Istio, and gRPC.";
```

### 5. Local Execution (Python/Faster-Whisper)
For privacy or high volume, use `faster-whisper` locally.

```python
from faster_whisper import WhisperModel

model_size = "large-v3"
model = WhisperModel(model_size, device="cuda", compute_type="float16")

segments, info = model.transcribe("audio.mp3", beam_size=5)

for segment in segments:
    print("[%.2fs -> %.2fs] %s" % (segment.start, segment.end, segment.text))
```

## Constraints
- **File Size**: 25MB limit on API. Must split/compress manually.
- **Latency**: Not real-time (usually 5-15s for a 1-minute clip).
- **Privacy**: API usage sends data to OpenAI. Use local Whisper for sensitive data.

## Expected Output
Highly accurate, time-stamped text representing the spoken audio, optionally translated into English.
