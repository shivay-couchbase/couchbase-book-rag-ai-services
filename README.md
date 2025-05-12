# Couchbase Book Knowledge Assistant

A Retrieval-Augmented Generation (RAG) application that uses Couchbase's vector search capabilities and Capella AI Services to answer questions about books and historical content.

![Couchbase Logo](img/cblogo.png)

## Overview

This application combines the power of:
- Couchbase's vector search for efficient document retrieval
- Capella AI Services for generating embeddings and responses
- Streamlit for a beautiful, interactive user interface

The assistant can answer questions about books and historical content by:
1. Generating embeddings for user queries
2. Finding relevant documents using vector search
3. Using the context to generate accurate, contextual responses

## Features

- 🤖 Interactive chat interface
- 📚 Context-aware responses
- 🔍 Vector-based document retrieval
- 🎨 Image generation for visual context
- 💬 Streaming responses
- 🎯 Suggested questions for easy start

## Prerequisites

- Python 3.8+
- Couchbase Capella account
- Capella AI Services endpoint
- Couchbase bucket with vector search index

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd <repository-name>
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment:
- Create a `.env` file with your credentials:
```
COUCHBASE_USERNAME=your_username
COUCHBASE_PASSWORD=your_password
COUCHBASE_ENDPOINT=your_capella_endpoint
```

## Project Structure

```
.
├── app.py              # Streamlit application
├── app_ui.py           # UI components and styling
├── main.py             # Core RAG functionality
├── requirements.txt    # Python dependencies
└── img/               # Application images
    ├── cblogo.png
    ├── cb.svg
    └── capella_ai.png
```

## Usage

1. Start the application:
```bash
streamlit run app.py
```

2. Enter your Capella AI Services endpoint when prompted

3. Start asking questions about books and historical content

## Example Questions

- "In the midst of the 10th century, about 967, which reclaimed its hereditary rule in Mecca"
- "In 1995 King Fahd suffered a stroke and Crown Prince Abdullah, assumed the role of the king. how is Abdullah related to King Fahd"
- "What was the significance of the Battle of Badr in Islamic history?"

## Technical Details

### RAG Implementation

The application uses a three-step process:

1. **Embedding Generation**:
   - Uses Capella AI Model Service embedding model to convert text to vectors
   - Generates embeddings for both queries and documents

2. **Vector Search**:
   - Uses Couchbase's vector search capabilities
   - Finds most relevant documents based on semantic similarity

3. **Response Generation**:
   - Uses Capella AI Services to generate contextual responses
   - Includes relevant document content in the prompt
   - Generates both text and image responses

### UI Components

- Modern, responsive design
- Real-time streaming responses
- Suggested questions for easy start
- Error handling and user feedback
- Couchbase-themed styling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Couchbase for the vector search capabilities
- Capella AI Services for the AI capabilities
- Streamlit for the beautiful UI framework

## Support

For support, please open an issue in the GitHub repository or contact the maintainers.

---

<div align="center">
  <img src="img/capella_ai.png" alt="Capella AI" width="200"/>
</div> 
