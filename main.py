import ingame_state

# Initialize the state machine
current_state = ingame_state

try:
    # Run the state machine
    while not current_state is None:
        current_state = current_state.run()
except KeyboardInterrupt:
    print("")
    print("Exiting program...")
