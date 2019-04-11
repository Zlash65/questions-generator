import json

def fetch_input(message="input"):
	''' take input from user '''

	# python 2 and 3 supported
	try:
		user_input = raw_input("%s : " % message)
	except NameError:
		user_input = input("%s : " % message)

	return user_input

def get_question_details(no_of_questions):
	unique_questions, counter = [], 1
	flag, error_retries = False, 0
	questions_map = []

	def error_log(message=''):
		''' error print '''
		if not message:
			message = 'Question details not entered correctly. Please enter again'

		print(message)

	print('\n\nEnter Question Name (unique), Difficulty (easy, medium or hard), Marks (integer) - '\
		+ '(separated by space, comma or tilda)')

	while counter <= no_of_questions:
		if error_retries > 5:
			flag = True
			error_log('Max retries reached!')
			break

		temp = fetch_input("Details for Question {0}".format(counter))

		delimeter = ',' if ',' in temp else '~' if '~' in temp else ' ' if ' ' in temp else None

		if not delimeter:
			error_retries += 1
			error_log()
			continue

		temp = [d.strip() for d in temp.split(delimeter)]
		if len(temp) < 3 or temp[0] in unique_questions or not temp[2].isdigit() or \
			temp[1] not in ['easy', 'medium', 'hard']:
			error_retries += 1
			error_log()
			continue

		questions_map.append({'question': temp[0], 'difficulty': temp[1], 'marks': int(temp[2])})
		unique_questions.append(temp[0])
		counter += 1

	if flag or error_retries>=5:
		return

	print(questions_map)
	return questions_map

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

	# get question details
	questions_map = get_question_details(no_of_questions)

	if not questions_map:
		return

if __name__ == "__main__":
	# main controller
	controller()
