from chatterbot import chatbot
from chatterbot.trainers import ListTrainer
 
#creating a new chatbot
chatbot = Chatbot('Edureka')
trainer = ListTrainer(chatbot)
trainer.train(['hi, can I help you find a course', 'sure I\'d love to find you a course', 'your course have been selected'])
 
#getting a response from the chatbot
response = chatbot.get_response("I want a course")
print(response)