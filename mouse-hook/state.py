from enum import Enum

'''
Colors can be found at https://pypi.org/project/colored/
Emojis can be found at https://unicode.org/emoji/charts/full-emoji-list.html
'''

Dead = {
    'color': '245',
    'emoji': 'skull',
    'caption': "X_X"
}

States = [
    # Brink of Death
    {
        'color': '61',
        'emoji': 'anxious_face_with_sweat',
        'caption': "I'm on the brink of death :("
    },
    # Starving
    {
        'color': '111',
        'emoji': 'persevering_face',
        'caption': "I'm starving!!! Give me code!"
    },
    # Hungry
    {
        'color': '141',
        'emoji': 'pleading_face',
        'caption': "I'm hungry for code. Please feed me!!"
    },
    # Peckish
    {
        'color': '219',
        'emoji': 'smiling_face_with_horns',
        'caption': "I'm feeling peckish for some lines of code!"
    },
    # Getting Full
    {
        'color': '202',
        'emoji': 'drooling_face',
        'caption': "I'm getting full!"
    },
    # Feels Good
    {
        'color': '202',
        'emoji': 'relieved_face',
        'caption': "Yum!!!! Thank you!"
    },
    # Feels Great
    {
        'color': '202',
        'emoji': 'face_savoring_food',
        'caption': "These lines are delicious. I feel so satisfied!"
    },
    # Full
    {
        'color': '200',
        'emoji': 'woozy_face',
        'caption': "I'm full! I'm so full with code!"
    }
]

ExtraStates = [    
    # Dizzy
    {
        'color': '198',
        'emoji': 'dizzy_face',
        'caption': "Oh gosh, so much code! This sure feels weird!"
    },
    # Hot
    {
        'color': '196',
        'emoji': 'hot_face',
        'caption': "Stop feeding me! I'm going to explode!!"
    },
    # Nauseated
    {
        'color': '100',
        'emoji': 'nauseated_face',
        'caption': "All these lines are making my head spin!"
    },
    # Vomiting
    {
        'color': '2',
        'emoji': 'face_vomiting',
        'caption': "I've learned my lesson. :( No more code!"
    }
]
