from superduper import Model, logging


class Rag(Model):
    llm_model: Model
    vector_index_name: str
    prompt_template: str
    processor: None | Model = None

    def __post_init__(self, *args, **kwargs):
        assert "{context}" in self.prompt_template, 'The prompt_template must include "{context}"'
        assert "{query}" in self.prompt_template, 'The prompt_template must include "{query}"'
        super().__post_init__(*args, **kwargs)

    def init(self, db=None):
        db = db or self.db
        self.vector_index = self.db.load("vector_index", self.vector_index_name)
        super().init(db=db)
        
    
    def predict(self, query, top_k=5, format_result=False):
        vector_search_out = self.vector_search(query, top_k=top_k)
        key = self.vector_index.indexing_listener.key
        context = "\n\n---\n\n".join([x[key] for x in vector_search_out])
        
        prompt = self.prompt_template.format(context=context, query=query)
        output = self.llm_model.predict(prompt)
        result = {
            "answer": output,
            "docs": vector_search_out,
        }
        if format_result and self.processor:
            result["images"] = list(self.processor.predict(
                vector_search_out,
                match_text=output,
            ))
        return result

    def vector_search(self, query, top_k=5, format_result=False):
        logging.info(f"Vector search query: {query}")
        select = self.db[self.vector_index.indexing_listener.select.table].like(
            {self.vector_index.indexing_listener.key:query},
            vector_index=self.vector_index.identifier, 
            n=top_k,
        ).select()
        out = select.execute()
        if out:
            out = sorted(out, key=lambda x: x["score"], reverse=True)
        return out