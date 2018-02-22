#Code for the party object, which contains characters

class Party():
	"""Indexable party for characters in Moderately Seafaring"""
	def __init__(self):
		super(Party, self).__init__()
		self.members = []
		self.current_member_number = 0
		self.stored_pos = [0, 0]

	def __getitem__(self, index):
		return self.get_members()[index]

	def __setitem__(self, index, new):
		self.members[index] = new

	def __delitem__(self, index):
		self.members.remove(self.members.index(index))

	def add_member(self, new_member):
		self.members.append(new_member)

	def get_members(self):
		return self.members

	def get_stored_pos(self):
		return self.stored_pos

	def get_current_member(self):
		return self.get_members()[self.current_member_number]

	def set_current_member_number(self, new):
		self.current_member_number = new

	def set_current_member(self, member):
		if member not in self.get_members():
			raise ValueError("You must set member to someone who exists in the party!")

		self.set_current_member_number(self.get_members().index(member))

	def set_stored_pos(self, new_pos):
		self.stored_pos = new_pos