# Memopin - AI-Enhanced Memory Recall Tool (Backend)

## Project Description

Memopin is an AI-enhanced memory recall tool designed to address the challenges of fragmented memories and forgetfulness in the digital age. People often struggle to recall meaningful moments as photos, conversations, and videos are scattered across various platforms, making retrieval difficult. For individuals with Alzheimer's and other memory impairments, this struggle becomes even more pronounced, leading to confusion, disorientation, and emotional distress.

Memopin solves these challenges by providing a unified platform to store and retrieve key moments. Using advanced AI technologies like Retrieval-Augmented Generation (RAG), Large Language Models (LLMs), and Natural Language Processing (NLP), it helps users retrieve detailed, context-rich memories from multimedia content like audio, video, and photos. Memopin's video analysis adds an extra layer of depth to memory recall, ensuring a comprehensive understanding of multimedia content.

The solution organizes memories into a searchable, context-aware database, making it easy to reflect on past experiences and improve cognitive health, emotional well-being, and memory management.

## Tech Stack

- **React**: Frontend framework for building the user interface and managing user interactions.
- **ReactDOM**: Renders the React components in the browser.
- **NLP (Natural Language Processing)**: Analyzes speech and text within recorded content to enhance memory context and improve relevance.
- **Retrieval-Augmented Generation (RAG) AI**: Combines memory storage and querying to generate contextually accurate responses to user queries.
- **Large Language Models (LLMs)**: Understands and contextualizes user queries, offering detailed and relevant memories reflecting personal experiences.
- **Vector Databases**: Efficiently stores and retrieves multimedia data, ensuring structured organization for quick access.

## Setup Instructions

Follow these steps to set up the **ai-backend** project locally:

1. **Ensure to go to the folder**:
   - First, ensure that the **ai-app** project is set up . And go to the same folder where we cloned ai-app.

2. **Open a New Terminal for ai-backend**:
   - Open another terminal or command prompt for the **ai-backend** setup and follow these steps.

3. **Initialize Git**:
   - Inside your terminal, initialize a Git repository:
     ```bash
     git init
     ```

4. **Clone the AI Backend Repository**:
   - Clone the **ai-backend** repository to your local machine using the URL:
     ```bash
     git clone <this repository url>
     ```

5. **Navigate to the ai-backend Directory**:
   - Change to the **ai-backend** directory:
     ```bash
     cd ai-backend
     ```

6. **Create a Virtual Environment**:
   - Create a new virtual environment using conda (Python 3.8):
     ```bash
     conda create -n venv python=3.8
     ```

7. **Activate the Virtual Environment**:
   - Activate the newly created virtual environment:
     ```bash
     conda activate venv
     ```

8. **Install Dependencies**:
   - Install the required Python dependencies from the `requirements.txt` file:
     ```bash
     pip install -r requirements.txt
     ```

9. **Create a `.env` File**:
   - Create a `.env` file in the root directory of **ai-backend** with the following keys:
     ```
     LANGCHAIN_API_KEY=<your langchain api key> 
     GROQ_API_KEY=<your groq api key> 
     LANGCHAIN_TRACING_V2="true"
     ```

10. **Run the Application**:
    - Start the AI backend service by running:
      ```bash
      python app.py
      ```

11. **Open the Frontend Application**:
    - Go to the **ai-app** directory and run it using:
      ```bash
      npm run dev
      ```
    - Open your browser and go to `http://localhost:5173/`. You should now be able to process audio files either for storing or retrieving memories.

---

## Additional Repositories

Once you have the **ai-backend** set up, make sure you have **ai-app** set up. There are two repositories you should clone and set up:

### 1. **AI Frontend** Repository
The user interface of the Memopin project, where users can interact with the system.

- Repository URL: [ai-app](https://github.com/Yash8745/ai-app) 

### 2. **Node Backend** Repository
The **Node Backend** handles the MongoDB-related functionality, including user management, authentication, and storing login/signup related data.

- Repository URL: [node-backend](https://github.com/Yash8745/node-backend)
