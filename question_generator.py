import argparse
import json
import traceback
import itertools

tracker = 1

def fetch_input(message="input"):
	''' taking input from user '''

	# python 2 and 3 supported
	try:
		user_input = raw_input("%s : " % message)
	except NameError:
		user_input = input("%s : " % message)

	return user_input

def get_question_details(no_of_questions, questions_map=[]):
	'''
		get details from user or read from file to formulate Question Store
		Question Store -
			[
				{
					'question' - should be unique
					'difficulty' - easy, medium or hard
					'marks' - marks pertaining to current question (integer)
				}
			]

		max retries allowed - 5

	'''

	unique_questions, counter = [], 1
	flag, error_retries = False, 0

	def error_log(message=''):
		''' error print '''
		if not message:
			message = 'Question details not entered correctly. Please enter again'

		print(message)

	# if question store not read from file
	if len(questions_map) == 0:
		print('\n\nEnter Question Name (unique), Difficulty (easy, medium or hard), Marks (integer) - '\
			+ '(separated by space, comma or tilda)')

		# iterating over to take all the three inputs for given no. of questions
		while counter <= no_of_questions:
			# break and exit if user enters wrong data repeatedly
			if error_retries > 5:
				flag = True
				error_log('Max retries reached!')
				break

			temp = fetch_input("Details for Question {0}".format(counter))

			# setting delimiter and checking if input is correctly entered
			delimeter = ',' if ',' in temp else '~' if '~' in temp else ' ' if ' ' in temp else None

			if not delimeter:
				error_retries += 1
				error_log()
				continue

			# check if data is properly entered with regard to their type and values they hold
			temp = [d.strip() for d in temp.split(delimeter)]
			if len(temp) < 3 or temp[0] in unique_questions or not temp[2].isdigit() or \
				temp[1] not in ['easy', 'medium', 'hard']:
				error_retries += 1
				error_log()
				continue

			questions_map.append({'question': temp[0], 'difficulty': temp[1], 'marks': int(temp[2])})
			unique_questions.append(temp[0])
			counter += 1
	else:
		# check if the data fetched from file follow the general norms of question store
		for d in questions_map:
			if len(d) < 3 or d['question'] in unique_questions or \
				not d['difficulty'] in ['easy', 'medium', 'hard'] or \
				not str(d['marks']).isdigit():
				print('Question details incorrect (in file)!')
				flag = True
				break

			d['marks'] = int(d['marks'])
			unique_questions.append(d['question'])

	# exit processing if flag is triggered or max retry attempted 
	if flag or error_retries>=5:
		return

	return questions_map

def get_question_paper_details(question_paper_map={}):
	'''
		get question paper overall detail or fetch from file
		Format - 
			{
				'total_marks' - integer value
				'difficulty' - {
					'easy' - weightage in terms of percentage of total_marks (integer)
					'medium' - weightage in terms of percentage of total_marks (integer)
					'hard' - weightage in terms of percentage of total_marks (integer)
				}
			}
	'''

	def error_log(message=''):
		''' error print '''
		if not message:
			message = 'Question paper details entered improperly.'

		print(message)

	# if question paper detail not read from file
	if len(question_paper_map) == 0:
		print('\nEnter Question Paper details - Total Marks (integer), '\
			+ 'Percentage weightage for each distinct difficulty level (comma separated)')
		print('ex:- 20, easy 25, medium 50, hard 25')

		question_paper_details = fetch_input()

		# validate user input according to format
		# else fallback to persistent input logic
		temp = [d.strip() for d in question_paper_details.split(',')]
		if len(temp) < 4:
			print('Question paper details not correctly entered')
			question_paper_map = get_question_paper_details_v2()
		else:
			question_paper_map['total_marks'] = temp[0]
			question_paper_map['difficulty'] = {}
			for d in temp[1:4]:
				diff = d.split(' ')
				if len(diff) < 2:
					print('Question paper details not correctly entered')
					question_paper_map = get_question_paper_details_v2()
					break
				else:
					question_paper_map['difficulty'][diff[0]] = diff[1]

	# validate overall mappings for file or user based input
	if (not str(question_paper_map['total_marks']).isdigit()) or \
		(not str(question_paper_map['difficulty']['easy']).isdigit()) or \
		(not str(question_paper_map['difficulty']['medium']).isdigit()) or \
		(not str(question_paper_map['difficulty']['hard']).isdigit()):
		error_log()
		return

	if (int(question_paper_map['difficulty']['easy'])+int(question_paper_map['difficulty']['medium'])+int(question_paper_map['difficulty']['hard'])) != 100:
		error_log("Weightage didn't add up to 100")
		return

	# normalize paper detail
	question_paper_map['total_marks'] = int(question_paper_map['total_marks'])
	question_paper_map['difficulty'] = {k: int(v) for k,v in question_paper_map['difficulty'].items()}
	return question_paper_map

