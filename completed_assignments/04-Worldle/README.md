# Worldle Final Project

## What I built

I built a Worldle-style country guessing game in Jupyter using Python, ipyleaflet, ipywidgets, and my updated `wdo` package.

The game chooses a mystery country, draws its polygon on the map, and lets the player guess countries using a searchable input box. After each guess, the game shows the guessed country's flag, country name, direction arrow, and distance from the guess to the target.

## wdo functions added or finished

- `wdo.geometry.bbox.bbox_from_feature`
- `wdo.maps.leaflet_helpers.make_map`
- `wdo.maps.leaflet_helpers.add_geojson`
- `wdo.maps.leaflet_helpers.fit_map_to_geojson`
- `wdo.games.worldle.choose_target`
- `wdo.games.worldle.feature_center`
- `wdo.games.worldle.guess_feedback`
- `wdo.games.worldle.format_feedback`

## Country lookup / flag notes

The country polygons use ISO-3 codes, but the flag icons use ISO-2 codes. I built a lookup table by matching country names and added a few manual aliases for countries whose names do not match exactly.

Some examples:

- United States of America → United States
- Russia → Russian Federation
- South Korea → Korea, Republic of
- Vietnam → Viet Nam

## Polish features

I added:

- Searchable country input using `Combobox`
- Guess limit
- Give up button
- Distance coloring
- Hot/cold emoji feedback
- Flag images in guess history

## Known bugs / limitations

- Country centers are based on bounding boxes, so large or unusual countries may produce imperfect arrows.
- Countries with islands or antimeridian issues may have less accurate centers.
- Some flags may be missing if the country name does not match the flag index.
- The game is designed for a notebook environment, not as a standalone web app.

## Screenshot

See `screenshots/worldle_completed_round.png`.
