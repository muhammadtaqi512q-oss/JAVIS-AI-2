import os
import json
import subprocess 
import time

# 200 NEW AI Categories & Characters
CATEGORIES = [
    # Talking & Living Cute Fruits                
    "ai_animated_cute_apple", "ai_animated_dancing_banana", "ai_animated_talking_mango", "ai_animated_happy_strawberry",
    "ai_animated_watermelon_character", "ai_animated_pineapple_warrior", "ai_animated_orange_fruit_face", "ai_animated_grapes_family",
    "ai_animated_cute_peach", "ai_animated_talking_avocado", "ai_animated_cherry_twins", "ai_animated_lemon_hero",
    "ai_animated_papaya_character", "ai_animated_guava_monster", "ai_animated_kiwi_bird_fruit", "ai_animated_dragon_fruit_monster",
    "ai_animated_pomegranate_king", "ai_animated_blueberry_squad", "ai_animated_raspberry_character", "ai_animated_lychee_fairy",

    # Talking & Living Cute Vegetables
    "ai_animated_talking_potato", "ai_animated_dancing_carrot", "ai_animated_broccoli_superhero", "ai_animated_cute_tomato",
    "ai_animated_onion_crying_face", "ai_animated_garlic_warrior", "ai_animated_chili_pepper_fire", "ai_animated_corn_man",
    "ai_animated_eggplant_character", "ai_animated_cucumber_ninja", "ai_animated_pumpkin_monster", "ai_animated_cabbage_king",
    "ai_animated_mushroom_village", "ai_animated_capsicum_robot", "ai_animated_pea_pod_family", "ai_animated_spinach_power",
    "ai_animated_beetroot_character", "ai_animated_ginger_root_monster", "ai_animated_cauliflower_brain", "ai_animated_radish_running",

    # Fruit & Vegetable Characters in Action
    "ai_fruit_boxing_match", "ai_vegetable_dancing_party", "ai_talking_fruit_funny_joke", "ai_fruit_superhero_league",
    "ai_vegetable_ninja_fight", "ai_fruit_racing_cars", "ai_animated_veggie_orchestra", "ai_fruit_gym_workout",
    "ai_talking_fruit_singing", "ai_animated_fruit_school", "ai_fruit_cooking_chef", "ai_vegetable_army_march",
    "ai_animated_fruit_magician", "ai_fruit_space_astronaut", "ai_vegetable_rock_band", "ai_animated_fruit_football",
    "ai_fruit_skateboarding", "ai_vegetable_karate_master", "ai_fruit_dj_party", "ai_animated_veggie_detective",

    # Transformations & Hybrid Monsters (Veggie & Fruit AI)
    "ai_fruit_to_monster_transformation", "ai_cyberpunk_banana", "ai_mecha_broccoli_robot", "ai_dragon_fruit_real_dragon",
    "ai_chili_fire_elemental", "ai_watermelon_golem", "ai_pineapple_armored_knight", "ai_pumpkin_jack_o_lantern_ai",
    "ai_crystal_apple_magic", "ai_glowing_bioluminescent_fruit", "ai_stone_vegetable_titan", "ai_poisonous_mushroom_witch",
    "ai_neon_fruit_city", "ai_glitch_animated_avocado", "ai_lava_chili_pepper", "ai_ice_mint_berry",
    "ai_galaxy_fruit_space", "ai_golden_mango_god", "ai_steampunk_clockwork_orange", "ai_alien_vegetable_creature",

    # 3D Hyper-Realistic & Photorealistic Fruit Animations
    "ai_3d_hyperrealistic_dancing_apple", "ai_photorealistic_talking_watermelon", "ai_3d_cute_banana_walk", "ai_unreal_engine_fruit_animation",
    "ai_hyperrealistic_cute_tomato_face", "ai_3d_juicy_orange_splash", "ai_cinematic_glowing_berries", "ai_3d_animated_avocado_dance",
    "ai_photorealistic_veggie_world", "ai_3d_cute_strawberry_smile", "ai_hyperrealistic_mango_character", "ai_3d_funny_potato_expression",
    "ai_cinematic_fruit_explosion", "ai_3d_pineapple_dancing", "ai_photorealistic_lemon_expressions", "ai_3d_animated_cherry_love",
    "ai_hyperrealistic_mushroom_spores", "ai_3d_funny_chili_reaction", "ai_cinematic_veggie_forest", "ai_3d_cute_grapes_jumping",

    # Emotion & Story-Driven Fruit Shorts
    "ai_sad_apple_story", "ai_angry_chili_pepper", "ai_scared_little_potato", "ai_happy_banana_adventure",
    "ai_lonely_strawberry_animation", "ai_brave_carrot_hero", "ai_funny_talking_veggies", "ai_cute_baby_fruit_animation",
    "ai_fruit_love_story_animation", "ai_vegetable_escape_from_kitchen", "ai_fruit_friendship_story", "ai_sleeping_cute_peach",
    "ai_surprised_avocado_face", "ai_hungry_caterpillar_and_fruit", "ai_fruit_birthday_party", "ai_veggie_bedtime_story",
    "ai_giant_fruit_attack", "ai_tiny_vegetable_world", "ai_magic_fruit_tree", "ai_talking_fruit_compilation",

    # Kitchen & Food World Fantasy
    "ai_kitchen_counter_veggie_party", "ai_refrigerator_fruit_night_life", "ai_fruit_salad_dancing", "ai_veggie_soup_swimming_pool",
    "ai_juice_blender_escape_plan", "ai_cutting_board_veggie_city", "ai_fruit_supermarket_adventure", "ai_animated_fruit_market",
    "ai_veggie_garden_fairy_tale", "ai_fruit_tree_village", "ai_underwater_fruit_aquarium", "ai_flying_fruit_balloons",
    "ai_candy_and_fruit_world", "ai_veggie_farm_story", "ai_fruit_waterfall_splash", "ai_animated_fruit_baking",
    "ai_ice_cream_and_fruit_friends", "ai_fruit_picnic_day", "ai_veggie_harvest_festival", "ai_giant_watermelon_house",

    # ASMR, Satisfying & Visual Effects Fruit AI
    "ai_fruit_asmr_animation", "ai_satisfying_veggie_slicing_ai", "ai_glowing_neon_fruits", "ai_squishy_cute_fruit_satisfying",
    "ai_fruit_jelly_transformation", "ai_kinetic_sand_fruit_animation", "ai_water_drop_on_talking_fruit", "ai_melting_ice_fruit_ai",
    "ai_rainbow_color_changing_apple", "ai_glitter_sparkle_strawberry", "ai_crystal_cut_fruit_visual", "ai_satisfying_fruit_peeling_ai",
    "ai_gummy_bear_and_fruit_animation", "ai_slime_fruit_character", "ai_hyper_satisfying_veggie_cut", "ai_glowing_mushroom_asmr",
    "ai_fruit_crushing_satisfying", "ai_neon_veggie_glow_in_dark", "ai_fruit_bubble_gum_pop", "ai_satisfying_fruit_juicing",

    # Aesthetic & Art Style Vegetables/Fruits
    "ai_claymation_cute_fruit", "ai_origami_paper_vegetables", "ai_woolen_crochet_animated_fruits", "ai_watercolor_talking_veggies",
    "ai_pixar_style_cute_apple", "ai_anime_style_talking_fruit", "ai_ghibli_style_veggie_garden", "ai_retro_8bit_pixel_fruit",
    "ai_felt_plushie_animated_banana", "ai_glass_sculpture_glowing_fruit", "ai_cartoon_veggie_show", "ai_chibi_fruit_characters",
    "ai_disney_style_talking_mango", "ai_3d_clay_veggie_world", "ai_doodle_art_animated_fruits", "ai_low_poly_3d_fruit",
    "ai_vibrant_pastel_veggies", "ai_gothic_style_dark_pumpkin", "ai_cyberpunk_neon_citrus", "ai_fantasy_fairy_fruit",

    # Specific Fruit/Veggie Mashups & Tropes
    "ai_banana_cat_fruit_hybrid", "ai_apple_dog_character", "ai_avocado_bear_cute", "ai_watermelon_shark_ocean",
    "ai_pineapple_owl_flying", "ai_tomato_frog_jumping", "ai_broccoli_tree_house", "ai_orange_cat_sleeping",
    "ai_strawberry_bunny_hopping", "ai_potato_sloth_moving_slow", "ai_corn_cockatoo_bird", "ai_mushroom_snail_crawling",
    "ai_mango_monkey_swinging", "ai_peach_piggy_cute", "ai_cherry_birds_singing", "ai_cucumber_snake_slithering",
    "ai_eggplant_penguin_walking", "ai_pumpkin_bear_hugging", "ai_lemon_chick_chirping", "ai_kiwi_hedgehog_rolling"
]

