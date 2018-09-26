import requests
url = "https://srv11.akinator.com:9152/"
session = requests.get(url+"ws/new_session?callback=&partner=&player=website-desktop&uid_ext_session=&frontaddr=NDYuMTA1LjExMC40NQ==&constraint=ETAT%3C%3E%27AV%27")
data = session.json()
sessionID = data['parameters']['identification']['session']
signature = data['parameters']['identification']['signature']
step = 0
progThres = 85

#makes a request to the akinator servers and returns the next question or answer in JSON format
def nextStep(answer, step):
	response = {
		"type":"",
		"json":{}
	}
	nextstep = requests.get(url+"ws/answer?callback=&session="+sessionID+"&signature="+signature+"&step="+str(step)+"&answer="+answer)
	response['json'] = nextstep.json()
	response['type'] = 'question'
	if float(response['json']['parameters']['progression']) >= progThres:
		guessAnswer = requests.get(url+"ws/list?callback=&session="+sessionID+"&signature="+signature+"&step="+str(step+1))
		if guessAnswer.json()['completion'] == "OK":
			response['json'] = guessAnswer.json()
			response['type'] = "answer"	
	return response

#parses JSON object into either answer or question
def getResponse(jsonObj):
	response = {
		"question":"",
		"answer":""
	}

	if jsonObj == data:
		response['question'] = jsonObj['parameters']['step_information']['question']
	else:
		if jsonObj['type'] == 'answer':
			response['answer'] = jsonObj['json']['parameters']['elements'][0]['element']['name']
		else:
			response['question'] = jsonObj['json']['parameters']['question']

	return response	

#Stores all options the user can enter as an answer, use ansToNumber['ans'] to retrieve the corresponding number
ansToNumber = {
	"yes":'0',
	"y":'0',
	"n":'1',
	"no":'1',
	"idk":"2",
	"i dont know":"2",
	"prob":"3",
	"probably":"3",
	"prob not":"4",
	"probably not":"4"
}
#Introduction for new users
print "Shorthand for answers:"
print "y = yes"
print "n = no"
print "idk = i dont know"
print "prob = probably"
print "prob not = probably not"
print "you can use either, but make sure to spell it right or it will break the game"
#initialize a new session, print first question, and wait for response
ansInput = raw_input(getResponse(data)['question'])
#while loop that goes through each question.
while data:
	ansInput = ansToNumber[ansInput]
	print ""
	#if an answer is detected, print the answer and wait for user to respond
	if getResponse(nextStep(ansInput, step))['answer']:
		print "Your character is:"
		confirm=raw_input(getResponse(nextStep(ansInput, step))['answer'])
		if confirm == "y":
			break
		else:
			progThres += 10
			print ""
			ansInput = raw_input(getResponse(nextStep(ansInput, step))['question'])
	else:
		ansInput = raw_input(getResponse(nextStep(ansInput, step))['question'])
	step += 1

