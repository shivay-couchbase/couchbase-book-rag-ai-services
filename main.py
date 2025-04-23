import base64
import logging
import asyncio
from typing import List, Dict, Any
from datetime import timedelta
from openai import OpenAI
from couchbase.cluster import Cluster
from couchbase.options import ClusterOptions, SearchOptions
from couchbase.auth import PasswordAuthenticator
from couchbase.vector_search import VectorQuery, VectorSearch
import couchbase.search as search

# Configure logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

class CouchbaseRAG:
    def __init__(self, cluster=None):
        """
        Initialize with an existing Couchbase cluster connection or create a new one
        """
        # Connection details
        connection_string = ""
        username = ""
        password = ""

        # Connect to Couchbase if no cluster provided
        if cluster is None:
            print(f"Connecting to Couchbase at {connection_string}")
            auth = PasswordAuthenticator(username, password)
            options = ClusterOptions(auth)
            self.cluster = Cluster(connection_string, options)
        else:
            self.cluster = cluster

        self.bucket_name = ""
        self.scope_name = ""
        self.collection_name = ""
        self.search_index_name = ""

        # Initialize bucket, scope and collection
        self.bucket = self.cluster.bucket(self.bucket_name)
        self.scope = self.bucket.scope(self.scope_name)
        self.collection = self.scope.collection(self.collection_name)

        # OpenAI setup
        self.client = OpenAI(
            base_url=input("Capella AI Services Endpoint"),
            api_key=base64.b64encode(f"{username}:{password}".encode("utf-8")).decode("utf-8")
        )

    def generate_embedding(self, text: str) -> List[float]:
        """Generate embedding for the input text using OpenAI"""
        try:
            print(f"Generating embedding for text: {text[:50]}...")
            response = self.client.embeddings.create(
                input=text,
                model="Snowflake/snowflake-arctic-embed-l-v2.0"
            )
            embedding = response.data[0].embedding
            print(f"Generated embedding with length: {len(embedding)}, sample: {embedding[:5]}")
            return embedding
        except Exception as e:
            print(f"Error generating embedding: {str(e)}")
            raise

    async def get_relevant_documents(self, embedding: List[float]) -> List[Dict[str, Any]]:
        """Perform vector search to find relevant documents"""
        try:
            print(f"Starting vector search with parameters: index={self.search_index_name}, embedding length={len(embedding)}")
            num_results = 10

            # Create search request with vector search
            vector_field = "embedding"
            search_req = search.SearchRequest.create(search.MatchNoneQuery()).with_vector_search(
                VectorSearch.from_vector_query(
                    VectorQuery(vector_field, embedding, num_candidates=num_results)
                )
            )

            # Execute search with timeout
            search_options = SearchOptions(timeout=timedelta(seconds=5.0))
            result = self.scope.search(self.search_index_name, search_req, search_options)
            rows = list(result.rows())

            if not rows:
                print("No vector search results found")
                return []

            # Process results
            documents = []
            for row in rows[:5]:  # Process top 5 results
                try:
                    doc_result = self.collection.get(row.id, timeout=timedelta(seconds=2.0))
                    content = doc_result.value

                    # Remove embedding from returned content
                    if content and isinstance(content, dict) and "embedding" in content:
                        del content["embedding"]

                    documents.append({
                        "content": content,
                        "score": row.score,
                        "id": row.id
                    })
                except Exception as err:
                    print(f"Error fetching document {row.id}: {str(err)}")

            return documents

        except Exception as error:
            print(f"Error in get_relevant_documents: {str(error)}")
            raise

    async def generate_rag_response(self, messages: List[Dict[str, str]], last_message: str) -> Dict[str, Any]:
        """Generate RAG response using OpenAI API"""
        try:
            # Generate embedding for the last message
            embedding = self.generate_embedding(last_message)

            # Get relevant documents
            documents = await self.get_relevant_documents(embedding)
            print(f"Retrieved {len(documents)} documents")

            # Create prompt with context
            prompt = f"""
            You are a helpful AI assistant. Use the following pieces of context to answer the question at the end.
            If you don't know the answer, just say you don't know. DO NOT try to make up an answer.
            If the question is not related to the context, politely respond that you are tuned to only answer questions that are related to the context.
            
            <context>
            {''.join([str(doc["content"]) for doc in documents])}
            </context>
            
            Please return your answer with clear headings and lists.
            User Query: {last_message}
            """

            # Generate text response
            result = self.client.chat.completions.create(
                model="deepseek-ai/DeepSeek-R1-Distill-Llama-8B",
                messages=[*messages[:-1], {"role": "user", "content": prompt}],
                stream=True
            )

            # Generate an image based on the query (optional)
            image_url = None
            try:
                image_prompt = f"Create an image of {last_message}"
                image_response = self.client.images.generate(
                    model="black-forest-labs/flux-schnell",
                    prompt=image_prompt,
                    response_format="url",
                    size="256x256",
                    quality="standard",
                    n=1
                )
                image_url = image_response.data[0].url
                print(f"Generated image URL: {image_url}")
            except Exception as image_error:
                print(f"Error generating image: {str(image_error)}")

            return {
                "text_stream": result,
                "image_url": image_url
            }

        except Exception as e:
            print(f"Error in generate_rag_response: {str(e)}")
            raise

# Modified example usage for Google Colab
async def main():
    # Create a new RAG instance that will connect to Couchbase
    rag = CouchbaseRAG()

    messages = [
        {"role": "user", "content": "In the midst of the 10th century, about 967, which reclaimed its hereditary rule in Mecca"}
    ]

    last_message = messages[-1]["content"]

    response = await rag.generate_rag_response(messages, last_message)

    # Process streaming response
    for chunk in response["text_stream"]:
        token = chunk.choices[0].delta.content
        if token:
            print(token, end="")

    if response["image_url"]:
        print(f"\n\nImage URL: {response['image_url']}")

# For Google Colab, use this instead of asyncio.run()
if __name__ == "__main__":
    import asyncio
    import nest_asyncio

    # Apply nest_asyncio to allow running asyncio within Jupyter/Colab
    nest_asyncio.apply()

    # Now we can create and run a new event loop
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())