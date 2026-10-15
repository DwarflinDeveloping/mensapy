from client import MensaSession
from mensa import Mensa
from utils import mass_like

"""Testing script written by AI"""


def main():
    # 1. Select a Mensa from the Mensa IntEnum
    print("Available Mensen:")
    for mensa in Mensa:
        print(f"[{mensa.value}] {mensa.name}")

    try:
        chosen_id = int(input("\nEnter the ID of the Mensa you want to select: "))
        selected_mensa_enum = Mensa(chosen_id)
    except (ValueError, KeyError):
        print("Invalid Mensa ID selected.")
        return

    # Initialize the session
    my_mensa = MensaSession()

    print(f"\nLoading meal plan for {selected_mensa_enum.name}...")
    meals = my_mensa.load_speiseplan(selected_mensa_enum)

    if not meals:
        print("No meals found for today.")
        return

    print(f"\nFound {len(meals)} meals today:")
    for idx, meal in enumerate(meals):
        print(f"  [{idx}] Gebinde: {meal.gebinde} - {meal.name} (Likes: {meal.likes})")

    # 2. Select a meal by index or gebinde
    try:
        meal_idx = int(input("\nEnter the index of the meal you want to inspect/like: "))
        my_meal = meals[meal_idx]
    except (ValueError, IndexError):
        print("Invalid meal selection.")
        return

    # 3. Show information about the selected meal
    print("\n--- Meal Information ---")
    print(f"Name: {my_meal.name}")
    print(f"Gebinde: {my_meal.gebinde}")
    print(f"RSCID: {my_meal.rscid}")
    print(f"Current Likes: {my_meal.likes}")
    print(f"Price (Student/Bedienstet/Gast): {my_meal.price_student}€ / {my_meal.price_bedienstet}€ / {my_meal.price_gast}€")
    if my_meal.komponenten:
        print(f"Components: {', '.join(my_meal.komponenten)}")
    if my_meal.allergene:
        print(f"Allergens: {', '.join(my_meal.allergene)}")
    if my_meal.co2_equivalent:
        print(f"CO2 Equivalent: {my_meal.co2_equivalent}g")

    # 4. Target amount of likes
    try:
        max_votes = int(input("\nEnter the target amount of likes you want to reach: "))
    except ValueError:
        print("Invalid number entered.")
        return

    current_likes = my_meal.likes if my_meal.likes is not None else 0

    if current_likes >= max_votes:
        print(f'This Gericht already has {current_likes} votes, which meets or exceeds your target of {max_votes}!')
        return

    # 5. Mass like utilizing mass_like
    print(f'Starting to like for "{my_meal.name}"...')
    for n, new_votes in enumerate(mass_like(my_mensa, my_meal, None)):
        print(f'{new_votes}/{max_votes}')
        if new_votes >= max_votes:
            break


if __name__ == "__main__":
    main()