from src.crawler import analyze_website
import pandas as pd
import os


# Ask user for website
website = input("Enter website URL: ")

# Analyze website
result = analyze_website(website)


if result:

    # Convert result into Pandas DataFrame
    df = pd.DataFrame([result])

    print("\nWebsite Data:")
    print("-" * 50)
    print(df)

    # Make sure data folder exists
    os.makedirs("data", exist_ok=True)

    # Save data to CSV
    file_path = "data/website_data.csv"

    df.to_csv(
        file_path,
        index=False
    )

    print("\nData saved successfully!")
    print(f"File: {file_path}")