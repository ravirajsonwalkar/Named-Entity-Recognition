Named Entity Recognition (NER) Web App
This project is a Gradio-based web application for performing Named Entity Recognition (NER) using the dslim/bert-base-NER model from Hugging Face Transformers. The app can be deployed locally or connected to an API for entity extraction.
Features

Uses Hugging Face Transformers for NER with dslim/bert-base-NER.
Implements token merging to handle subword splits and improve entity extraction.
Gradio UI for an easy-to-use web interface.
Can work locally or integrate with an external API via HF_API_NER_BASE.

Installation

Clone the repository:
bashCopygit clone https://github.com/your-username/ner-web-app.git
cd ner-web-app

Create a virtual environment and install dependencies:
bashCopypython -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt

Set up environment variables:
bashCopyexport HF_API_KEY=your_huggingface_api_key
export PORT4=7860  # Optional: Change the default port


Usage

Run the app:
bashCopypython app.py

Once launched, access the Gradio interface in your browser and input text to extract entities.

Deployment
To host the app online, consider using:

Hugging Face Spaces
Google Colab
AWS EC2

Contributing
Contributions are welcome! Feel free to open an issue or submit a pull request.
License
This project is open-source under the MIT License.
