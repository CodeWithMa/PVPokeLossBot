import start_state

# Initialize the state machine
current_state = start_state

try:
    # Run the state machine
    while not current_state is None:
        current_state = current_state.run()
except KeyboardInterrupt:
    print("Exiting program...")
