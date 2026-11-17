"""Lab 7 input handling by Paturu Naga Jignas (PES2UG24AM110)."""


def parse_coins(coins_csv):
    """Parse comma-separated integers, or return None for malformed input."""
    if not isinstance(coins_csv, str):
        return None
    try:
        return [int(c) for c in coins_csv.split(',')]
    except ValueError:
        return None


def slot_position(code):
    """Convert an A-Z row and positive column to zero-based coordinates."""
    if not isinstance(code, str) or len(code) < 2:
        return None
    letter = code[0]
    if not ('A' <= letter <= 'Z' or 'a' <= letter <= 'z'):
        return None
    try:
        column = int(code[1:])
    except ValueError:
        return None
    if column < 1:
        return None
    return ord(letter.upper()) - ord('A'), column - 1


def change_due(payment):
    """Return exact change in five-unit coins, or None for invalid payments."""
    if not isinstance(payment, str):
        return None
    try:
        paid_text, price_text = payment.split('/')
        paid, price = int(paid_text), int(price_text)
    except ValueError:
        return None
    if paid < 0 or price < 0 or paid < price:
        return None
    change = paid - price
    if change % 5:
        return None
    return str(change // 5) + ' five-coins'


def main():
    print("==== Running parse_coins ====")
    user_input = input("Enter coin values as CSV (e.g. 5,10,25): ")
    result = parse_coins(user_input)
    print("Coins:", result)

    print("\n==== Running slot_position ====")
    user_input = input("Enter a slot code (e.g. B7): ")
    result = slot_position(user_input)
    print("Row and Column:", result)

    print("\n==== Running change_due ====")
    user_input = input("Enter paid/price (e.g. 200/150): ")
    result = change_due(user_input)
    print("Change Due:", result)

if __name__ == "__main__":
    main()
