from dish import Dish
from edamampy import get_edamam_json
from hidden import app_id, app_key


class DishesAPIReader:
    '''Class for reading JSON-file with information about dishes'''
    def __init__(self):
        '''Create new dishes reader instance'''
        self._data = None

    def load_data(self, q=None, r=None, fromi=None, toi=None, ingr=None,
                  diet=None, health=None, calories=None, nutrients=None,
                  nutrients_range=None):
        '''Load data from API to JSON-format'''
        try:
            self._data = get_edamam_json(q, r, app_id, app_key, fromi, toi,
                                         ingr, diet, health, calories,
                                         nutrients, nutrients_range)
        except AssertionError as e:
            print(e)

    def extract_dishes(self):
        '''Extract all dishes from file and store to a list as Dish objects'''
        dishes_list = list()

        for dish in self._data['hits']:
            recipe = dish['recipe']

            name = recipe['label']
            url = recipe['url']
            image_url = recipe['image']
            portions = int(recipe['yield'])
            calories = recipe['calories']
            weight = recipe['totalWeight']
            ingredients = dict()
            for ingredient in recipe['ingredients']:
                ingredients[ingredient['text']] = ingredient['weight']
            nutrients = recipe['totalNutrients']
            daily_info = recipe['totalDaily']
            diet_labels = recipe['dietLabels']
            health_labels = recipe['healthLabels']

            dishes_list.append(Dish(name, url, image_url, portions, calories,
                                    weight, ingredients, nutrients, daily_info,
                                    diet_labels, health_labels))

        return dishes_list
