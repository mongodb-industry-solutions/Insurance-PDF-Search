# Insurance RAG demo - WIP

Create a file named '.env' and store your OpenAI API key and MongoDB connection string in it, follow this format:

```bash
OPENAI_API_KEY=<your key>
MONGO_URI="mongodb+srv://<usr>:<pswd>@<cluster-name>.mongodb.net/?retryWrites=true&w=majority"
```

``` bash  
pip install -r requirements.txt
```

and then launch the backend

```bash
python3 -m uvicorn main:app --reload
```
move to the frontend folder and run the frontend

```bash
npm install
npm start
```

