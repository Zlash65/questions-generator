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

def get_question_paper_details():
	def error_log(message=''):
		''' error print '''
		if not message:
			message = 'Question paper details entered improperly.'

		print(message)

	print('\nEnter Question Paper details - Total Marks (integer), '\
		+ 'Percentage weightage for each distinct difficulty level (comma separated)')
	print('ex:- 20, easy 25, medium 50, hard 25')

	question_paper_details = fetch_input()
	question_paper_map = {}

	temp = [d.strip() for d in question_paper_details.split(',')]
	if len(temp) < 4:
		print('Question paper details not correctly entered')
	else:
		question_paper_map['total_marks'] = temp[0]
		question_paper_map['difficulty'] = {}
		for d in temp[1:4]:
			diff = d.split(' ')
			if len(diff) < 2:
				print('Question paper details not correctly entered')
				break
			else:
				question_paper_map['difficulty'][diff[0]] = diff[1]

	try:
		if (not str(question_paper_map['total_marks']).isdigit()) or \
			(not str(question_paper_map['difficulty']['easy']).isdigit()) or \
			(not str(question_paper_map['difficulty']['medium']).isdigit()) or \
			(not str(question_paper_map['difficulty']['hard']).isdigit()):
			error_log()
			return

		if (int(question_paper_map['difficulty']['easy'])+int(question_paper_map['difficulty']['medium'])+int(question_paper_map['difficulty']['hard'])) != 100:
			error_log("Weightage didn't add up to 100")
			return

		question_paper_map['total_marks'] = int(question_paper_map['total_marks'])
		question_paper_map['difficulty'] = {k: int(v) for k,v in question_paper_map['difficulty'].items()}
		return question_paper_map
	except:
		error_log()
		return

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

	# get details for setting question paper
	question_paper_map = get_question_paper_details()

	if not question_paper_map:
		# print('Invalid format for question paper details. Please try again.')
		return

if __name__ == "__main__":
	# main controller
	controller()