def get_question_paper_details_v2():
	''' a more persistent method for taking input from user '''

	print('\nLets try another way')

	# keep trying till user gives proper input for total marks settings
	while True:
		total_marks = fetch_input('Enter total marks for the paper')
		if not total_marks.isdigit():
			print('Please enter an integer to denote marks')
		else:
			break

	# keep trying till user gives proper input for difficulty settings
	while True:
		easy = fetch_input('Enter weightage for difficulty level - easy')
		medium = fetch_input('Enter weightage for difficulty level - medium')
		hard = fetch_input('Enter weightage for difficulty level - hard')

		if not easy.isdigit() or not medium.isdigit() or not hard.isdigit():
			print('Please enter an integer to denote percentage weight out of 100')
			continue

		# break the loop if no issue encountered
		break

	question_paper_map = {'total_marks': total_marks, 'difficulty': {'easy': easy,
		'medium': medium, 'hard': hard}}

	return question_paper_map

def generate_questions(q_map, qp_map):
	'''
		Given all the details correctly,
		will generate a list of questions to be picked from Question Store
		that adds up to total marks following the percentage weightage of difficulties
	'''

	total_marks = qp_map['total_marks']

	questions = []
	for k, v in qp_map['difficulty'].items():
		marks = [d['marks'] for d in q_map if d['difficulty'] == k]
		weight = int(total_marks * v / 100)

		# generate combination of all possible marks for a given difficulty
		# that adds up to given weightage
		result = [seq for i in range(len(marks), 0, -1) for seq in itertools.combinations(marks, i) \
			if sum(seq) == weight]

		if not result:
			continue

		# picking the one with minimum no. of questions
		min_data = min(result, key=len)

		# extract question for the selected marks combination for given difficulty
		temp_map = {d['question']: d['marks'] for d in q_map if d['difficulty'] == k}
		for d in min_data:
			q = [i for i, j in temp_map.items() if j == d][0]
			temp_map.pop(q, None)
			questions.append(q)

	return questions

def controller(user=True, file_data={}):
	''' main flow controller '''

	global tracker

	# user based input
	if user:

		# input number of questions
		try:
			no_of_questions = fetch_input("Total number of questions")
			no_of_questions = int(no_of_questions)
		except ValueError:
			print('Please enter an integer to denote number of questions!')
			return

	# file based input
	elif file_data:
		no_of_questions = file_data['total_questions']

	# exit if invalid input
	if no_of_questions <= 0:
		print('No. of questions cannot be zero or lower in paper!')
		return

	# get question details
	questions_map = file_data.get('question_details', [])
	questions_map = get_question_details(no_of_questions, questions_map)

	# exit if invalid input
	if not questions_map:
		return

	# get details for setting question paper
	question_paper_map = file_data.get('question_paper_details', {})
	question_paper_map = get_question_paper_details(question_paper_map)

	# exit if invalid input
	if not question_paper_map:
		return

	# generating combination of questions to be used
	selector = generate_questions(questions_map, question_paper_map)
	print('Selected Questions - %s -' % tracker, ' , '.join(selector))
	tracker += 1

if __name__ == "__main__":

	# construct the argument parse and parse the arguments
	ap = argparse.ArgumentParser()

	ap.add_argument("-f", type=str, help="path to input json")
	ap.add_argument("--file", type=str, help="path to input json")
	args = vars(ap.parse_args())

	if args['file'] or args['f']:
		try:
			if args['file'] == 'default' or args['f'] == 'default':
				args['file'] = "inputs.json"

			with open(args['file']) as file_obj:
				data = json.loads(file_obj.read())

				if isinstance(data, (list, tuple)):
					for d in data:
						controller(user=False, file_data=d)
				elif isinstance(data, dict):
					controller(user=False, file_data=data)
				else:
					print("Cannot parse the file")

		except:
			print("Cannot open the file.")
			# traceback.print_exc()
	else:
		controller(user=True)
