import streamlit as st
import random
import time

# Dictionary of Marvel characters and their hints
# The hints are structured to be revealed progressively.
MARVEL_CHARACTERS = {
    "Iron Man": {
        "hints": [
            "This character is known for their high-tech suits of armor.",
            "They are a founding member of the Avengers and are incredibly wealthy.",
            "Their alter ego's last name is Stark."
        ],
        "category": "Hero"
    },
    "Captain America": {
        "hints": [
            "This hero was enhanced by a super-soldier serum during World War II.",
            "Their main weapon is a vibranium shield.",
            "Their alter ego is Steve Rogers."
        ],
        "category": "Hero"
    },
    "Thor": {
        "hints": [
            "He is the Asgardian God of Thunder.",
            "His main weapon is a mystical hammer called Mjolnir.",
            "He is the son of Odin."
        ],
        "category": "Hero"
    },
    "Hulk": {
        "hints": [
            "This character gets stronger the angrier they get.",
            "Their alter ego is a brilliant scientist named Bruce Banner.",
            "They are famously big, green, and destructive."
        ],
        "category": "Hero"
    },
    "Black Widow": {
        "hints": [
            "She is a highly skilled spy and assassin.",
            "She was trained in the Red Room program.",
            "Her alter ego is Natasha Romanoff."
        ],
        "category": "Hero"
    },
    "Spider-Man": {
        "hints": [
            "He gained his powers after being bitten by a radioactive spider.",
            "His iconic phrase is 'With great power comes great responsibility.'",
            "His alter ego is Peter Parker."
        ],
        "category": "Hero"
    },
    "Thanos": {
        "hints": [
            "He is a powerful Titan with the goal of balancing the universe.",
            "He seeks the six Infinity Stones.",
            "He is known as the 'Mad Titan'."
        ],
        "category": "Villain"
    },
    "Loki": {
        "hints": [
            "He is known as the God of Mischief.",
            "He is the adopted brother of Thor.",
            "He is a master of illusion and deception."
        ],
        "category": "Villain"
    },
    "Magneto": {
        "hints": [
            "He is one of the most powerful mutants in the world.",
            "He has the ability to manipulate magnetic fields.",
            "He is a long-time friend and adversary of Charles Xavier."
        ],
        "category": "Villain"
    },
    "Doctor Doom": {
        "hints": [
            "He is the ruler of the fictional nation of Latveria.",
            "He is a genius inventor and sorcerer.",
            "He is the archenemy of the Fantastic Four."
        ],
        "category": "Villain"
    }
}

# --- Initialize Session State ---
def initialize_game():
    """Initializes or resets the game state in Streamlit's session state."""
    st.session_state.mode = None
    st.session_state.game_over = False
    st.session_state.result = None
    st.session_state.tries = 0
    st.session_state.user_guess_input = ""
    st.session_state.secret_character = ""
    st.session_state.hint_index = 0
    st.session_state.user_secret = ""
    st.session_state.computer_guesses = []

if "mode" not in st.session_state:
    initialize_game()

def reset_game():
    """Resets the game and re-initializes all state variables."""
    initialize_game()
    st.rerun()

def normalize_string(s):
    """Removes special characters and whitespace, and converts to lowercase for comparison."""
    if not isinstance(s, str):
        return ""
    return "".join(char for char in s if char.isalnum()).lower()

# --- Game Logic Functions ---
def handle_user_guess():
    """Handles the user's guess submission."""
    user_input = st.session_state.user_guess_input.strip()
    if not user_input:
        st.warning("Please enter a character name.")
        return

    st.session_state.tries += 1
    
    # Normalize strings for comparison
    normalized_user_input = normalize_string(user_input)
    normalized_secret = normalize_string(st.session_state.secret_character)

    if normalized_user_input == normalized_secret:
        st.session_state.game_over = True
        st.session_state.result = "win"
    else:
        if st.session_state.tries >= 15:
            st.session_state.game_over = True
            st.session_state.result = "loss"
        elif st.session_state.tries % 5 == 0 and st.session_state.hint_index < 2:
            st.session_state.hint_index += 1
        st.error("Wrong guess! Try again.")

def handle_computer_guess():
    """Handles the computer's guess submission."""
    if st.session_state.game_over:
        return
        
    st.session_state.tries += 1
    
    available_characters = [c for c in MARVEL_CHARACTERS.keys() if c not in st.session_state.computer_guesses]
    if not available_characters:
        st.session_state.game_over = True
        st.session_state.result = "loss"
        st.warning("The computer ran out of characters to guess!")
        return
        
    computer_guess = random.choice(available_characters)
    st.session_state.computer_guesses.append(computer_guess)

    # Check if computer's guess is correct
    if normalize_string(computer_guess) == normalize_string(st.session_state.user_secret):
        st.session_state.game_over = True
        st.session_state.result = "win"
    elif st.session_state.tries >= 15:
        st.session_state.game_over = True
        st.session_state.result = "loss"
    
