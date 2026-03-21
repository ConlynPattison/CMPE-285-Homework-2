import yfinance as yf

from datetime import datetime


def main():
    while True:
        symbol = input_handler()
        details = fetch_stock_details(symbol)

        if not details:
            print("Invalid stock ticker symbol provided.\n")
            continue

        print(f"\n{details["datetime"]}", end="\n\n")
        print(details["name"], end="\n\n")

        change = f"+{details['change']:.2f}" if details['change'] > 0 else f"{details['change']:.2f}"
        print(f"${details['price']:.2f} {change} ({details['change_percent']:.2f}%)", end="\n\n")


def input_handler() -> str:
    print("Please enter a symbol: ")
    symbol = input().strip()

    if len(symbol) < 1:
        print("Symbol must be at least 1 character long.\n")
        return input_handler()

    if len(symbol) > 5:
        print("Symbol cannot be longer than 5 characters.\n")
        return input_handler()
    
    return symbol


def fetch_stock_details(symbol: str) -> dict | None:
    ticker = yf.Ticker(symbol)
    info = ticker.info

    # Info not present for non-equity tickers (e.g., ETF, mutual fund, etc.)
    if not info["quoteType"] == "EQUITY":
        return None
    
    current_datetime = datetime.now()
    formatted_datetime = current_datetime.strftime("%a %b %d %X %p %Y")

    name = info.get("longName", None)
    if not name:
        name = info.get("displayName", "Unnamed Stock")

    return {
        "datetime": formatted_datetime,
        "name": f"{name} ({symbol.upper()})",
        "price": info.get("regularMarketPrice", "N/A"),
        "change": info.get("regularMarketChange", "N/A"),
        "change_percent": info.get("regularMarketChangePercent", "N/A"),
    }


if __name__ == "__main__":
    main()
