question = "What are the different modules offered by the Capillary Loyalty system?"
response = chatbot.get_answer(question)

print(" Answer:", response["answer"])
print(" Sources:", response["sources"])
