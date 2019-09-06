import datapipes
from typing import *
import os
import re

AUDIO_EXTENSIONS = set(['.flac', '.wav'])

CHARACTERS = {
	'A. K. Yearling': 'AK Yearling',
	'Ahuizotl': 'Ahuizotl',
	'All Aboard': 'All Aboard',
	'Apple Bloom': 'Apple Bloom',
	'Apple Cobbler': 'Apple Cobbler',
	'Apple Rose': 'Apple Rose',
	'Applejack': 'Applejack',
	'Auntie Applesauce': 'Auntie Applesauce',
	'Autumn Blaze': 'Autumn Blaze',
	'Babs Seed': 'Babs Seed',
	'Big Bucks': 'Big Bucks',
	'Big Daddy Mccolt': 'Big Daddy Mccolt',
	'Big Mac': 'Big Macintosh',
	'Big Macintosh': 'Big Macintosh',
	'Blaze': 'Blaze',
	'Bow Hothoof': 'Bow Hothoof',
	'Boyle': 'Boyle',
	'Braeburn': 'Braeburn',
	'Bright Mac': 'Bright Mac',
	'Bulk Biceps': 'Bulk Biceps',
	'Burnt Oak': 'Burnt Oak',
	'Caballeron': 'Caballeron',
	'Cadance': 'Cadance',
	'Cadence': 'Cadance',
	'Capper': 'Capper',
	'Captain Celaeno': 'Captain Celaeno',
	'Carnival Barker': 'Carnival Barker',
	'Celestia': 'Celestia',
	'Cheerilee': 'Cheerilee',
	'Cheerlee': 'Cheerilee',
	'Cheese Sandwich': 'Cheese Sandwich',
	'Cherry Berry': 'Cherry Berry',
	'Cherry Jubilee': 'Cherry Jubilee',
	'Chiffon Swirl': 'Chiffon Swirl',
	'Chrysalis': 'Chrysalis',
	'Clear Skies': 'Clear Skies',
	'Cloudy Quartz': 'Cloudy Quartz',
	'Coco Pommel': 'Coco Pommel',
	'Code Red': 'Code Red',
	'Coriander Cumin': 'Coriander Cumin',
	'Countess Coloratura': 'Countess Coloratura',
	'Cozy Glow': 'Cozy Glow',
	'Cranberry Muffin': 'Cranberry Muffin',
	'Cranky': 'Cranky',
	'Daisy': 'Daisy',
	'Daring Do': 'Daring Do',
	'Daybreaker': 'Daybreaker',
	'Derpy': 'Derpy',
	'Diamond Tiara': 'Diamond Tiara',
	'Diamond Tiarra': 'Diamond Tiara',
	'Discord': 'Discord',
	'Donut Joe': 'Donut Joe',
	'Double Diamond': 'Double Diamond',
	'Dr. Caballeron': 'Dr Caballeron',
	'Dr. Hooves': 'Dr Hooves',
	'Dragon Lord Torch': 'Dragon Lord Torch',
	'Ember': 'Ember',
	'Fancy Pants': 'Fancy Pants',
	'Featherweight': 'Featherweight',
	'Female Pony 2': 'Female Pony 2',
	'Film': 'Film',
	'Filthy Rich': 'Filthy Rich',
	'Firelight': 'Firelight',
	'Flam': 'Flam',
	'Flash Magnus': 'Flash Magnus',
	'Fleetfoot': 'Fleetfoot',
	'Flim': 'Flim',
	'Flurry': 'Flurry',
	'Fluttershy': 'Fluttershy',
	'Gabby': 'Gabby',
	'Gallus': 'Gallus',
	'Gilda': 'Gilda',
	'Gladmane': 'Gladmane',
	'Goldgrape': 'Goldgrape',
	'Goldie Delicious': 'Goldie Delicious',
	'Grampa Gruff': 'Grampa Gruff',
	'Grand Pear': 'Grand Pear',
	'Granny Smith': 'Granny Smith',
	'Grany Smith': 'Granny Smith',
	'Grubber': 'Grubber',
	'Gustave Le Grand': 'Gustave Le Grand',
	'High Winds': 'High Winds',
	'Hoity Toity': 'Hoity Toity',
	'Hoo\'far': 'Hoofar',
	'Igneous': 'Igneous',
	'Iron Will': 'Iron Will',
	'Jack Pot': 'Jack Pot',
	'Lemon Hearts': 'Lemon Hearts',
	'Lightning Dust': 'Lightning Dust',
	'Lily Valley': 'Lily Valley',
	'Limestone': 'Limestone',
	'Lix Spittle': 'Lix Spittle',
	'Louise': 'Louise',
	'Luggage Cart': 'Luggage Cart',
	'Luna': 'Luna',
	'Lyra Heartstrings': 'Lyra Heartstrings',
	'Lyra': 'Lyra Heartstrings',
	'Ma Hooffield': 'Ma Hooffield',
	'Mane-iac': 'Mane-iac',
	'Marble': 'Marble',
	'Matilda': 'Matilda',
	'Maud': 'Maud',
	'Mayor Mare': 'Mayor Mare',
	'Meadowbrook': 'Meadowbrook',
	'Mean Applejack': 'Mean Applejack',
	'Mean Fluttershy': 'Mean Fluttershy',
	'Mean Pinkie Pie': 'Mean Pinkie Pie',
	'Mean Rainbow Dash': 'Mean Rainbow Dash',
	'Mean Rarity': 'Mean Rarity',
	'Mean Twilight Sparkle': 'Mean Twilight Sparkle',
	'Minuette': 'Minuette',
	'Miss Harshwhinny': 'Miss Harshwhinny',
	'Mistmane': 'Mistmane',
	'Misty Fly': 'Misty Fly',
	'Moon Dancer': 'Moon Dancer',
	'Mori': 'Mori',
	'Mr Cake': 'Mr Cake',
	'Mr. Cake': 'Mr Cake',
	'Mrs Cake': 'Mrs Cake',
	'Mrs. Cake': 'Mrs Cake',
	'Mrs. Shy': 'Mrs Shy',
	'Mudbriar': 'Mudbriar',
	'Mulia Mild': 'Mulia Mild',
	'Mullet': 'Mullet',
	'Multiple': 'Multiple',
	'Neighsay': 'Neighsay',
	'Night Glider': 'Night Glider',
	'Night Light': 'Night Light',
	'Nightmare Moon': 'Nightmare Moon',
	'Ocean Flow': 'Ocean Flow',
	'Ocellus': 'Ocellus',
	'Octavia': 'Octavia',
	'On Stage': 'On Stage',
	'Party Favor': 'Party Favor',
	'Pear Butter': 'Pear Butter',
	'Pharynx': 'Pharynx',
	'Photo Finish': 'Photo Finish',
	'Photographer': 'Photographer',
	'Pig Creature 1': 'Pig Creature 1',
	'Pig Creature 2': 'Pig Creature 2',
	'Pinkie': 'Pinkie Pie',
	'Pipsqueak': 'Pipsqueak',
	'Pony Of Shadows': 'Pony Of Shadows',
	'Prince Rutherford': 'Prince Rutherford',
	'Princess Cadance': 'Cadance',
	'Princess Skystar': 'Skystar',
	'Pursey Pink': 'Pursey Pink',
	'Pushkin': 'Pushkin',
	'Queen Novo': 'Queen Novo',
	'Quibble Pants': 'Quibble Pants',
	'Rachel Platten': 'Rachel Platten',
	'Rain Shine': 'Rain Shine',
	'Rainbow': 'Rainbow Dash',
	'Rarity': 'Rarity',
	'Raspberry Beret': 'Raspberry Beret',
	'Rockhoof': 'Rockhoof',
	'Rolling Thunder': 'Rolling Thunder',
	'Rose': 'Rose',
	'Rumble': 'Rumble',
	'S04e26 Unnamed Earth Mare #1': 'S04e26 Unnamed Earth Mare #1',
	'Saffron Masala': 'Saffron Masala',
	'Sandbar': 'Sandbar',
	'Sapphire Shores': 'Sapphire Shores',
	'Sassy Saddles': 'Sassy Saddles',
	'Scootaloo': 'Scootaloo',
	'Seaspray': 'Seaspray',
	'Shining Armor': 'Shining Armor',
	'Short Fuse': 'Short Fuse',
	'Silver Spoon': 'Silver Spoon',
	'Silverstream': 'Silverstream',
	'Sky Beak': 'Sky Beak',
	'Sky Stinger': 'Sky Stinger',
	'Sludge': 'Sludge',
	'Smolder': 'Smolder',
	'Snails': 'Snails',
	'Snips': 'Snips',
	'Soarin': 'Soarin',
	'Sombra': 'Sombra',
	'Somnambula': 'Somnambula',
	'Songbird Serenade': 'Songbird Serenade',
	'Spike': 'Spike',
	'Spitfire': 'Spitfire',
	'Spoiled Rich': 'Spoiled Rich',
	'Star Swirl': 'Star Swirl',
	'Starlight': 'Starlight',
	'Stellar Flare': 'Stellar Flare',
	'Steve': 'Steve',
	'Storm Creature': 'Storm Creature',
	'Stormy Flare': 'Stormy Flare',
	'Stygian': 'Stygian',
	'Sugar Belle': 'Sugar Belle',
	'Sunburst': 'Sunburst',
	'Surprise': 'Surprise',
	'Svengallop': 'Svengallop',
	'Sweetie Belle': 'Sweetie Belle',
	'Sweetie Drops': 'Sweetie Drops',
	'Tempest Shadow': 'Tempest Shadow',
	'Terramar': 'Terramar',
	'The Storm King': 'The Storm King',
	'Thorax': 'Thorax',
	'Thunderlane': 'Thunderlane',
	'Tight End': 'Tight End',
	'Tirek': 'Tirek',
	'Toothy Klugetowner': 'Toothy Klugetowner',
	'Tourist Pony': 'Tourist Pony',
	'Tree Hugger': 'Tree Hugger',
	'Tree Of Harmony': 'Tree Of Harmony',
	'Trixie': 'Trixie',
	'Twilight Velvet': 'Twilight Velvet',
	'Twilight': 'Twilight Sparkle',
	'Twinkleshine': 'Twinkleshine',
	'Twist': 'Twist',
	'Vapor Trail': 'Vapor Trail',
	'Vendor 2': 'Vendor 2',
	'Vera': 'Vera',
	'Verko': 'Verko',
	'Vinny': 'Vinny',
	'Whinnyfield': 'Whinnyfield',
	'Wind Rider': 'Wind Rider',
	'Windy Whistles': 'Windy Whistles',
	'Yona': 'Yona',
	'Zecora': 'Zecora',
	'Zephyr': 'Zephyr',
	'Zesty Gourmand': 'Zesty Gourmand',
}

