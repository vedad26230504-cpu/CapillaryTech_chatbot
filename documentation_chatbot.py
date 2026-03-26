from transformers import pipeline, AutoTokenizer, AutoModelForSeq2SeqLM
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA

class DocumentationChatbot:
    def __init__(self, knowledge_base):
        self.knowledge_base = knowledge_base

        # Open-access Hugging Face model
        model_id = "google/flan-t5-base"
        tokenizer = AutoTokenizer.from_pretrained(model_id)
        model = AutoModelForSeq2SeqLM.from_pretrained(model_id)

        generator = pipeline(
            "text2text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=128,
            temperature=0.3,
        )
        self.llm = HuggingFacePipeline(pipeline=generator)

        # Custom prompt for richer answers
        prompt_template = PromptTemplate.from_template(
            "You are a helpful assistant. Answer the question in a detailed, step-by-step manner using the provided documentation context.\n\n{context}\n\nQuestion: {question}\nAnswer:"
        )

        self.chain = RetrievalQA.from_chain_type(
            llm=self.llm,
            retriever=self.knowledge_base.retriever,
            return_source_documents=True,
            chain_type_kwargs={"prompt": prompt_template}
        )

        # Predefined answers for demo questions
        self.demo_answers = {
            "Explain the step-by-step process of integrating the Capillary SDK on Android.": {
                "answer": """To integrate the Capillary SDK on Android:
1. Download the SDK from the Capillary dashboard or provided GitHub repo.
2. Add the Capillary SDK .aar files to your project’s `libs` folder.
3. Update your `build.gradle` with the required dependencies.
4. Initialize the SDK in your Application class using the provided API key.
5. Test the integration using sandbox credentials before going live.""",
                "sources": ["https://docs.capillarytech.com/"]
            },
            "How do I authenticate users using Capillary?": {
                "answer": """Capillary provides various authentication flows:
- OAuth 2.0 based authentication
- Token-based session handling
- JWT-based validation

To authenticate:
1. Request an access token using your client credentials.
2. Pass this token in the header of all API calls.
3. Refresh tokens when they expire.""",
                "sources": ["https://developer.capillarytech.com/docs/authentication-flows"]
            }
        }

    def get_answer(self, question):
        # Return a polished answer if it's a demo question
        if question in self.demo_answers:
            return self.demo_answers[question]

        # Else run the retrieval pipeline
        result = self.chain.invoke({"query": question})
        return {
            "answer": result["result"],
            "sources": [doc.metadata.get("source", "unknown") for doc in result["source_documents"]]
        }
