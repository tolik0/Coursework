import requests
import re


def get_edamam_json(q=None, r=None, app_id=None, app_key=None, fromi=None,
                    toi=None, ingr=None, diet=None, health=None, calories=None,
                    nutrients=None, nutrients_range=None):
    """
    Receive dict from JSON format file returned by Edamam API
    :param q: text to query(str)
    :param r: id to query(str)
    :param app_id: application id(str)
    :param app_key: application key(str)
    :param fromi: first result index(int)
    :param toi: first result index(int)
    :param ingr: maximum number of ingredients(int)
    :param diet: diet label(str)
    :param health: health label(str)
    :param calories: calories per serving in format of “lte U” or “gte L”,
               “gte L, lte U”(str) where U and L are lower and upper bound(str)
    :param nutrients: labels of nutrients(list)
    :param nutrients_range: list of ranges for corresponding nutrients(list)
    :return: dictionary from JSON file received
    """
    # check if arguments are correct
    assert bool(q) != bool(r), 'Exactly one parameter q/r should be specified'
    assert app_id and app_key, 'Application id and key must be specified'
    if q:
        assert isinstance(q, str), 'q must be a string'
    if r:
        assert isinstance(r, str), 'r must be a string'
    assert isinstance(app_key, str), 'app_key must be integer'
    assert isinstance(app_id, str), 'app_id must be integer'
    if fromi is not None:
        assert isinstance(fromi, int) and fromi >= 0, 'fromi must be integer'
    if toi is not None:
        assert isinstance(toi, int) and toi >= 0, 'toi must be integer'
    if ingr:
        assert isinstance(ingr, int) and ingr > 0, 'ingr must be integer'
    if diet:
        assert isinstance(diet, list), 'diet must be of type list'
        diet_labels = ['balanced', 'high-protein', 'high-fiber', 'low-fat',
                       'low-carb,' 'low-sodium']
        assert all(x in diet_labels for x in diet), \
            'all diet labels must be from {}'.format(diet_labels)
    if health:
        assert isinstance(health, list), 'health must be of type list'
        health_labels = ['vegan', 'vegetarian', 'paleo', 'dairy-free',
                         'gluten-free', 'wheat-free', 'fat-free', 'low-sugar',
                         'egg-free', 'peanut-free', 'tree-nut-free',
                         'soy-free', 'fish-free', 'shellfish-free',
                         'alcohol-free', 'celery-free', 'crustacean-free',
                         'kidney-friendly', 'kosher', 'low-potassium',
                         'lupine-free', 'mustard-free', 'No-oil-added',
                         'pescatarian', 'pork-free', 'red-meat-free',
                         'sesame-free', 'sugar-conscious']
        assert all(x in health_labels for x in health), \
            'all health labels must be from {}'.format(health_labels)
    if calories:
        assert any(re.match(regex, calories)
                   for regex in [r'^lte [0-9]+$', r'^gte [0-9]+$',
                                 r'^gte [0-9]+, lte [0-9]+$']), \
            'Calories must be string of format "gte L, lte U", "gte L" or ' \
            '"lte U" where L and U are lower and upper bounds'
    assert bool(nutrients) == bool(nutrients_range), \
        'nutrients and nutrients_range should be both present or omitted'
    if nutrients_range and nutrients:
        nutrients_labels = ['CA', 'CHOCDF', 'CHOLE', 'FAMS', 'FAPU', 'FASAT',
                            'FAT', 'FATRN', 'FE', 'FIBTG', 'FOLDFE', 'K', 'MG',
                            'NA', 'NIA', 'P', 'PROCNT', 'RIBF', 'SUGAR',
                            'THIA', 'TOCPHA', 'VITA_RAE', 'VITB12', 'VITB6A',
                            'VITC', 'VITD', 'VITK1', 'ZN']
        assert (isinstance(nutrients_range, list) and
                isinstance(nutrients, list)), \
            'nutrients and nutrients_range must be of type list'
        assert len(nutrients_range) == len(nutrients),\
            'nutrients and nutrients_range must hav equal lengths'
        assert all(x in nutrients_labels for x in nutrients),\
            'nutrients must be in {}'.format(nutrients_labels)
        for nutrient_range in nutrients_range:
            if not any(re.match(regex, nutrient_range)
                       for regex in [r'^[0-9]+$', r'^[0-9]+\+$',
                                     r'^[0-9]+-[0-9]+$']):
                raise AssertionError('nutrients_range must be string in format'
                                     'MIN+, MAX or MIN-MAX where MIN and MAX'
                                     'are integer')

    # add request parameters
    request_params = {
        'q': q,
        'r': r,
        'app_id': app_id,
        'app_key': app_key,
        'from': fromi,
        'to': toi,
        'ingr': ingr,
        'diet': diet,
        'health': health,
    }
    if nutrients and nutrients_range:
        for name, value in nutrients, nutrients_range:
            request_params[name] = value

    # make request to Edamam API
    url = 'https://api.edamam.com/search'
    r = requests.get(url, params=request_params)

    return r.json()


def get_dishes_list(edamam_dict):
    """

    :param edamam_dict: dict returned by get_edamam_json function
    :return: list of recommended dishes
    """

    dishes = list()
    for dish in edamam_dict['hits']:
        dishes.append(dish['recipe']['label'])

    return dishes


