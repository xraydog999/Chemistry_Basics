import streamlit as st

st.title("Density of Metals Quiz")
st.write("Use the given densities to answer each question:")

st.info("""
**Densities**
- Lead: 11.35 g/cm³  
- Aluminum: 2.70 g/cm³  
- Gold: 19.3 g/cm³  
""")

# Helper to check answers
def check(answer, correct):
    if answer == "":
        return ""
    return "✅ Correct!" if answer == correct else "❌ Incorrect"

# Questions
questions = [
    ("You have a 54.0 g sample of aluminum. What is its volume?",
     ["146 cm³", "20.0 cm³", "0.0500 cm³", "10.0 cm³"], "20.0 cm³"),

    ("A gold ornament has a volume of 5.00 cm³. What is its mass?",
     ["3.86 g", "10.0 g", "96.5 g", "193 g"], "96.5 g"),

    ("A block of lead has a mass of 113.5 g and a volume of 10.0 cm³. What is its density?",
     ["1135 g/cm³", "1.14 g/cm³", "11.35 g/cm³", "0.0881 g/cm³"], "11.35 g/cm³"),

    ("What is the volume of a 38.6 g gold coin?",
     ["745 cm³", "0.500 cm³", "2.00 cm³", "10.0 cm³"], "2.00 cm³"),

    ("You have an aluminum rod with a volume of 15.0 cm³. What is its mass?",
     ["40.5 g", "5.56 g", "0.180 g", "27.0 g"], "40.5 g"),

    ("A sample of aluminum has a mass of 8.10 g and a volume of 3.00 cm³. What is its density?",
     ["24.3 g/cm³", "2.70 g/cm³", "0.370 g/cm³", "19.3 g/cm³"], "2.70 g/cm³"),

    ("What is the volume of a 22.7 g sample of lead?",
     ["2.00 cm³", "258 cm³", "0.500 cm³", "10.0 cm³"], "2.00 cm³"),

    ("Calculate the mass of a 4.00 cm³ piece of lead.",
     ["45.4 g", "2.84 g", "11.4 g", "2.70 g"], "45.4 g"),

    ("A gold ingot has a mass of 193 g and a volume of 10.0 cm³. What is its density?",
     ["1930 g/cm³", "0.0518 g/cm³", "19.3 g/cm³", "11.4 g/cm³"], "19.3 g/cm³"),

    ("What is the volume of a 13.5 g piece of aluminum?",
     ["36.5 cm³", "5.00 cm³", "0.200 cm³", "10.0 cm³"], "5.00 cm³"),
]

# Render quiz
for i, (q, options, correct) in enumerate(questions, start=1):
    st.subheader(f"Question {i}")
    st.write(q)
    answer = st.radio("Choose an answer:", [""] + options, key=f"q{i}")
    st.write(check(answer, correct))
    st.markdown("---")
