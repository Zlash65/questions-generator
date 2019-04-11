import json

def fetch_input(message="input"):
	''' take input from user '''

	# python 2 and 3 supported
	try:
		user_input = raw_input("%s : " % message)
	except NameError:
		user_input = input("%s : " % message)

	return user_input

def controller():
	''' main flow controller '''

	# input number of questions
	try:
		no_of_questions = fetch_input("Total number of questions")
		no_of_questions = int(no_of_questions)
	except ValueError:
		print('Please enter an integer to denote number of questions!')
		return

	if no_of_questions <= 0:
		print('No. of questions cannot be zero or lower in paper!')
		return

if __name__ == "__main__":
	# main controller
	controller()
