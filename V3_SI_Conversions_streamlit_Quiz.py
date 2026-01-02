import streamlit as st
import random

st.set_page_config(page_title="SI Conversion Quiz")

# --- PREFIX DATA ---
prefixes = {
    "k": 1_000,
    "c": 0.01,
    "m": 0.001,
    "µ": 0.000001,
    "n": 0.000000001
}

units = ["m"]  # You can later add "g", "L", etc.

# --- SESSION STATE INITIALIZATION ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.question_number = 0
    st.session_state.quiz_over = False
    st.session_state.results = []
    st.session_state.total_questions = 8
    st.session_state.current_question = None
    st.session_state.correct_value = None
    st.session_state.correct_unit = None

st.title("SI Unit Conversion Quiz")
st.write(f"Score: {st.session_state.score}/{st.session_state.total_questions}")

# --- FUNCTION TO GENERATE A NEW QUESTION ---
def generate_question():
    value = random.choice([1, 2, 5, 10, 20, 50])
    from_prefix = random.choice(list(prefixes.keys()))
    to_prefix = random.choice(list(prefixes.keys()))
    base_unit = random.choice(units)

    # Avoid same-prefix conversions
    while to_prefix == from_prefix:
        to_prefix = random.choice(list(prefixes.keys()))

    question_text = f"Convert {value} {from_prefix}{base_unit} to {to_prefix}{base_unit}"

    # Compute correct answer
    base_value = value * prefixes[from_prefix]
    converted_value = base_value / prefixes[to_prefix]

    return question_text, converted_value, f"{to_prefix}{base_unit}"

# --- QUIZ OVER SCREEN ---
if st.session_state.quiz_over:
    st.success("Quiz Complete!")
    st.write(f"Final Score: {st.session_state.score}/{st.session_state.total_questions}")

    st.subheader("Summary")
    for r in st.session_state.results:
        if r["correct"]:
            st.write(f"✅ {r['question']} → You answered: {r['user']} (Correct)")
        else:
            st.write(
                f"❌ {r['question']} → You answered: {r['user']} "
                f"(Correct: {r['correct_answer']})"
            )

    if st.button("Restart quiz"):
        # Reset everything
        for key in list(st.session_state.keys()):
            del st.session_state[key]
        st.rerun()

    st.stop()

# --- ENSURE WE HAVE A CURRENT QUESTION ---
if st.session_state.current_question is None:
    q, ans_value, ans_unit = generate_question()
    st.session_state.current_question = q
    st.session_state.correct_value = ans_value
    st.session_state.correct_unit = ans_unit

st.subheader(st.session_state.current_question)

# --- FORM FOR CONTROLLED SUBMISSION ---
with st.form(key="answer_form"):
    user_value = st.text_input("Numeric value:")
    user_unit = st.text_input("Unit (e.g., m, km, mm):")
    submitted = st.form_submit_button("Submit")

if submitted:
    if not user_value or not user_unit:
        st.error("Please enter both a numeric value and a unit.")
    else:
        try:
            numeric = float(user_value)
            correct_numeric = abs(numeric - st.session_state.correct_value) < 1e-9
            correct_unit = (user_unit.strip() == st.session_state.correct_unit)

            is_correct = correct_numeric and correct_unit

            # Store result
            st.session_state.results.append({
                "question": st.session_state.current_question,
                "user": f"{user_value} {user_unit}",
                "correct_answer": f"{st.session_state.correct_value} {st.session_state.correct_unit}",
                "correct": is_correct
            })

            if is_correct:
                st.success("Correct!")
                st.session_state.score += 1
            else:
                st.error(
                    f"Incorrect. Correct answer: "
                    f"{st.session_state.correct_value} {st.session_state.correct_unit}"
                )

            # Move to next question
            st.session_state.question_number += 1

            if st.session_state.question_number >= st.session_state.total_questions:
                st.session_state.quiz_over = True
            else:
                # Generate next question
                q, ans_value, ans_unit = generate_question()
                st.session_state.current_question = q
                st.session_state.correct_value = ans_value
                st.session_state.correct_unit = ans_unit

            st.rerun()

        except ValueError:
            st.error("Please enter a valid number.")
