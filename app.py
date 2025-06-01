import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data.csv")

def show_summary():
    print("\n--- Summary Stats ---")
    print(df.describe())

def show_top_scorer():
    top = df.loc[df['Score'].idxmax()]
    print(f"\nTop Scorer: {top['Name']} with {top['Score']} points")

def show_average():
    avg = df['Score'].mean()
    print(f"\nAverage Score: {avg:.2f}")

def filter_by_age():
    age = int(input("Enter age to filter above: "))
    filtered = df[df['Age'] > age]
    print(f"\nPeople over {age}:")
    print(filtered)
    return filtered

def save_filtered(filtered):
    if not filtered.empty:
        filtered.to_csv("filtered_output.csv", index=False)
        print("Saved to filtered_output.csv")
    else:
        print("No data to save.")

def show_graph():
    plt.bar(df['Name'], df['Score'], color='green')
    plt.title('Scores by Name')
    plt.xlabel('Name')
    plt.ylabel('Score')
    plt.tight_layout()
    plt.show()

# Menu loop
while True:
    print("\n--- Menu ---")
    print("1. View Summary Stats")
    print("2. Show Top Scorer")
    print("3. Filter by Age")
    print("4. Save Last Filtered CSV")
    print("5. Show Graph")
    print("6. Exit")

    choice = input("Choose an option: ")
    if choice == '1':
        show_summary()
    elif choice == '2':
        show_top_scorer()
    elif choice == '3':
        filtered_df = filter_by_age()
    elif choice == '4':
        try:
            save_filtered(filtered_df)
        except:
            print("⚠️ You must filter first!")
    elif choice == '5':
        show_graph()
    elif choice == '6':
        print("Goodbye 👋")
        break
    else:
        print("Invalid choice.")
