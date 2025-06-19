def electronics_quiz_game():
    score = 0
    questions = [
        {
            "question": "Which component is used to store electrical energy?",
            "options": ["A) Resistor", "B) Inductor", "C) Capacitor", "D) Diode"],
            "answer": "C"
        },
        {
            "question": "What does LED stand for?",
            "options": ["A) Light Emitting Diode", "B) Low Energy Diode", "C) Light Energy Detector", "D) Linear Electric Device"],
            "answer": "A"
        },
        {
            "question": "Which logic gate gives a high output only when both inputs are high?",
            "options": ["A) OR", "B) AND", "C) XOR", "D) NAND"],
            "answer": "B"
        },
        {
            "question": "The unit of inductance is?",
            "options": ["A) Henry", "B) Farad", "C) Ohm", "D) Tesla"],
            "answer": "A"
        },
        {
            "question": "Which of the following is NOT a semiconductor material?",
            "options": ["A) Silicon", "B) Germanium", "C) Copper", "D) Gallium Arsenide"],
            "answer": "C"
        },
        {
            "question": "What is the main use of a resistor in a circuit?",
            "options": ["A) To store charge", "B) To oppose current flow", "C) To amplify signal", "D) To emit light"],
            "answer": "B"
        },
        {
            "question": "What is the main use of a capacitor in a circuit?",
            "options": ["A) To store electrical energy", "B) To emit light", "C) To amplify signals", "D) To reduce resistance"],
            "answer": "A"
        },
        {
            "question": "What is the unit of resistance?",
            "options": ["A) Farad", "B) Ohm", "C) Henry", "D) Tesla"],
            "answer": "B"
        },
        {
            "question": "What is the primary use of Raspberry Pi?",
            "options": ["A) To store large amounts of data", "B) As a programmable microcomputer for various projects", "C) As a power supply", "D) As a display screen"],
            "answer": "B"
        }
    ]

    print("Welcome to the Extended Electronics Quiz Game!")
    print("--------------------------------------------\n")

    for i, q in enumerate(questions):
        print(f"Q{i+1}: {q['question']}")
        for option in q['options']:
            print(option)
        
        answer = input("Your answer (A/B/C/D): ").upper()

        if answer == q['answer']:
            print("✅ Correct!\n")
            score += 1
        else:
            print(f"❌ Wrong! The correct answer was {q['answer']}.\n")

    print(f"Quiz Over! Your final score is: {score}/{len(questions)}")


electronics_quiz_game()
