#Functions to do with battling. The most important one is still found in the main script
#Moderately Seafaring

def position_for_battle(party_to_position, y):
	party_length = len(party_to_position.get_members())

	for i in range(0, party_length):
		party_to_position.get_members()[i].set_battle_pos( (900/(party_length-i+2)-32, y) )