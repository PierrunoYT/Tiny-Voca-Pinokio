# tiny-voca (Pinokio launcher)

One-click launcher for [tiny-voca](https://github.com/n4ze3m/tiny-voca), a 4.5M-parameter English text-to-speech model with two voices: **F2** (female) and **M2** (male). It runs on the CPU at roughly 70x real time and outputs 24 kHz mono audio. Weights: [n4ze3m/tiny-voca](https://huggingface.co/n4ze3m/tiny-voca).

## What the launcher does

- **Install**: creates a Python venv in `app/env`, installs the CPU build of PyTorch, `tiny-voca` and the `dizione` phonemizer from GitHub, then downloads `tiny-voca.pt` and `phonemizer/` (about 24 MB) into `app/weights`.
- **Start**: runs a Gradio web UI (`app/app.py`).
- **Update**: pulls this launcher, reinstalls the latest `tiny-voca`/`dizione` and fetches the latest weights.
- **Reset**: deletes `app/env` and `app/weights`.

## Usage

1. Click **Install**, then **Start**.
2. Open the Web UI, type English text, pick a voice and click **Generate**.

Controls:

| Control | Default | Meaning |
|---|---|---|
| Voice | F2 | `F2` (female) or `M2` (male) |
| Speed | 1.0 | Speaking rate; larger is faster |
| Pitch shift | 0 | Semitones up or down |
| Pitch range | 1.0 | More or less pitch movement |

Text of any length is fine: it is read sentence by sentence and joined. English only.

## API

The UI exposes the Gradio endpoint `/generate` with the arguments `text, voice, speed, pitch_semitones, pitch_range`. It returns a WAV file. Use the URL shown in Pinokio (for example `http://127.0.0.1:7860`).

### Python

```python
from gradio_client import Client

client = Client("http://127.0.0.1:7860/")
wav_path = client.predict(
    "Hello! This is tiny voca.",  # text
    "F2",                         # voice: F2 or M2
    1.0,                          # speed
    0,                            # pitch shift (semitones)
    1.0,                          # pitch range
    api_name="/generate",
)
print(wav_path)
```

### JavaScript

```javascript
import { Client } from "@gradio/client";

const client = await Client.connect("http://127.0.0.1:7860/");
const result = await client.predict("/generate", {
  text: "Hello! This is tiny voca.",
  voice: "M2",
  speed: 1.0,
  pitch_semitones: 0,
  pitch_range: 1.0,
});
console.log(result.data[0].url);
```

### Curl

```bash
EVENT_ID=$(curl -s -X POST http://127.0.0.1:7860/gradio_api/call/generate \
  -H "Content-Type: application/json" \
  -d '{"data": ["Hello! This is tiny voca.", "F2", 1.0, 0, 1.0]}' | jq -r .event_id)

curl -s -N http://127.0.0.1:7860/gradio_api/call/generate/$EVENT_ID
# The "complete" event holds the audio file URL; download it with curl -o out.wav <url>
```

## License

The launcher is MIT. tiny-voca code and weights are Apache-2.0 (phonemizer data licenses ship in `app/weights/phonemizer`).
