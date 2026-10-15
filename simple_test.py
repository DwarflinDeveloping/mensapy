from client import MensaSession
from mensa import Mensa
from utils import mass_like

if __name__ == '__main__':
    my_mensa = MensaSession()
    meals = my_mensa.load_speiseplan(Mensa.MENSA_ERNST_ABBE_PLATZ)
    my_meal = meals[2]

    max_votes = 5
    print(my_meal.likes)

    if my_meal.likes >= max_votes:
        print(f'This Gericht already has {max_votes} votes or more!')
        exit(0)

    print(f'Starting to like for "{my_meal.name}"...')
    for n, new_votes in enumerate(mass_like(my_mensa, my_meal, None)):
        print(f'{new_votes}/{max_votes}')
        if new_votes >= max_votes:
            break
