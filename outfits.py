"""Small, transparent outfit rules. Profiles are never persisted."""
from math import isfinite

COLORS = {'olive': '#73785b', 'navy': '#35485e', 'terracotta': '#b76a52', 'cream': '#e6dbc4', 'black': '#343333', 'rose': '#c18c92'}


def recommend(profile):
    if not isinstance(profile, dict):
        raise ValueError('Please send a valid profile.')
    for field, minimum, maximum in [('height', 80, 250), ('weight', 20, 400)]:
        value = profile.get(field)
        if field == 'weight' and value in (None, ''):
            continue
        try:
            number = float(value)
        except (TypeError, ValueError):
            raise ValueError(f'Please enter a valid {field}.')
        if isinstance(value, bool) or not isfinite(number) or not minimum <= number <= maximum:
            raise ValueError(f'{field.capitalize()} must be between {minimum} and {maximum}.')
    color = profile.get('color', 'olive')
    occasion = profile.get('occasion', 'Everyday')
    fit = profile.get('fit', 'Relaxed')
    weather = profile.get('weather', 'Mild')
    if not all(isinstance(value, str) for value in (color, occasion, fit, weather)) or color not in COLORS or occasion not in ['Everyday', 'Office', 'Evening'] or fit not in ['Relaxed', 'Regular', 'Tailored'] or weather not in ['Warm', 'Mild', 'Cool']:
        raise ValueError('Please choose one of the available style options.')
    optional_choices = {
        'skinTone': ['Fair', 'Light', 'Medium', 'Tan', 'Deep', 'Dark'],
        'hairColor': ['Black', 'Brown', 'Blonde', 'Red', 'Gray / white', 'Colorful', 'No hair'],
        'gender': ['Woman', 'Man', 'Non-binary', 'Self-described'],
        'style': ['Minimal', 'Classic', 'Sporty', 'Creative'],
    }
    for field, choices in optional_choices.items():
        if profile.get(field, '') not in ['', *choices]:
            raise ValueError(f'Please choose a valid {field}.')
    style = profile.get('style', '')
    tops = {'Everyday': 'Cotton overshirt', 'Office': 'Unstructured blazer', 'Evening': 'Textured knit polo'}
    top = tops[occasion]
    if weather == 'Warm':
        top = 'Linen button-up' if occasion != 'Evening' else 'Fine-knit polo'
    elif weather == 'Cool':
        top = 'Wool-blend jacket' if occasion != 'Office' else 'Wool blazer'
    if style == 'Sporty' and occasion == 'Everyday':
        top = 'Cotton jersey tee' if weather == 'Warm' else 'Zip-front track jacket'
    elif style == 'Creative':
        top = f'Color-block {top.lower()}'
    elif style == 'Minimal':
        top = f'Clean-lined {top.lower()}'
    elif style == 'Classic' and occasion == 'Everyday':
        top = 'Oxford cotton shirt' if weather != 'Cool' else 'Cable-knit cardigan'
    height = float(profile['height'])
    length = 'Try petite or shorter-length options; check sleeve and inseam measurements.' if height < 160 else 'Try tall-length options; check sleeve and inseam measurements.' if height > 185 else 'Start with standard lengths and check sleeve and inseam measurements.'
    return {
        'title': {'Everyday': 'The everyday edit', 'Office': 'Quietly put together', 'Evening': 'After-hours ease'}[occasion],
        'description': f'{color.capitalize()} tones, {fit.lower()} lines, and pieces chosen for {weather.lower()} weather. An easy starting point for your {occasion.lower()} wardrobe.',
        'items': [
            {'name': top, 'kind': 'top', 'color': COLORS[color], 'detail': f'{color.capitalize()} · {fit} fit'},
            {'name': 'Straight-leg chinos' if occasion == 'Everyday' else 'Pleated trousers', 'kind': 'bottom', 'color': '#d8c8ac' if color != 'cream' else '#73785b', 'detail': f'{fit} fit · versatile neutral'},
            {'name': 'Leather sneakers' if occasion == 'Everyday' else 'Suede loafers', 'kind': 'shoes', 'color': '#ede5d8' if occasion == 'Everyday' else '#795747', 'detail': 'A simple, understated finish'},
        ],
        'notes': [f'Your palette: {color} with grounded neutrals.', length, f'Choose a {fit.lower()} cut according to how you like your clothes to feel.', *([f'Your {style.lower()} style mood guides the finishing details.'] if style else [])],
        'sizing': 'Height and weight alone cannot determine clothing size. Weight is optional and does not change the style suggestion; use garment measurements for sizing.'
    }
