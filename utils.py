# Return the plant hashmap for use in main.py and get_NRC_data.py
def get_plant_hashmap():
    plant_hashmap = {
        "Arkansas Nuclear 1": 1,
        "Arkansas Nuclear 2": 2,
        "Beaver Valley 1": 3,
        "Beaver Valley 2": 4,
        "Braidwood 1": 5,
        "Braidwood 2": 6,
        "Browns Ferry 1": 7,
        "Browns Ferry 2": 8,
        "Browns Ferry 3": 9,
        "Brunswick 1": 10,
        "Brunswick 2": 11,
        "Byron 1": 12,
        "Byron 2": 13,
        "Callaway": 14,
        "Calvert Cliffs 1": 15,
        "Calvert Cliffs 2": 16,
        "Catawba 1": 17,
        "Catawba 2": 18,
        "Clinton": 19,
        "Columbia Generating Station": 20,
        "Comanche Peak 1": 21,
        "Comanche Peak 2": 22,
        "Cooper": 23,
        "D.C. Cook 1": 24,
        "D.C. Cook 2": 25,
        "DC Cook 1": 24,
        "DC Cook 2": 25,
        "Davis-Besse": 26,
        "Diablo Canyon 1": 27,
        "Diablo Canyon 2": 28,
        "Dresden 2": 29,
        "Dresden 3": 30,
        "Farley 1": 31,
        "Farley 2": 32,
        "Fermi 2": 33,
        "FitzPatrick": 34,
        "Ginna": 35,
        "Grand Gulf 1": 36,
        "Hatch 1": 37,
        "Hatch 2": 38,
        "Hope Creek 1": 39,
        "LaSalle 1": 40,
        "LaSalle 2": 41,
        "Limerick 1": 42,
        "Limerick 2": 43,
        "McGuire 1": 44,
        "McGuire 2": 45,
        "Millstone 2": 46,
        "Millstone 3": 47,
        "Monticello": 48,
        "Nine Mile Point 1": 49,
        "Nine Mile Point 2": 50,
        "North Anna 1": 51,
        "North Anna 2": 52,
        "Oconee 1": 53,
        "Oconee 2": 54,
        "Oconee 3": 55,
        "Palo Verde 1": 56,
        "Palo Verde 2": 57,
        "Palo Verde 3": 58,
        "Peach Bottom 2": 59,
        "Peach Bottom 3": 60,
        "Perry 1": 61,
        "Point Beach 1": 62,
        "Point Beach 2": 63,
        "Prairie Island 1": 64,
        "Prairie Island 2": 65,
        "Quad Cities 1": 66,
        "Quad Cities 2": 67,
        "River Bend Station 1": 68,
        "Robinson 2": 69,
        "Saint Lucie 1": 70,
        "Saint Lucie 2": 71,
        "Salem 1": 72,
        "Salem 2": 73,
        "Seabrook 1": 74,
        "Sequoyah 1": 75,
        "Sequoyah 2": 76,
        "Harris 1": 77,
        "South Texas 1": 78,
        "South Texas 2": 79,
        "Summer": 80,
        "Surry 1": 81,
        "Surry 2": 82,
        "Susquehanna 1": 83,
        "Susquehanna 2": 84,
        "Turkey Point 3": 85,
        "Turkey Point 4": 86,
        "Vogtle 1": 87,
        "Vogtle 2": 88,
        "Vogtle 3": 89,
        "Vogtle 4": 90,
        "Waterford 3": 91,
        "Watts Bar 1": 92,
        "Watts Bar 2": 93,
        "Wolf Creek 1": 94
    }
    return plant_hashmap

# Returns hashmap with uppercase keys
def get_upper_plant_hashmap():
    test_dict = get_plant_hashmap()
    new_dict = dict()
    for key in test_dict.keys():
        if isinstance(test_dict[key], dict):
            new_dict[key.upper()] = get_upper_plant_hashmap(test_dict[key])
        else:
            new_dict[key.upper()] = test_dict[key]
    return new_dict


# Returns the reverse of the plant hashmap
def get_reverse_plant_hashmap():
    plant_hashmap = get_plant_hashmap()
    reverse_plant_hashmap = dict((v, k) for k, v in plant_hashmap.items())
    return reverse_plant_hashmap



