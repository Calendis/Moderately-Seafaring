#Functions that generate names for various types of characters
#Moderately Seafaring
from random import randint

def GenerateName(name_type):
	if name_type == "pirate_male":
		first_names = pirate_male_first_names
		last_names = pirate_last_names
	elif name_type == "human_male":
		first_names = human_male_first_names
		last_names = human_last_names

	first_name = first_names[randint(0, len(first_names)-1)]
	last_name = last_names[randint(0, len(last_names)-1)]

	while first_name.split()[-1] == last_name: #This loop prevents names like "Jack Jack", "George George", or "Clam Chowder Chowder"
		if randint(0, 1):
			first_name = first_names[randint(0, len(first_names)-1)]
		else:
			last_name = last_names[randint(0, len(last_names)-1)]

	return first_name+" "+last_name
	
pirate_male_first_names = [
	"Big",
	"Rick",
	"Toby",
	"Andy",
	"John",
	"Jarge",
	"Wet",
	"Crusty",
	"Spikey",
	"James",
	"Stinky",
	"Larry",
	"Mad",
	"Dingle",
	"Misty",
	"Squeaky",
	"Nestor",
	"Don",
	"Jimmy",
	"Limey",
	"Lemony",
	"Piers",
	"Chris",
	"Jack",
	"Worm",
	"Hunter",
	"Jamie",
	"Moist",
	"Beefy",
	"Black",
	"Reggie",
	"Clam Chowder",
	"Bearded",
	"Eyepatch",
	"Cutlass",
	"Rich",
	"Crazy",
	"Henry",
	"Steve",
	"Squall",
	"Stormy",
	"Sandy",
	"Rocky",
	"Dennis",
	"Windy",
	"Bilgemaster",
	"Scabby"
]
	
pirate_last_names = [
	"Cornpower",
	"Slick",
	"Cream",
	"Zips",
	"Seaweed",
	"George",
	"Johnson",
	"Sunday",
	"Rats",
	"Baxter",
	"Dog",
	"Tuna",
	"Salmon",
	"Shark",
	"Barracuda",
	"Eyepatch",
	"Stevens",
	"Clean",
	"McSeasick",
	"Tornado",
	"Cutlass",
	"Salteen",
	"Swabs",
	"Barrels",
	"Columbus",
	"Beard",
	"Blue",
	"Snakes",
	"Polaris",
	"Chowder",
	"Jack",
	"Snicket",
	"Morgan",
	"Monsoon",
	"Danger",
	"Fishcake",
	"Gold",
	"Steve",
	"Wacko",
	"Machete",
	"of the Wind",
	"Keelhauler",
	"Thicksail",
	"of the Sea",
	"Bilgemaster",
	"Bloodrag"
]

human_male_first_names = [
	"Hector",
	"Jeff"
]

human_last_names = [
	"Smith",
	"Jefferson"
]