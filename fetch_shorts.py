import os
import json
import subprocess 
import time

# 200 NEW AI Categories & Characters
CATEGORIES = [
    # AI Characters & People
    "ai_boys", "ai_girls", "ai_cyberpunk_boy", "ai_cyberpunk_girl", "ai_anime_boy", "ai_anime_girl",
    "ai_monk", "ai_warrior", "ai_samurai", "ai_ninja", "ai_astronaut", "ai_king", "ai_queen",
    "ai_robot", "ai_android", "ai_cyborg", "ai_demon", "ai_angel", "ai_vampire", "ai_wizard",
    "ai_witch", "ai_viking", "ai_knight", "ai_pirate", "ai_detective", "ai_doctor", "ai_teacher",
    "ai_alien", "ai_greek_god", "ai_pharaoh", "ai_superhero", "ai_villain", "ai_baby", "ai_old_man",
    "ai_old_woman", "ai_soldier", "ai_gladiator", "ai_spartan", "ai_ghost", "ai_zombie",
    
    # Nature & Scenery AI
    "ai_mountain", "ai_forest", "ai_ocean", "ai_space", "ai_galaxy", "ai_waterfall", "ai_desert",
    "ai_volcano", "ai_jungle", "ai_cave", "ai_skyline", "ai_sunset", "ai_aurora", "ai_snow_mountain",
    "ai_island", "ai_river", "ai_clouds", "ai_underwater", "ai_storm", "ai_lightning",

    # AI Animals & Creatures
    "ai_cat", "ai_dog", "ai_lion", "ai_tiger", "ai_wolf", "ai_dragon", "ai_phoenix", "ai_eagle",
    "ai_bear", "ai_snake", "ai_horse", "ai_monkey", "ai_fox", "ai_owl", "ai_shark", "ai_whale",
    "ai_dinosaur", "ai_unicorn", "ai_griffin", "ai_monster",

    # Sci-Fi, Fantasy & Architecture
    "ai_futuristic_city", "ai_cyberpunk_city", "ai_fantasy_castle", "ai_space_station",
    "ai_alien_planet", "ai_sci_fi_lab", "ai_neon_street", "ai_flying_car", "ai_time_portal",
    "ai_underwater_city", "ai_steampunk_world", "ai_floating_island", "ai_ancient_temple",
    "ai_pyramids", "ai_abandoned_city", "ai_post_apocalypse", "ai_dystopia", "ai_utopia",
    "ai_magic_forest", "ai_haunted_house",

    # Art Styles & Conceptual AI
    "ai_3d_avatar", "ai_hyperrealistic", "ai_unreal_engine", "ai_pixar_style", "ai_ghibli_style",
    "ai_cinematic_short", "ai_dark_fantasy", "ai_synthwave", "ai_vaporwave", "ai_surrealism",
    "ai_concept_art", "ai_glitch_art", "ai_hologram", "ai_neon_art", "ai_claymation",
    "ai_papercraft", "ai_pixel_art", "ai_low_poly", "ai_abstract_art", "ai_fractal_art",

    # AI Gaming & Pop Culture
    "ai_minecraft", "ai_gta6", "ai_fortnite", "ai_elden_ring", "ai_cyberpunk2077", "ai_pokemon",
    "ai_dragon_ball", "ai_naruto", "ai_one_piece", "ai_attack_on_titan", "ai_demon_slayer",
    "ai_marvel", "ai_dc_comics", "ai_star_wars", "ai_lord_of_the_rings", "ai_harry_potter",
    "ai_matrix", "ai_avatar_pandora", "ai_transformers", "ai_godzilla",

    # Vehicles & Technology AI
    "ai_supercar", "ai_hypercar", "ai_concept_bike", "ai_spaceship", "ai_mecha", "ai_jet",
    "ai_ufo", "ai_drone", "ai_hoverboard", "ai_quantum_computer",
    # AI Historical Figures & Ancient Warriors
    "ai_roman_emperor", "ai_samurai_legend", "ai_mongol_warrior", "ai_persian_immortal",
    "ai_aztec_warrior", "ai_cleopatra", "ai_alexander_the_great", "ai_king_arthur",
    "ai_celtic_warrior", "ai_ottoman_janissary", "ai_ninja_assassin", "ai_gladiator_champion",
    "ai_spartan_king", "ai_pharaoh_guard", "ai_viking_berserker", "ai_medieval_monk",
    "ai_templar_knight", "ai_samurai_geisha", "ai_ancient_philosopher", "ai_tribal_chief",

    # World Cultures & Traditional Attire AI
    "ai_indian_wedding", "ai_japanese_kimono", "ai_arabian_sheikh", "ai_african_warrior",
    "ai_chinese_emperor", "ai_korean_hanbok", "ai_mexican_mariachi", "ai_viking_valkyrie",
    "ai_native_american", "ai_bedouin_nomad", "ai_persian_princess", "ai_scottish_highlander",
    "ai_egyptian_god", "ai_russian_czar", "ai_balines_dancer", "ai_tibetan_monk",
    "ai_spanish_matador", "ai_thai_warrior", "ai_hawaiian_kahuna", "ai_polynesian_tribal",

    # AI Mythological & Folklore Creatures
    "ai_minotaur", "ai_centaur", "ai_medusa", "ai_kraken", "ai_anubis", "ai_thor",
    "ai_odin", "ai_poseidon", "ai_zeus", "ai_valkyrie", "ai_yeti", "ai_wendigo",
    "ai_basilisk", "ai_sphinx", "ai_golem", "ai_cyclops", "ai_siren", "ai_pegasus",
    "ai_hydra", "ai_fenrir",

    # Sci-Fi Cybernetic & Post-Human AI
    "ai_mecha_pilot", "ai_exosuit_soldier", "ai_space_bounty_hunter", "ai_cyber_ninja",
    "ai_cybernetic_samurai", "ai_ai_overlord", "ai_android_assassin", "ai_cyborg_gladiator",
    "ai_quantum_human", "ai_neon_bounty_hunter", "ai_space_pirate", "ai_alien_diplomat",
    "ai_dystopian_rebel", "ai_cyber_detective", "ai_hologram_singer", "ai_mech_suit",
    "ai_nano_tech_man", "ai_synth_human", "ai_time_enforcer", "ai_void_walker",

    # Fantasy Professions & RPG Classes
    "ai_necromancer", "ai_paladin", "ai_druid", "ai_bard", "ai_archmage", "ai_assassin",
    "ai_beast_master", "ai_elemental_mage", "ai_shadow_knight", "ai_potion_maker",
    "ai_dragon_rider", "ai_demon_hunter", "ai_blood_mage", "ai_runesmith", "ai_astrologer",
    "ai_bounty_hunter", "ai_alchemist", "ai_battle_mage", "ai_divine_cleric", "ai_soul_reaper",

    # Extreme Environments & Post-Apocalypse
    "ai_nuclear_winter", "ai_cyber_wasteland", "ai_sub_zero_ice_city", "ai_sandstorm_desert", "ai_toxic_swamp",
    "ai_volcanic_ash_world", "ai_acid_rain_city", "ai_alien_jungle", "ai_space_colony", "ai_underground_bunker",
    "ai_flooded_metropolis", "ai_asteroid_mining", "ai_deep_space_void", "ai_frozen_wasteland", "ai_lava_planet",
    "ai_ruined_sanctuary", "ai_radiation_zone", "ai_sunken_continent", "ai_black_hole_horizon", "ai_quantum_realm",

    # Futuristic & Retro Vehicles
    "ai_hover_car", "ai_cyber_truck", "ai_flying_motorcycle", "ai_steampunk_train",
    "ai_space_dreadnought", "ai_plasma_supercar", "ai_underwater_sub_fighter", "ai_armored_mech",
    "ai_alien_starship", "ai_neon_racer", "ai_solar_sail_ship", "ai_supersonic_jet",
    "ai_cyber_tank", "ai_futuristic_yacht", "ai_warp_drive_ship", "ai_hover_tank",
    "ai_steampunk_airship", "ai_exo_rover", "ai_orbital_shuttle", "ai_quantum_ship",

    # Unique Surreal & Digital Art Styles
    "ai_origami_art", "ai_stained_glass", "ai_wireframe_3d", "ai_watercolor_cinematic",
    "ai_charcoal_sketch", "ai_chibi_character", "ai_ink_wash_painting", "ai_graffiti_mural",
    "ai_isometric_city", "ai_glitch_core", "ai_retrofuturism", "ai_cyber_punk_gothic",
    "ai_blueprint_art", "ai_voxel_world", "ai_oil_painting_masterpiece", "ai_marble_statue",
    "ai_hologram_matrix", "ai_sand_art", "ai_glass_sculpture", "ai_neon_gothic",

    # Popular Anime, Games & Media Tropes
    "ai_mecha_godzilla", "ai_cyberpunk_samurai_girl", "ai_fantasy_dungeon", "ai_space_marine",
    "ai_dark_souls_boss", "ai_monster_hunter", "ai_tekken_fighter", "ai_street_fighter",
    "ai_genshin_impact_style", "ai_valorant_style", "ai_overwatch_hero", "ai_final_fantasy",
    "ai_anime_villain", "ai_anime_transformation", "ai_chibi_anime", "ai_kaiju_battle",
    "ai_cyber_fighter", "ai_stealth_ninja", "ai_arena_champion", "ai_space_explorer",

    # Specialized Short-Form Storytelling & Niche Topics
    "ai_scary_mythology", "ai_unexplained_mysteries", "ai_time_travel_stories", "ai_future_jobs_2050",
    "ai_alien_encounter", "ai_parallel_universe", "ai_ancient_china", "ai_dark_fairytale",
    "ai_deep_ocean_mysteries", "ai_space_exploration_2100", "ai_extinction_event", "ai_ancient_tech",
    "ai_ancient_aliens", "ai_dystopian_laws", "ai_futuristic_weapons", "ai_cybernetic_implants",
    "ai_ai_robot_revolution", "ai_mind_control_sci_fi", "ai_matrix_glitch", "ai_quantum_physics_visual"
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
