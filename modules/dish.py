from copy import deepcopy


class Dish:
    '''Class representing a dish'''
    def __init__(self, name, url, image_url, portions, calories, weight,
                 ingredients, nutrients, daily_info, diet_labels,
                 health_labels):
        '''Create new Dish instance'''
        if not isinstance(name, str):
            raise TypeError('Wrong type of name')
        self._name = name

        if not isinstance(url, str):
            raise TypeError('Wrong type of url')
        self._url = url

        if not isinstance(image_url, str):
            raise TypeError('Wrong type of image url')
        self._image_url = image_url

        if not isinstance(portions, int):
            raise TypeError('Wrong type of portions')
        self._portions = portions

        if not isinstance(calories, (int, float)):
            raise TypeError('Wrong type of calories')
        self._calories = calories

        if not isinstance(weight, (int, float)):
            raise TypeError('Wrong type of weight')
        self._weight = weight

        if not isinstance(ingredients, dict):
            raise TypeError('Wrong type of ingredients')
        self._ingredients = deepcopy(ingredients)

        if not isinstance(nutrients, dict):
            raise TypeError('Wrong type of nutrients')
        self._nutrients = deepcopy(nutrients)

        if not isinstance(daily_info, dict):
            raise TypeError('Wrong type of daily information')
        self._daily_info = deepcopy(daily_info)

        if not isinstance(diet_labels, list):
            raise TypeError('Wrong type of diet labels')
        self._diet_labels = diet_labels

        if not isinstance(health_labels, list):
            raise TypeError('Wrong type of health labels')
        self._health_labels = health_labels

    def __str__(self):
        """ Return str(self). """
        return 'NAME: {}\nNUMBER OF PORTIONS: {}\nCALORIES: {}\nWEIGHT: {}\n' \
               'INGREDIENTS: {}\nNUTRIENTS: {}\nDIET LABELS: {}\n' \
               'HEALTH LABELS: {}\n\n'.format(self._name, self._portions,
                                              self._calories, self._weight,
                                              ', '.join(self.get_ingredients()),
                                              ', '.join(self.get_nutrients()),
                                              ', '.join(self._diet_labels),
                                              ', '.join(self._health_labels))

    def __repr__(self):
        """ Return repr(self). """
        return self._name

    def get_ingredients(self):
        return list(self._ingredients.keys())

    def get_nutrients(self):
        return list(self._nutrients.keys())
