<p align="center">
  <a href="https://github.com/docling-project/docling-sdg">
    <img loading="lazy" alt="Docling" src="https://github.com/docling-project/docling-sdg/raw/main/docs/assets/docling-sdg-pic.png" width="40%"/>
  </a>
</p>

# AI Tutor DG

[![Platforms](https://img.shields.io/badge/platform-macos%20|%20linux%20|%20windows-blue)](https://github.com/docling-project/docling-parse/)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://docs.pydantic.dev/latest/contributing/#badges)

AI Tutor Data Generation (DG) provides a set of tools to create artificial data from documents, leveraging generative AI capabilities.

## Features

- 🧬 Generation of question(text and image)-answering pairs from passages of [multiple document formats][supported_formats] including
  PDF, PNG, JPG, JPEG.
- 💻 Simple and convenient CLI

### Coming soon

- 📝 More optimizer prompt
- 📝 Adding overlapping when chunking image
- 📝 Documentation

## Installation

To use AI Tutor DG, you can clone this repository for
creating a virtual environment, installing the packages, and running the project commands.

```bash
git clone https://github.com/TranMinhThang-dev/AI_tutor_data_generation.git
cd AI_tutor_data_generation
git checkout dev
pip install -r requirements.txt
```

## Getting started

You can create synthetically-generated questions and answers from relevant parts of one or several documents.
These question-answer pairs may be used in AI applications, such as evaluating or generating
ground truth to train a language model.

### Sample

Generating data from pdf

```
python main.py --input data/Chuyên\ đề\ SỐ\ PHỨC\ đầy\ đủ\ -\ Bùi\ Trần.pdf  --start_page 14 --end_page 17 --step-by-step
```

By default, the results will be exported to the file `output.json`. Every line represents a question-answer pair.

## Get help and support

Please feel free to connect with us using the [discussion section](https://github.com/TranMinhThang-dev/AI_tutor_data_generation/discussions).

## Current flow(subject to change)

<p align="center">
  <a href="https://github.com/TranMinhThang-dev/AI_tutor_data_generation/blob/dev/img/architecture.png">
    <img loading="lazy" alt="Architecture" src="https://github.com/TranMinhThang-dev/AI_tutor_data_generation/blob/dev/img/architecture.png"/>
  </a>
</p>

### Techainer ❤️

The project was started by the AI for knowledge team at Techainer.
