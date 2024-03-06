# Insurance RAG demo - WIP

Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it, follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGO_URI="mongodb+srv://<usr>:<pswd>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
```

run
```bash
source env/bin/activate 
```

``` bash  
pip3 install uvicorn
python install langchain
python install langchain_openai
python -m pip install python-dotenv
```

and then

```bash
python3 -m uvicorn main:app --reload
```
move to /frontend

```bash
npm install
npm start
```

