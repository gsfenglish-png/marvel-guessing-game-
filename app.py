import streamlit as st
import random

# A list of popular Marvel characters and their hints
# The hints are deliberately simple to make the game challenging but not impossible
MARVEL_CHARACTERS = {
    "Iron Man": {
        "hint_1": "He is a genius, billionaire, playboy, philanthropist.",
        "hint_2": "He is known for his advanced suits of armor.",
        "hint_3": "He is the founder of the Avengers in the MCU."
    },
    "Captain America": {
        "hint_1": "He was a soldier who was frozen in ice for decades.",
        "hint_2": "His primary weapon is an indestructible shield.",
        "hint_3": "His real name is Steve Rogers."
    },
    "Thor": {
        "hint_1": "He is the God of Thunder.",
        "hint_2": "He wields a mighty hammer named Mjolnir.",
        "hint_3": "He is from the realm of Asgard."
    },
    "Hulk": {
        "hint_1": "He is a scientist who turns into a giant green monster.",
        "hint_2": "His alter ego is Bruce Banner.",
        "hint_3": "His strength increases with his anger."
    },
    "Black Widow": {
        "hint_1": "She is a highly skilled spy and assassin.",
        "hint_2": "Her main weapons are a pair of electrified batons.",
        "hint_3": "Her real name is Natasha Romanoff."
    },
    "Spider-Man": {
        "hint_1": "He got his powers from a radioactive spider bite.",
        "hint_2": "He is a high school student from Queens, New York.",
        "hint_3": "He has a strong sense of responsibility, often saying 'with great power comes great responsibility'."
    },
    "Doctor Strange": {
        "hint_1": "He was a brilliant but arrogant surgeon.",
        "hint_2": "He protects Earth from mystical threats.",
        "hint_3": "He controls the Eye of Agamotto."
    },
    "Black Panther": {
        "hint_1": "He is the king of a technologically advanced African nation.",
        "hint_2": "His suit is made from Vibranium.",
        "hint_3": "His home country is Wakanda."
    },
    "Captain Marvel": {
        "hint_1": "She is an Air Force pilot with cosmic powers.",
        "hint_2": "She can fly and fire powerful energy blasts.",
        "hint_3": "Her name is Carol Danvers."
    },
    "Thanos": {
        "hint_1": "He is a powerful warlord from Titan.",
        "hint_2": "His main goal is to collect all six Infinity Stones.",
        "hint_3": "He is known for snapping his fingers to wipe out half of all life in the universe."
    }
}

# --- Game Functions ---

def new_game():
    """Resets the game state for a new round."""
    st.session_state.character = random.choice(list(MARVEL_CHARACTERS.keys()))
    st.session_state.guesses_left = 3
    st.session_state.game_over = False
    st.session_state.message = ""
    st.session_state.guess_history = []

def check_guess():
    """Checks the user's guess and updates the game state."""
    if st.session_state.game_over:
        return

    user_guess = st.session_state.user_input.strip().title()

    if user_guess == st.session_state.character:
        st.session_state.message = f"Congratulations! You guessed correctly! The character was **{st.session_state.character}**."
        st.session_state.game_over = True
    else:
        st.session_state.guesses_left -= 1
        st.session_state.guess_history.append(user_guess)
        if st.session_state.guesses_left > 0:
            st.session_state.message = f"Incorrect. You have {st.session_state.guesses_left} guesses left. Try again!"
        else:
            st.session_state.message = f"Sorry, you ran out of guesses. The character was **{st.session_state.character}**."
            st.session_state.game_over = True

# --- Streamlit UI ---

def main():
    """Main function to run the Streamlit app."""
    st.title("Guess the Marvel Character! 💥")

    # Initialize session state on the first run
    if "character" not in st.session_state:
        new_game()

    # Display hints based on remaining guesses
    st.header("Hints")
    if st.session_state.guesses_left <= 2:
        st.info(MARVEL_CHARACTERS[st.session_state.character]["hint_1"])
    if st.session_state.guesses_left <= 1:
        st.info(MARVEL_CHARACTERS[st.session_state.character]["hint_2"])
    if st.session_state.guesses_left == 0 and not st.session_state.game_over:
        st.info(MARVEL_CHARACTERS[st.session_state.character]["hint_3"])

    # Input and button for guessing
    if not st.session_state.game_over:
        st.text_input(
            "Who am I?",
            key="user_input",
            on_change=check_guess
        )
        st.write(st.session_state.message)
    else:
        st.success(st.session_state.message)

    # Display guess history
    if st.session_state.guess_history:
        st.subheader("Your Guesses")
        st.write(", ".join(st.session_state.guess_history))

    # Button to start a new game
    st.button("Play Again", on_click=new_game)

if __name__ == "__main__":
    main()
