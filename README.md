#                     Portable Executable Analysis With Machine learning File Scanner API

## Overview
Portable Executable Analysis is a project designed to analyze and classify PE files (such as .exe and .dll) for malicious behavior using machine learning techniques.

## Features
- Extracts important features from PE files.
- Classifies files as either malicious or legitimate.
- Supports both .exe and .dll formats.

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/deskram/PEBehaviorDetection.git
   cd PEBehaviorDetection
   ```
2. Install the required dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
To start the API server, run:
```bash
uvicorn main:app --reload
```

Then, you can send a POST request to `/pe_scan/` with a PE file to analyze it.

## API Endpoints
- `POST /pe_scan/` - Analyzes a provided PE file.

## License
This project includes components from the following libraries and tools:

- **DeskRam**
- **EXEGR**
- **Ammer SSH**

The rights to these tools are held by their respective authors.

## Acknowledgments
- Thanks to the open-source community for their invaluable contributions.

## Contact
For any inquiries, please reach out to [your.email@example.com].
```
