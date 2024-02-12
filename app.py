
# Replace 'your-api-key' with your actual OpenAI API key
import sqlite3
import openai

# Function to initialize the SQLite database
def initialize_database():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY,
            user_message TEXT,
            ai_response TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Function to save chat to the database
def save_chat_to_database(user_message, ai_response):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO chat_history (user_message, ai_response) VALUES (?, ?)
    ''', (user_message, ai_response))
    conn.commit()
    conn.close()

def chat_with_girlfriend(prompt):
    try:
        openai.api_key = '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'

        # Adjusting the parameters as needed
        response = openai.Completion.create(
          engine="gpt-3.5-turbo-instruct",  # Choose the model
          prompt=prompt,
          max_tokens=150,
           temperature=0.7,  # Adjusting for more creative responses
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6 
          #gpt-3.5-turbo-instruct, babbage-002, davinci-002# Maximum length of the response
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return f"An error occurred: {e}"

def main():
    initialize_database()
    print(" How can I help you today?")
    chat_history = "you are frinted therapist"

    while True:
        user_input = input("You: ")
        chat_history += "You: " + user_input 
        response = chat_with_girlfriend(chat_history)
        print( response)
        chat_history += response

        save_chat_to_database(user_input, response)

        if 'goodbye' in user_input.lower():
            break

if __name__ == "__main__":
    main()

