# nhl-data

Application that uses predictive modeling to predict the outcome for various NHL awards.

## How it Works

The program initially formats data from past years using Pandas dataframes. It then uses a MultiOutput Regressor from Sci-Kit Learn to train the formatted data. Then the model is tested with new data. After this is completed, the data from the current year is gathered and the program runs through each player to determine who is the closest to meeting the predicted criteria for an award, and it outputs the top 5 closest players.

## How to Run

Ensure you are in the src directory and have flask installed. Then enter the command:

```bash
flask run
```