from openai import OpenAI
import numpy as np
import json

client = OpenAI()

users_json = '''[
    {
        "name": "Viki",
        "topics": ["Fintech", "Politcis", "Books", "Startups"],
        "personality": ["Avid reader", "Focused", "Indoor person", "casual", "MBA"]
    },
    {
        "name": "Smitha",
        "topics": ["Plants", "Ecofriendly", "Biryani"],
        "personality": ["Chill", "Clean freak", "Meghana biryani lover", "Mother of 11 year old boy", "MBA"]
    },
    {
        "name": "Bharath",
        "topics": ["AI/ML", "AWS", "Travelling", "New cuisines"],
        "personality": ["Calm", "Talented", "Fun"]

    },
    {
        "name": "Gt",
        "topics": ["AI/ML", "South Indian food", "Madhwa", "Coffee"],
        "personality": [ "Talented", "sarcastic", "funny", "smart", "Pro hindu", "Space tech"]
    },
    {
        "name": "Chandana",
        "topics": ["Traveller", "Pani Poori", "snacks, Chats"],
        "personality": ["Funny", "outdoor person", "casual", "chill"]
    },    
    {
        "name": "Hemanth",
        "topics": ["Entrepreneur", "Business", "Startups", "Foodie", "Coffee lover", "Infra & Interiors business"],
        "personality": ["Funny", "Enthusiastic", "Independent", "busy bee", "calm & composed"]
    }
]'''

def get_all_users():
    return json.loads(users_json)

def get_embedding(text, model="text-embedding-ada-002"):
    response = client.embeddings.create(input=[text], model=model)  # Ensure input is a list
    embedding = response.data[0].embedding  # Correct way to access data
    return np.array(embedding)


def cosine_similarity(vec1, vec2):
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

def find_relevant_users(sentence, users, top_n=1):
    sentence_embedding = get_embedding(sentence)
    user_scores = []
    
    for user in users:
        user_text = user["name"] + " " + ", ".join(user["topics"] + user["personality"])
        user_embedding = get_embedding(user_text)
        similarity = cosine_similarity(sentence_embedding, user_embedding)
        user_scores.append((user["name"], similarity))
    
    user_scores.sort(key=lambda x: x[1], reverse=True)
    return [user[0] for user in user_scores[:top_n]]


def get_most_relevant_user(sentence):
    users = json.loads(users_json)
    relevant_users = find_relevant_users(sentence, users)
    return relevant_users[0]


def get_reply(user_name, sentence):
    user_props = [user for user in json.loads(users_json) if user["name"] == user_name][0]
    system_prompt = "you are a user with this attributes " + str(user_props) + "given the topic/conversation - " + sentence + " what is your reply? "

    completion = client.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": "you are a user with this attributes " + str(user_props) + "given the topic/conversation, what is your reply? "},
        {"role": "user", "content": f"sentence/message: "+sentence}
    ]
    )
    response = completion.choices[0].message.content
    return response

    # print("response",response)


