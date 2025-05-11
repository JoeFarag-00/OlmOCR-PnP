<div align="center">
  <!-- <img src="https://github.com/allenai/OLMo/assets/8812459/774ac485-a535-4768-8f7c-db7be20f5cc3" width="300"/> -->
<img src="https://github.com/user-attachments/assets/d70c8644-3e64-4230-98c3-c52fddaeccb6" alt="olmOCR Logo" width="300"/>
<br/>
  <br>
  <h1>OlmOCR</h1>
</div>

# 🚀 OlmOCR-PnP

**Plug-and-play PDF → Text OCR using AllenAI’s OlmOCR web UI**  
_No setup needed—just drop your PDFs and go!_

This repo is just a wrapper repurposing the OlmOCR toolkit demo for production without any further setup.

Try the online demo: [https://olmocr.allenai.org/](https://olmocr.allenai.org/)

What is included:
 - A prompting strategy to get really good natural text parsing using ChatGPT 4o - [buildsilver.py](https://github.com/allenai/olmocr/blob/main/olmocr/data/buildsilver.py)
 - An side-by-side eval toolkit for comparing different pipeline versions - [runeval.py](https://github.com/allenai/olmocr/blob/main/olmocr/eval/runeval.py)
 - Basic filtering by language and SEO spam removal - [filter.py](https://github.com/allenai/olmocr/blob/main/olmocr/filter/filter.py)
 - Finetuning code for Qwen2-VL and Molmo-O - [train.py](https://github.com/allenai/olmocr/blob/main/olmocr/train/train.py)
 - Processing millions of PDFs through a finetuned model using Sglang - [pipeline.py](https://github.com/allenai/olmocr/blob/main/olmocr/pipeline.py)
 - Viewing [Dolma docs](https://github.com/allenai/dolma) created from PDFs - [dolmaviewer.py](https://github.com/allenai/olmocr/blob/main/olmocr/viewer/dolmaviewer.py)

## Team

<!-- start team -->

**olmOCR** is developed and maintained by the AllenNLP team, backed by [the Allen Institute for Artificial Intelligence (AI2)](https://allenai.org/).
AI2 is a non-profit institute with the mission to contribute to humanity through high-impact AI research and engineering.
To learn more about who specifically contributed to this codebase, see [our contributors](https://github.com/allenai/olmocr/graphs/contributors) page.

<!-- end team -->

## 📦 Project Structure
OlmOCR-PnP/
├── config.py # ➡️ global settings & folder paths
├── logger.py # 📝 file-based logging setup
├── pdf_chunker.py # 📄 PDFChunker: splits big PDFs into 10-page parts
├── ocr_client.py # 🤖 OCRClient: automates upload & “Copy” via Selenium
├── main.py # 🎯 Main: orchestrates chunking → OCR → assemble text
├── requirements.txt # 📦 Python dependencies
├── Input_PDFs/ # 📥 drop your .pdf files here (ignored by Git)
├── Chunked_PDFs/ # 🔀 intermediate 10-page chunks (auto-created)
└── Output_PDFs/ # 📤 final .txt outputs & ingestion_process.log
---

## ✨ Features

- **Zero-config**: No API keys or complex setup  
- **Automatic chunking**: Splits large PDFs into 10-page segments  
- **Web-UI OCR**: Leverages AllenAI’s OlmOCR via Selenium  
- **Plug-and-play**: Run `python main.py`—outputs drop in `Output_PDFs/`  
- **Progress bars**: Real-time feedback on PDF & chunk processing with `tqdm`  
- **Robust logging**: Detailed logs in `Output_PDFs/ingestion_process.log`

---
## 🛠️ Quick Start

1. **Clone the repo**  
   ```bash
   git clone https://github.com/JoeFarag-00/OlmOCR4Free.git
   cd OlmOCR4Free

2. **Install dependencies**  
   ```bash
    pip install -r requirements.txt

## License

<!-- start license -->

**olmOCR** is licensed under [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0).
A full copy of the license can be found [on GitHub](https://github.com/allenai/olmocr/blob/main/LICENSE).

<!-- end license -->

## Citing

```bibtex
@misc{olmocr,
      title={{olmOCR: Unlocking Trillions of Tokens in PDFs with Vision Language Models}},
      author={Jake Poznanski and Jon Borchardt and Jason Dunkelberger and Regan Huff and Daniel Lin and Aman Rangapur and Christopher Wilhelm and Kyle Lo and Luca Soldaini},
      year={2025},
      eprint={2502.18443},
      archivePrefix={arXiv},
      primaryClass={cs.CL},
      url={https://arxiv.org/abs/2502.18443},
}
```
