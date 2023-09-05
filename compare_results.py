import pickle

def compare_positions():
    # Load the coin_data_list from the pickle file
    try:
        with open('coin_data_list.pkl', 'rb') as file:
            coin_data_list = pickle.load(file)
    except FileNotFoundError:
        print("Coin data file not found.")
        return

    up_positions = []   # List to store coins that moved up
    down_positions = []   # List to store coins that moved down


    # Iterate over the coin_data_list and compare positions
    loop_count = 0  # Counter for the number of loops
    for i in range(len(coin_data_list) - 1):
        previous_data = coin_data_list[i]
        current_data = coin_data_list[i + 1]

        for previous_coin in previous_data:
            coin_name = previous_coin['CoinName']
            previous_position = previous_coin['Position']
            previous_timestamp = previous_coin["Timestamp"]

            for current_coin in current_data:
                if current_coin['CoinName'] == coin_name:
                    current_position = current_coin['Position']
                    current_timestamp = current_coin["Timestamp"]

                    if previous_position != current_position:
                        if previous_position > current_position:
                            up_positions.append((coin_name, previous_position, current_position, previous_timestamp, current_timestamp))
                        else:
                            down_positions.append((coin_name, previous_position, current_position, previous_timestamp, current_timestamp))

        loop_count += 1  # Increment the loop count after each iteration


    # Sort the positions based on the number of positions moved
    up_positions.sort(key=lambda x: x[1] - x[2], reverse=True)
    down_positions.sort(key=lambda x: x[2] - x[1], reverse=True)

    # Print the number of loops scanned
    print(f"Number of loops scanned: {loop_count}")

    # Print the positions that went up
    if up_positions:
        print()
        print("UP positions:")
        for coin in up_positions:
            message = f"{coin[0]} moved up from position {coin[1]} to {coin[2]} at {coin[4]}."
            print(message)

    # Print the positions that went down
    if down_positions:
        print()
        print("DOWN positions:")
        for coin in down_positions:
            message = f"{coin[0]} moved down from position {coin[1]} to {coin[2]} at {coin[4]}."
            print(message)

# Run the position comparison
compare_positions()