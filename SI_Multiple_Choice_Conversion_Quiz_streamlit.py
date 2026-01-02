import streamlit as st
import random

st.set_page_config(page_title="SI Conversion Multiplier Quiz")

# --- PREFIX DATA ---
prefixes = {
    "k": 1_000,
    "c": 0.01,
    "m": 0.001,
    "µ": 0.000001,
    "n": 0.000000001
}

prefix_names = {
    "k": "kilo",
    "c": "centi",
    "m": "milli",
    "µ": "micro",
    "n": "nano"
}

# --- SESSION STATE ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_number = 0
    st.session_state.quiz_over = False
    st.session_state.results = []
    st.session_state.total_questions = 10
    st.session_state.current_question = None
    st.session_state.correct_choice = None
    st.session_state.choices = None

st.title("SI Conversion Multiplier Quiz")
st.write(f"Score: {st.session_state.score}/{st.session_state.total_questions}")

# --- FUNCTION TO GENERATE QUESTION ---
def generate_question():
    from_p = random.choice(list(prefixes.keys()))
    to_p = random.choice(list(prefixes.keys()))

    while to_p == from_p:
        to_p = random.choice(list(prefixes.keys()))

    # Correct multiplier
    multiplier = prefixes[from_p] / prefixes[to_p]

    # Generate distractors
    distractors = set()
    while len(distractors) < 3:
        factor = random.choice([0.001, 0.01, 0.1, 10, 100, 1000, 1e6, 1e-6])
        if factor != multiplier:
            distractors.add(factor)

    all_choices = list(distractors) + [multiplier]
    random.shuffle(all_choices)

    labels = ["a", "b", "c", "d"]
    choice_map = {labels[i]: all_choices[i] for i in range(4)}

    correct_label = [k for k, v in choice_map.items() if v == multiplier][0]

    question_text = (
        f"To convert **{prefix_names[from_p]} ({from_p})** to "
        f"**{prefix_names[to_p]} ({to_p})**, which multiplier is used?"
    )

    return question_text, choice_map, correct_label

# --- QUIZ OVER ---
if st.session_state.quiz_over:
    st.success("Quiz Complete!")
    st.write(f"Final Score: {st.session_state.score}/{st.session_state.total_questions}")

    st.subheader("Summary")
    for r in st.session_state.results:
        if r["correct"]:
            st.write(f"✅ {r['question']} → You chose: {r['user']} (Correct)")
        else:
            st.write(
                f"❌ {r['question']} → You chose: {r['user']} "
                f"(Correct: {r['correct']})"
            )

    if st.button("Restart quiz"):
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.stop()

# --- ENSURE QUESTION EXISTS ---
if st.session_state.current_question is None:
    q, choices, correct = generate_question()
    st.session_state.current_question = q
    st.session_state.choices = choices
    st.session_state.correct_choice = correct

# --- DISPLAY QUESTION ---
st.subheader(st.session_state.current_question)

choice_labels = list(st.session_state.choices.keys())
choice_strings = [
    f"{label}) {st.session_state.choices[label]}"
    for label in choice_labels
]

user_choice = st.radio("Select your answer:", choice_strings)

if st.button("Submit"):
    selected_label = user_choice.split(")")[0]

    is_correct = (selected_label == st.session_state.correct_choice)

    st.session_state.results.append({
        "question": st.session_state.current_question,
        "user": selected_label,
        "correct": st.session_state.correct_choice,
        "correct_bool": is_correct
    })

    if is_correct:
        st.success("Correct!")
        st.session_state.score += 1
    else:
        st.error(f"Incorrect. Correct answer: {st.session_state.correct_choice}")

    # Move to next question
    st.session_state.question_number += 1

    if st.session_state.question_number >= st.session_state.total_questions:
        st.session_state.quiz_over = True
    else:
        q, choices, correct = generate_question()
        st.session_state.current_question = q
        st.session_state.choices = choices
        st.session_state.correct_choice = correct

    st.rerun()
