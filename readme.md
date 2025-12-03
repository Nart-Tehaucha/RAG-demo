<h1>Quick RAG retrieval system demonstration</h1>

<h2>Used dataset:</h2>
https://www.kaggle.com/datasets/dkhundley/sample-rag-knowledge-item-dataset?resource=download

<h2>Prerequisites</h2>
<ul>
  <li>Python 3.11+</li>
</ul>

<h2>Installation</h2>
<h3>1. Clone the repository:</h3>

```
git clone https://github.com/Nart-Tehaucha/RAG-demo.git
cd Retrieval-Augmented-Generation
```

<h3>2. Create a virtual environment</h3>

```
python -m venv venv
```

<h3>3. Activate the virtual environment</h3>

```
venv\Scripts\Activate
(or on Mac): source venv/bin/activate
```

<h3>4. Install libraries</h3>

```
pip install -r requirements.txt
```

<h3>5. Setup npm and react</h3>

```
npm init -y
npm install
```
```
npm install react react-dom
```

<h3>5. Add OpenAI API Key</h3>
Get an OpenAI API Key from here: https://platform.openai.com/settings/organization/admin-keys<BR>
Add it to .env.example<BR>
Rename to .env<BR>

<h2>Executing the scripts</h2>

- Open a terminal in VS Code

- Set up Chromadb with our dataset:

```
python backend/ingest.py
```
- Run the Flask server:
```
python backed/app.py
```
- Run react:
```
npm run dev
```
