from superduper import Model, logging


class Rag(Model):
    """ RAG model for question answering with retrieval. """
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
        self.vector_index = self.db.load(
            "vector_index", self.vector_index_name)
        super().init(db=db)

    def predict(self, query, pdf_filename, top_k=7, format_result=False):
        vector_search_out = self.vector_search(query, pdf_filename, top_k=top_k)
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

    def vector_search(self, query, pdf_filename, top_k=7, format_result=False):
        """ Perform vector search to retrieve relevant documents.

        Args:
            query (str): The query to search for.
            pdf_filename (str): The filename of the PDF to filter the search results.
            top_k (int): The number of documents to retrieve.
            format_result (bool): Whether to format the result.

        Returns:
            list: The search results.
    
        """
        logging.info(f"PDF: Filename filter: {pdf_filename}")
        logging.info(f"QUERY: Vector search query: {query}")
        key = self.vector_index.indexing_listener.key
        logging.info(f"KEY: {key}")

        # Use rsplit to split from the right, ensuring only one split
        _outputs__chunk = key.rsplit('.txt', 1)[0]
        logging.info(f"OUTPUTS CHUNK: {_outputs__chunk}")
        
        select = self.db[self.vector_index.indexing_listener.select.table].like({self.vector_index.indexing_listener.key: query},
              vector_index=self.vector_index.identifier,
              n=top_k,
              ).select()
        logging.info(f"SELECT: Vector search select: {select}")
        out = select.execute()

        if out:
            out = sorted(out, key=lambda x: x["score"], reverse=True)
            logging.info(f"OUT: Vector search out: {out}")

            # Below code is just EMULATING the MongoDB Atlas Vector Search Pre-Filter
            # For more information: https://www.mongodb.com/docs/atlas/atlas-vector-search/vector-search-stage/#atlas-vector-search-pre-filter
            # At the moment the code was written, superduper-framework = "0.4.5" doesn't support the filter parameter in the $vectorSearch stage
            # TODO: Once superduper-framework supports the filter parameter in the $vectorSearch stage, add the filter parameter to the vector_query

            filename_filter = pdf_filename
            # Filter the documents by the specific filename
            filtered_out = [doc for doc in out if any(
                element['metadata']['filename'] == filename_filter
                for element in doc[_outputs__chunk]['source_elements']
            )]

            logging.info(f"FILTERED OUT: Vector search out: {filtered_out}")
        
        # Return filtered_out if it's not empty, otherwise return out
        return filtered_out if filtered_out else out

    # In case you want to build the vector_query by using pymongo directly (MongoClient) and apply the filter. It'll be something like this:
    #     
    # vector_query = [
    #     {
    #         "$vectorSearch": {  
    #             'index': INDEX_NAME,
    #             'path': "_outputs.elements.<embedding-model>.0",
    #             'queryVector': query_embedding,
    #             'numCandidates': vector_search_top_k,
    #             'limit': vector_search_top_k,
    #             'filter': {'_outputs.elements.chunk.0.source_elements.metadata.filename': filename}
    #         }
    #     },
    #     {
    #         "$project": {
    #             "_outputs.elements.text-embedding-ada-002.0": 0,
    #             "score": { "$meta": "vectorSearchScore" }
    #         }
    #     }
    # ]
    #
    # Note that above code is just an example and it's not implemented in the current codebase
    # The current codebase uses the superduper library to build the vector_query
    # 'filter': {'_outputs.elements.chunk.0.source_elements.metadata.filename': filename} is the key part that filters the search results to only the PDF that we're interested in