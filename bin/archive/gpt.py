#Reference: https://github.com/openai/openai-python/issues/271

import openai

# Set up your OpenAI API credentials
openai.api_key = '****'

# Make a request to the API
completion = openai.ChatCompletion.create(
  model="gpt-3.5-turbo",
  messages=[{"role": "user", "content": "Tell the world about the ChatGPT API in the style of a pirate."}]
)

# Access the generated response
print (completion)
generated_text = completion.choices[0].message.content.strip()

# Print the generated text
print(generated_text)