LINKS_PER_CATEGORY = 10

def fetch_shorts_for_category(category, count=10):
    query_text = category.replace('_', ' ')
    search_query = f"ytsearch25:#shorts {query_text} AI video"
    
    cmd = [
        "yt-dlp",
        search_query,
        "--dump-json",
        "--flat-playlist",
        "--ignore-errors",
        "--no-warnings",
        "--extractor-args", "youtube:player_client=android,web"
    ]
    
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    results = []
    seen_ids = set()
    
    for line in process.stdout:
        line_str = line.strip()
        if not line_str:
            continue
        try:
            video_data = json.loads(line_str)
            video_id = video_data.get("id")
            title = video_data.get("title", "AI Shorts Video")
            
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                results.append({
                    "title": title,
                    "url": f"https://www.youtube.com/shorts/{video_id}"
                })
                
                if len(results) >= count:
                    break
        except Exception:
            continue
            
    return results

def main():
    json_filename = "data.json"
    
    # Existing data.json load karke merge karne ka logic
    if os.path.exists(json_filename):
        try:
            with open(json_filename, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception:
            data = {"categories": {}}
    else:
        data = {"categories": {}}

    if "categories" not in data:
        data["categories"] = {}

    total_new_fetched = 0
    print(f"Starting to fetch {len(CATEGORIES)} new categories...")
    
    for idx, category in enumerate(CATEGORIES, 1):
        shorts = fetch_shorts_for_category(category, LINKS_PER_CATEGORY)
        data["categories"][category] = shorts
        total_new_fetched += len(shorts)
        print(f"[{idx}/{len(CATEGORIES)}] {category}: {len(shorts)} shorts added.")
        time.sleep(0.1)

    # Save merged data
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

    total_cats = len(data["categories"])
    total_links = sum(len(v) for v in data["categories"].values())

    print("\n==========================================")
    print(f"[SUCCESS] Merged and Saved to {json_filename}")
    print(f"New Links Added Today: {total_new_fetched}")
    print(f"Total Categories in JSON: {total_cats}")
    print(f"Total Combined Links in JSON: {total_links}")
    print("==========================================")

if __name__ == "__main__":
    main()