# --- Game Mode Set-up Functions ---
def start_user_guessing_mode():
    """Starts the game where the user guesses the character."""
    st.session_state.mode = "user_guesses"
    st.session_state.game_over = False
    st.session_state.tries = 0
    st.session_state.secret_character = random.choice(list(MARVEL_CHARACTERS.keys()))
    st.session_state.hint_index = 0
    st.session_state.user_guess_input = ""
    st.rerun()

def start_computer_guessing_mode():
    """Starts the game where the computer guesses the character."""
    st.session_state.mode = "computer_guesses"
    st.session_state.game_over = False
    st.session_state.tries = 0
    st.session_state.computer_guesses = []
    st.session_state.hint_index = 0
    st.session_state.user_secret = ""
    st.rerun()

# --- UI Layout ---
st.title("Marvel Guessing Game")

if st.session_state.mode is None:
    st.write("Welcome! Please select a game mode to begin.")
    st.button("I guess the character", on_click=start_user_guessing_mode)
    st.button("The computer guesses the character", on_click=start_computer_guessing_mode)

elif st.session_state.mode == "user_guesses":
    st.header("Mode: You Guess")
    st.write("I'm thinking of a Marvel character. You have 15 tries to guess who it is!")

    if st.session_state.secret_character in MARVEL_CHARACTERS:
        hints = MARVEL_CHARACTERS[st.session_state.secret_character]["hints"]
        st.info("Hint: " + hints[st.session_state.hint_index])

    st.write(f"Tries: {st.session_state.tries}/15")

    if not st.session_state.game_over:
        st.text_input("Enter your guess:", key="user_guess_input", on_change=handle_user_guess)
        if st.session_state.tries > 0 and st.session_state.result != "win":
            st.write("Incorrect!")

    if st.session_state.game_over:
        if st.session_state.result == "win":
            st.balloons()
            st.success(f"Correct! You guessed it in {st.session_state.tries} tries. The character was {st.session_state.secret_character}!")
        else:
            st.error(f"You've run out of tries! The character was {st.session_state.secret_character}.")
        st.button("Play Again", on_click=reset_game)

elif st.session_state.mode == "computer_guesses":
    st.header("Mode: The Computer Guesses")
    
    if "user_secret" not in st.session_state or not st.session_state.user_secret:
        st.session_state.user_secret = st.text_input("First, think of a Marvel character from my list and enter it here:", key="user_secret_input")
        if st.button("Start Game"):
            if normalize_string(st.session_state.user_secret) not in [normalize_string(c) for c in MARVEL_CHARACTERS.keys()]:
                st.warning("Please choose a character from the list: " + ", ".join(MARVEL_CHARACTERS.keys()))
            else:
                st.session_state.user_secret = st.session_state.user_secret.strip()
                st.session_state.computer_guesses = []
                st.session_state.game_over = False
                st.session_state.tries = 0
                st.session_state.hint_index = 0
                st.rerun()

    if st.session_state.user_secret and not st.session_state.game_over:
        st.write(f"You have chosen **{st.session_state.user_secret}**. Now, I will guess!")
        
        st.write(f"Tries: {st.session_state.tries}/15")

        if st.button("Computer makes a guess", on_click=handle_computer_guess):
            pass  # The on_click handler does the work
        
        if st.session_state.computer_guesses:
            last_guess = st.session_state.computer_guesses[-1]
            is_correct = (normalize_string(last_guess) == normalize_string(st.session_state.user_secret))
            
            st.info(f"The computer's guess is: **{last_guess}**")

            if is_correct:
                st.session_state.game_over = True
                st.session_state.result = "win"
                st.balloons()
                st.success(f"I got it! I guessed it in {st.session_state.tries} tries.")
            elif st.session_state.tries >= 15:
                st.session_state.game_over = True
                st.session_state.result = "loss"
                st.error(f"I've failed! You win! My 15 guesses weren't enough.")
            else:
                st.error("I was wrong! Please give me a hint to help me out.")
                hints_for_character = MARVEL_CHARACTERS.get(st.session_state.user_secret, {"hints": ["No hints available."]})["hints"]
                if st.session_state.hint_index < len(hints_for_character):
                    st.write(f"**Hint {st.session_state.hint_index + 1}:** {hints_for_character[st.session_state.hint_index]}")
                    if st.button("Give me this hint", key=f"hint_{st.session_state.hint_index}"):
                        st.session_state.hint_index += 1
                        st.success("Thank you for the hint!")

    if st.session_state.game_over:
        st.button("Play Again", on_click=reset_game)

st.sidebar.button("Restart Game", on_click=reset_game)
