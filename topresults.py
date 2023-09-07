import pickle
from datetime import datetime
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph
from reportlab.lib.styles import getSampleStyleSheet
import os

# Function to create the PDF report
def create_pdf_report(results):
    pdf_directory = "pdf"
    if not os.path.exists(pdf_directory):
        os.mkdir(pdf_directory)

    filename = f"{pdf_directory}/report_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.pdf"
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    story = []

    # Add a title to the PDF
    title = Paragraph(f"Cryptocurrency Position Comparison Report {datetime.now().strftime('%Y-%m-%d')}<br/><br/><br/>", styles['Title'])
    story.append(title)

    # Add the results to the PDF
    for result in results:
        text = Paragraph(result, styles['Normal'])
        story.append(text)

    doc.build(story)
    print(f"Report saved as {filename}")


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

    top_10_coins = []  # List to store the top 10 coins
    new_top_10_coins = []  # List to store up to 5 new coins in the top 10
    ascending_moved_coins = []  # List to store the top 5 ascending moved coins

    # Iterate over the coin_data_list and compare positions
    loop_count = 0  # Counter for the number of loops
    for i in range(len(coin_data_list) - 1):
        previous_data = coin_data_list[i]
        current_data = coin_data_list[i + 1]

        for previous_coin in previous_data:
            coin_name = previous_coin['CoinName']
            previous_position = previous_coin['Position']

            for current_coin in current_data:
                if current_coin['CoinName'] == coin_name:
                    current_position = current_coin['Position']

                    if previous_position != current_position:
                        if previous_position > current_position:
                            up_positions.append((coin_name, previous_position, current_position))
                        else:
                            down_positions.append((coin_name, previous_position, current_position))

        loop_count += 1  # Increment the loop count after each iteration

    # Sort the positions based on the number of positions moved
    up_positions.sort(key=lambda x: x[1] - x[2], reverse=True)
    down_positions.sort(key=lambda x: x[2] - x[1], reverse=True)

    # Get the top 10 coins
    top_10_coins = [coin for coin in current_data[:10]]

    # Find new coins in the top 10
    new_top_10_coins = [coin for coin in top_10_coins if coin['CoinName'] not in [c[0] for c in up_positions]]

    # Find the top 5 ascending moved coins
    ascending_moved_coins = up_positions[:5]

    #terminal printing and PDF creation section
    #Create a list to store the results for PDF
    results = []

    # Print the number of loops scanned
    print(f"Number of loops scanned: {loop_count}")

    # Print the top 10 coins
    print("\n\nTop 10 Coins:")
    results.append("<br/>Top 10 Coins: <br/>")
    for coin in top_10_coins:
        print(f"{coin['CoinName']} - Position: {coin['Position']}")
        results.append(f"{coin['CoinName']} - Position: {coin['Position']}")

    # Print up to 5 new coins in the top 10
    if new_top_10_coins:
        print("\n\nNew Coins in Top 10:")
        results.append("<br/>New Coins in Top 10: <br/>")
        for coin in new_top_10_coins:
            print(f"{coin['CoinName']} - Position: {coin['Position']}")
            results.append(f"{coin['CoinName']} - Position: {coin['Position']}")
            
    # Print the top 5 ascending moved coins
    if ascending_moved_coins:
        print("\n\nTop 5 Ascending Moved Coins:")
        results.append("<br/>Top 5 Ascending Moved Coins: <br/>")
        for coin in ascending_moved_coins:
            print(f"{coin[0]} - Moved Up from Position {coin[1]} to {coin[2]}")
            results.append(f"{coin[0]} - Moved Up from Position {coin[1]} to {coin[2]}")

    #Create the PDF report
    create_pdf_report(results)

# Run the position comparison
compare_positions()
