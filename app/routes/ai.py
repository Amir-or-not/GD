import google.generativeai as genai

genai.configure(api_key="AIzaSyC1yUKKBcQVh5eWnWt0EAYfFcusdWK9aHM")

model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

i = str.lower(input())

response = model.generate_content(i)

print(response.text)


# import google.generativeai as genai

# genai.configure(api_key="AIzaSyC1yUKKBcQVh5eWnWt0EAYfFcusdWK9aHM")

# model = genai.GenerativeModel(model_name="models/gemini-1.5-pro-latest")

# def async getresponse(text):
#     response = str(model.generate_content(text))
#     return response

# print(getresponse('kaka')) 