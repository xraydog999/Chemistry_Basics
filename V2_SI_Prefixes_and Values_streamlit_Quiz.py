import streamlit as st
import random

# --- CONFIG ---
st.set_page_config(page_title="SI Prefixes")

# --- QUIZ DATA ---
# Each prefix now includes BOTH the name and the decimal multiplier
quiz_data = {
    "k": {"name": "kilo", "value": "1000"},
    "c": {"name": "centi", "value": "0.01"},
    "m": {"name": "milli", "value": "0.001"},
    "\u03bc": {"name": "micro", "value": "0.000001"},
    "n": {"name": "nano", "value": "0.000000001"},
}

# --- SESSION STATE ---
if "score" not in st.session_state:
    st.session_state.score = 0
    st.session_state.current_index = 0
    st.session_state.symbols = list(quiz_data.keys())
    random.shuffle(st.session_state.symbols)
    st.session_state.quiz_over = False
    st.session_state.results = []

st.title("SI Prefixes Quiz")
st.write(f"Score: {st.session_state.score}/{len(quiz_data)}")

# --- QUIZ OVER SCREEN ---
if st.session_state.quiz_over:
    st.success("Quiz Over!")
    st.write(f"Final Score: {st.session_state.score}/{len(quiz_data)}")

    st.subheader("Quiz Summary:")
    for result in st.session_state.results:
        symbol = result["symbol"]
        correct_name = result["correct_name"]
        correct_value = result["correct_value"]
        user_name = result["user_name"]
        user_value = result["user_value"]
        is_correct = result["is_correct"]

        if is_correct:
            st.write(f"✅ **{symbol}**: You answered '{user_name}', '{user_value}' (Correct)")
        else:
            st.write(
                f"❌ **{symbol}**: You answered '{user_name}', '{user_value}' "
                f"(Correct: '{correct_name}', '{correct_value}')"
            )

else:
    idx = st.session_state.current_index
    symbols = st.session_state.symbols

    if idx < len(symbols):
        symbol = symbols[idx]
        correct_name = quiz_data[symbol]["name"]
        correct_value = quiz_data[symbol]["value"]

        st.markdown(f"### Prefix: ${symbol}$")

        user_name = st.text_input(
            "Enter the prefix name (lowercase):",
            key=f"name_{idx}"
        )

        user_value = st.text_input(
            "Enter the decimal value:",
            key=f"value_{idx}"
        )

        if user_name and user_value:
            is_correct = (
                user_name.lower() == correct_name.lower()
                and user_value.replace(" ", "") == correct_value
            )

            st.session_state.results.append({
                "symbol": symbol,
                "correct_name": correct_name,
                "correct_value": correct_value,
                "user_name": user_name,
                "user_value": user_value,
                "is_correct": is_correct
            })

            if is_correct:
                st.success("Correct!")
                st.session_state.score += 1
                st.session_state.current_index += 1

                if st.session_state.current_index >= len(symbols):
                    st.session_state.quiz_over = True

                st.rerun()
            else:
                st.error("Incorrect. Try again.")

    else:
        st.session_state.quiz_over = True
        st.rerun()
