# 📰 rsser: "Smart" RSS Analyzer

An intelligent RSS feed analyzer powered by Python and designed for seamless integration with FreshRSS.
Focused on statistical analysis for realiability.

TODO:
* [ ] Add multiple Data analysis tools
* [ ] Add multiple visualization styles
* [ ] Add frontend / "home" page for visualization management
* [ ] Implement ML - Model for summarization / questioning

![Version](https://img.shields.io/badge/version-1.0.0-blue)
![License](https://img.shields.io/badge/license-None-lightgrey)
![Stars](https://img.shields.io/github/stars/plusk0/rsser?style=social)
![Forks](https://img.shields.io/github/forks/plusk0/rsser?style=social)

![example-preview-image](/preview_example.png)
_A sneak peek at rsser's potential analysis output._

## ✨ Features

*   **🔍 RSS Analysis:** Extract valuable insights from your RSS feeds, identifying trends, popular topics, and content patterns.
*   **🔗 FreshRSS Integration:** Seamlessly connect with your FreshRSS backend to analyze your curated feeds without manual exports.
*   **📊 Customizable Visualizations:** Generate insightful charts and graphs from your RSS data to better understand content consumption and trends.
*   **⚙️ Modular & Extensible:** Built with a modular Python architecture, making it easy to add new analysis modules or integrate with different backends.
*   **🚀 Dockerized Deployment:** Easily deploy and run rsser in isolated environments using Docker, ensuring consistent performance across platforms.

## 🚀 Installation

You can get rsser up and running using Docker or by setting up a local Python environment.

### Docker (Recommended)

The easiest way to deploy rsser is by using Docker.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/plusk0/rsser.git
    cd rsser
    ```

2.  **Build the Docker image:**
    ```bash
    docker build -t rsser:latest .
    ```

3.  **Run the Docker container:**
    You might need to mount your `config` and `data` directories if you want persistent storage or custom configurations.
    ```bash
    docker run -it --rm -v $(pwd)/config:/app/config -v $(pwd)/data:/app/data rsser:latest python main.py
    ```
    _Replace `$(pwd)` with `%cd%` on Windows._

### Manual Installation (Python)

If you prefer to run rsser directly on your system, follow these steps:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/plusk0/rsser.git
    cd rsser
    ```

2.  **Create and activate a Conda environment (recommended for `environment.yml`):**
    ```bash
    conda env create -f environment.yml
    conda activate rsser
    ```
    If you don't use Conda, you can create a virtual environment and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate # On Windows: .\venv\Scripts\activate
    pip install -r requirements.txt # (assuming requirements.txt generated from environment.yml)
    ```
    _Note: If `requirements.txt` is not present, you'll need to generate it from `environment.yml` or manually install packages._

3.  **Configure your settings:**
    Navigate to the `config` directory and update `fresh_rss.ini`, `analysis.ini`, or similar files with your FreshRSS backend details and other preferences.

4.  **Run the application:**
    ```bash
    python main.py
    ```

## 💡 Usage Examples

rsser is designed to be run as a script, regularly processing your RSS database based on the configuration provided.

### Basic Execution

After installation, you can run the main script. Ensure your configuration files in the `config` directory are set up correctly.

```bash
python main.py
