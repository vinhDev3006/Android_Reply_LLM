import pandas as pd
import os
import argparse


def main():
    # Add command line arguments
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input_data",
        help="Locate the downloaded review data",
        type=str,
        default=os.path.join("data", "reviews_reviews_dev.com.example_202410.csv"),
    )
    parser.add_argument(
        "-o",
        "--output_data",
        help="Location to saved the processed data",
        type=str,
        default=os.path.join("data", "october_reviews_record.csv"),
    )
    args = parser.parse_args()

    file_path = args.input_data

    # Ensure file exists
    if not os.path.exists(file_path):
        print(f"Error: File '{file_path}' does not exist.")
        return

    # Data processing
    try:
        df = pd.read_csv(file_path, encoding="utf-16")
        columns_to_anonymize = [
            "Package Name",
            "App Version Code",
            "App Version Name",
            "Reviewer Language",
            "Device",
            "Review Submit Date and Time",
            "Review Submit Millis Since Epoch",
            "Review Last Update Date and Time",
            "Review Last Update Millis Since Epoch",
            "Review Title",
            "Developer Reply Date and Time",
            "Developer Reply Millis Since Epoch",
            "Developer Reply Text",
            "Review Link",
        ]
        df[columns_to_anonymize] = "Confidential"

        output_file = args.output_data

        df.to_csv(output_file, index=False)
        print(f"Data saved to {output_file}")

    except Exception as e:
        print(f"Error processing the file: {e}")


if __name__ == "__main__":
    main()
