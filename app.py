
import streamlit as st
import requests
import json

st.set_page_config(
    page_title="AI Quiz Generator",
    page_icon="📝",
    layout="centered"
)

st.title("📝 AI Quiz Generator")
st.write("Generate quizzes on any topic using AI!")

topic = st.text_input(
    "Enter Quiz Topic",
    placeholder="Example: Python, Machine Learning, Django"
)

difficulty = st.selectbox(
    "Select Difficulty",
    ["Beginner", "Intermediate", "Advanced"]
)

num_questions = st.number_input(
    "Number of Questions",
    min_value=1,
    max_value=20,
    value=5
)


def generate_quiz(topic, difficulty, num_questions):

    api_key = st.secrets["OPENROUTER_API_KEY"]

    url = "https://openrouter.ai/api/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    prompt = f"""
    Generate {num_questions} multiple choice quiz questions
    about {topic}.

    Difficulty: {difficulty}

    Return only valid JSON in this format:

    {{
        "questions": [
            {{
                "question": "What is Python?",
                "options": [
                    "Programming language",
                    "Database",
                    "Browser",
                    "Operating System"
                ],
                "answer": "Programming language",
                "explanation": "Python is a programming language."
            }}
        ]
    }}
    """

    payload = {
        "model": "openai/gpt-4o-mini",
        "messages": [
            {
                "role": "user",
                "content": prompt
            }
        ],
        "temperature": 0.7
    }

    response = requests.post(
        url,
        headers=headers,
        json=payload,
        timeout=60
    )

    response.raise_for_status()

    data = response.json()

    content = data["choices"][0]["message"]["content"]

    quiz = json.loads(content)

    return quiz


if st.button("Generate Quiz"):

    if not topic.strip():
        st.warning("Please enter a topic!")

    else:
        try:
            with st.spinner("Generating your quiz..."):

                quiz = generate_quiz(
                    topic,
                    difficulty,
                    num_questions
                )

            st.success("Quiz generated successfully!")

            st.json(quiz)

        except requests.exceptions.RequestException as e:
            st.error(f"API Error: {e}")

        except (KeyError, ValueError) as e:
            st.error(f"Response Error: {e}")

        except Exception as e:
            st.error(f"Something went wrong: {e}")

