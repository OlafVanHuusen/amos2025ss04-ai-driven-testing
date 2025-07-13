# AI-Driven Testing Project (AMOS SS 2025)

This repository contains the code and tests for the AI-Driven Testing project, designed to develop an LLM-based AI that can automatically generate test code for existing software through a chat-based interface.

## Table of Contents

1. [Project Overview](#1-project-overview)
2. [Prerequisites](#2-prerequisites)
3. [Quick Start](#3-quick-start)
4. [Backend Setup and Usage](#4-backend-setup-and-usage)
5. [Frontend Setup](#5-frontend-setup)
6. [API Reference](#6-api-reference)
7. [Modular Plugin System](#7-modular-plugin-system)
8. [Configuration](#8-configuration)
9. [Examples](#9-examples)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Project Overview

### Project Goal

The goal of this project is to develop or customize a **LLM-based (Large Language Model) AI** that can automatically **generate test code** for existing software or documentation. The AI is controlled through a **chat-based interface** or a **command-line interface** and can be provided with information about the target software in various ways.

### Main Features

- 🔍 **Test Code Generation**  
  The AI can generate test code for arbitrary software using methods such as Retrieval-Augmented Generation (RAG), fine-tuning, or prompting.

- 🔄 **Incremental Test Extension**  
  The AI can recognize and expand existing test code intelligently.

- 🧪 **Understanding of Test Types**  
  The AI can distinguish between different layers and types of tests:
  - **Layers**: User interface, domain/business logic, persistence layer
  - **Test Types**: Unit test, integration test, acceptance test

- 🛠️ **On-Premise Operation**  
  The solution can run fully offline, suitable for on-premise environments.

- 🐳 **Docker Support**  
  The backend can run inside a Docker container and be accessed via an API.

- 🔌 **IDE Integration**  
  The solution can be embedded into existing **open-source development environments**.

- 🤝 **Open Source**  
The solution is open source, allowing for community contributions and transparent development.

### Usage Workflow

1. Provide the software (source code or API/documentation) either via CLI or web interface
2. Select from optional features like complexity analysis, incremental test evolution, or web-assisted research
3. Examine the generated test code along with any supporting insights or recommendations
4. Integrate test code into your existing test suite

---

## 2. Prerequisites

Before setting up the project, ensure you have the following installed:

- **Node.js** - [Install Node.js](https://nodejs.org/)
- **Docker** - [Install Docker](https://docs.docker.com/get-started/get-docker/)
- **Conda**  - [Install Conda](https://www.anaconda.com/download/success)
- **Git** (for cloning the project) - [Install Git](https://git-scm.com/downloads)

---

## 3. Quick Start

### Clone the repository:
   ```bash
   git clone https://github.com/amosproj/amos2025ss04-ai-driven-testing.git
   cd amos2025ss04-ai-driven-testing
   ```


### Automated Setup

For quick setup, use the provided setup script (not working on windows):

```bash
chmod +x setup.sh
./setup.sh
```

### Manual Setup (for using the CLI)

1. Ensure Docker is running on your machine.

2. Set up the backend:
   ```bash
   cd backend/
   conda env create -f environment.yml
   conda activate backend
   ```




### Manual Setup (for using the web interface)

1. Ensure Docker is running on your machine

2. Start the docker compose that starts both the backend and the frontend:
    ```bash
    docker compose up
    ```

---

## 4. Backend Information and Usage

### File Structure

- `api.py` — FastAPI wrapper for HTTP endpoints
- `cli.py` — Handling the CLI parameters
- `schemas.py` — Defining the data structure for information in the project
- `model_manager.py`— loading the usable models
- `module_manager.py`- loading the available modules
- `main.py` — Main script to run a single model
- `llm_manager.py` — Docker container management and LLM interaction
- `allowed_models.json` — Configuration for allowed language models
- `prompt.txt` — Default input prompt file
- `output-<MODEL_ID>.md` — example output files for each model

### Basic Usage

#### Running a Single Model

```bash
python backend/main.py
```

#### Command Line Parameters

The script supports the following command line parameters:

- `--model` - Model index to use (integer, choices based on available models, default: 0)
- `--prompt_file` - Path to the prompt file (default: `user_message.txt`)
- `--source_code` - Path to the source code file (default: `source_code.txt`)
- `--output_file` - Path to the output file (default: `output.md`)
- `--modules` - List of module names to run (space-separated)
- `--seed` - Random seed for reproducible results (default: 42)
- `--num_ctx` - Context size for the model (default: 4096)
- `--command-order` - Enable manual module ordering (flag, default: false)
- `--timeout` - Timeout for operations (integer, in seconds)
- `--use-links` - Provide one or more web links to include in the context (space-separated URLs)

#### Example with CLI parameters: 

```bash
python backend/main.py --model 1 --seed 123 --num_ctx 8192 --timeout 300 --use-links https://example.com/docs
```

#### Running All Models

```bash
python backend/example_all_models.py
```

This script:
- Starts each model's container
- Sends the provided prompt (from `prompt.txt`)
- Saves each response into its own `output-<MODEL_ID>.md`
- Stops all containers after completion

### How It Works

1. The project uses the Docker image `ollama/ollama` to run language models locally
2. The `LLMManager` class:
   - Pulls the required Docker image with progress indication
   - Selects a free port for each container
   - Waits until the container's API becomes available
   - Pulls the selected model inside the container
   - Sends user prompts to the model endpoint and writes the Markdown-formatted response

---

## 5. Frontend Setup

### Getting Started

1. Start the docker containers:
   ```bash
   docker compose up
   ```

4. Open your browser and go to:
   ```
   http://localhost:3000/
   ```

---

## 6. API Reference

### Starting the API Server

```bash
cd backend
uvicorn api:app --reload  # --port 8000 by default
```

### Available Endpoints

| Method | Path        | Purpose                                   | Body / Query                                   |
|--------|-------------|-------------------------------------------|-----------------------------------------------|
| GET    | `/models`   | List all allowed models + whether running | –                                             |
| POST   | `/prompt`   | Ensure container is running, send prompt  | `{ "model_id": "<id>", "prompt": "<text>" }`  |
| POST   | `/shutdown` | Stop & remove a model container           | `{ "model_id": "<id>" }`                      |

### API Documentation

Open the automatically generated Swagger UI at:
```
http://127.0.0.1:8000/docs
```

### Input/Output Schema

The schema defined in `schemas.py` provides a structured format for communication:

- **PromptData**: Encapsulates model metadata, prompt text, system instructions, and generation options
- **ResponseData**: Contains generated Markdown response, extracted code, token usage statistics, and timing metrics

---

## 7. Modular Plugin System

This project uses a flexible module interface to add custom functionality before and after interacting with an LLM. Modules can handle tasks like logging, prompt modification, response postprocessing, and metric collection.

#### For comprehensive information about modules in general or specific modules, see:
* [modules](modules.md)
    * [context\_size\_calculator](modules/context_size_calculator.md)
    * [lm\_eval\_runner](modules/lm_eval_runner.md)

## 8. Models

Models are configured in `allowed_models.json`.

### Supported Models

The following models are currently supported in the project:

- **[mistral:7b-instruct-v0.3-q3_K_M](https://ollama.com/library/mistral:7b-instruct-v0.3-q3_K_M)** - The 7B model released by Mistral AI, updated to version 0.3.

- **[qwen2.5-coder:3b-instruct-q8_0](https://ollama.com/library/qwen2.5-coder:3b)** - The latest series of Code-Specific Qwen models, with significant improvements in code generation, code reasoning, and code fixing.

- **[phi4-mini:3.8b-q4_K_M](https://ollama.com/library/phi4-mini)** - Microsoft's Phi-4 Mini model, a compact language model optimized for efficiency.

- **[tinyllama:1.1b](https://ollama.com/library/tinyllama)** - The TinyLlama project is an open endeavor to train a compact 1.1B Llama model on 3 trillion tokens.

- **[qwen3:4b-q4_K_M](https://ollama.com/library/qwen3)** - Qwen3 is the latest generation of large language models in Qwen series, offering a comprehensive suite of dense and mixture-of-experts (MoE) models

- **[openhermes:v2.5](https://ollama.com/library/openhermes)** - OpenHermes 2.5 is a 7B model fine-tuned by Teknium on Mistral with fully open datasets.

- **[smollm2:360m](https://ollama.com/library/smollm2:360m)** - SmolLM2 is a family of compact language models available in three size: 135M, 360M, and 1.7B parameters.

- **[phi4-reasoning:14b](https://ollama.com/library/phi4-reasoning)** - Microsoft's Phi-4 Reasoning model, optimized for complex reasoning tasks.

---

## 9. Examples

### Example Input

If your `prompt.txt` contains:

```text
Write unit tests for the following Python function:

```python
def add_numbers(a, b):
    """
    Adds two numbers together and returns the result.
    
    Args:
        a (int or float): The first number.
        b (int or float): The second number.
    
    Returns:
        int or float: The sum of a and b.
    
    Examples:
        >>> add_numbers(2, 3)
        5
        >>> add_numbers(-1, 1)
        0
        >>> add_numbers(0.5, 0.5)
        1.0
    """
    return a + b
```

### Example Output

Your `output.md` will contain:

```md
Here is how you can write unit tests for the `add_numbers` function using Python's built-in unittest module:

```python
import unittest
from add_numbers import add_numbers

class TestAddNumbers(unittest.TestCase):
    def test_positive_integers(self):
        self.assertEqual(add_numbers(2, 3), 5)
        
    def test_negative_integers(self):
        self.assertEqual(add_numbers(-1, 1), 0)
        
    def test_decimal(self):
        self.assertEqual(add_numbers(0.5, 0.5), 1.0)
        
if __name__ == "__main__":
    unittest.main()
```

This unit test covers the basic functionality with positive integers, negative integers, and decimal numbers as shown in the examples.


---

## 10. Troubleshooting

### Common Issues

1. **Docker not running**: Ensure Docker is started before running the backend
2. **Port conflicts**: The system automatically selects free ports for containers
3. **Model download failures**: Check your internet connection and Docker Hub access
4. **Memory issues**: Large models may require significant system resources
5. **Tokenizer download failures**: May require Hugging Face authentication

### Resource Management

- Each container is automatically stopped after completion to free up system resources
- The response is formatted as clean Markdown
- Progress indication is provided during Docker image and model pulling

### Getting Help

For additional support:
- Check the logs for detailed error messages
- Ensure all prerequisites are properly installed
- Verify Docker container status using `docker ps`
- Check available system resources before running large models

---

## Notes

- The script automatically pulls necessary Docker images and models if not already available
- Each container starts on a free port with automatic API endpoint management
- All models in `allowed_models.json` are supported by the Context Size Calculator
- The system is designed to work fully offline for on-premise environments