class ClipperDataset:
	def __init__(self, folder: str):
		self.folder = folder

	def get_clips(self):
		if datapipes.__verbose__:
			print('collecting audio files from {}'.format(self.folder.path))

		audio_paths = []
		for root, dirs, files in os.walk(self.folder.path, followlinks=False):
			audio_paths.extend([os.path.join(root, x)
				for x in files if os.path.splitext(x)[-1] in AUDIO_EXTENSIONS])

		for path in audio_paths:
			try:
				if datapipes.__verbose__:
					print('found {}'.format(path))
				yield ClipperFile(path)
			except AssertionError as e:
				if not datapipes.__dry_run__:
					raise
				print(str(e))

def character_from_path(path: str):
	filename = os.path.basename(path)

	# hh_mm_ss_character_extra
	character_match = re.search(r'^[0-9][0-9]_[0-9][0-9]_[0-9][0-9]_([^_]*)', filename)
	assert character_match != None, \
		'Sound file {} should be in format hh_mm_ss_CharacterName_extra.flac'.format(path)

	character_key = character_match.groups()[0]
	assert character_key in CHARACTERS, \
		'Missing character {} in clipper_in.CHARACTERS for {}'.format(character_key, path)

	return CHARACTERS[character_key]

class ClipperFile:
	def __init__(self, audio_path: str):
		base_filename = os.path.splitext(audio_path)[0]
		self.audio_path = audio_path
		self.transcript_path = '{}.txt'.format(base_filename)
		self.character = character_from_path(audio_path)

