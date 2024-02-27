# Insurance RAG demo - WIP

Set up your OpenAI API key and your MongoDB connection string

run
```bash
source env/bin/activate 
```

``` bash  
pip3 install uvicorn
python install langchain
python install langchain_openai
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

