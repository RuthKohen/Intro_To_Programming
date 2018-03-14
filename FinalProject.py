#!/usr/bin/env python

'''
IT FDN 100 B Wi 18 - 3-13-2018
Ruth Kohen Final Project

The PHQ-9 screening questionnaire for depression is widely used in clinical practice as a simple paper form
The functions contained in the PHQ9 class do the following:
1 - establish a time stamped entry for a specific client
2 - present questions to the client in sequential order
3 = make a diagnosis based on established cutoff criteria
4 - give clients feedback based on PHQ-9 score
5 - append the information to a csv file containing data from different clients
An additional function (outside of the PHQ9 class) reads the csv file with the aggregate data
'''

from datetime import datetime, date, time
import csv

class PHQ9():
    '''Contains functions to generate a session_id, ask all the PHQ-9 questions, returns feedback to client, and writes information to a csv file'''

    def __init__(self, session_time):
        self.session_time = session_time

    def gennerate_session_id(self, session_time):
    # asks for client first and last name and combines this with the timestamp into a session_id
        first0 = None
        last0 = None
        while first0 == None:
            first0 = input("Please give me your first name: ")
        first_name = first0.capitalize()
        while last0 == None:
            last0 = input("Please give me your last name: ")
        last_name = last0.capitalize()
        session_id = (first_name + last_name + session_time)
        return session_id

    def nine_questions(self):
    # asks the nine core questions of the PHQ-9 in order and returns the answers in a list
        questions = ("(1) Little interest or pleasure in doing things",
                     "(2) Feeling down, depressed, or hopeless",
                     "(3) Trouble falling or staying asleep, or sleeping too much",
                     "(4) Feeling tired or having little energy",
                     "(5) Poor appetite or overeating",
                     "(6) Feeling bad about yourself — or that you are a failure or have let yourself or your family down",
                     "(7) Trouble concentrating on things, such as reading the newspaper or watching television",
                     "(8) Moving or speaking so slowly that other people could have noticed? Or the opposite — being so fidgety or restless that you have been moving around a lot more than usual",
                     "(9) Thoughts that you would be better off dead or of hurting yourself in some way")
        responses = []
        print("\nI will now ask you nine questions about thoughts, emotions, or medical symptoms you may have experienced in the past two weeks."
                "\nFor each question, please chose from among four options to describe how often you have experienced the problem.")
        for q in questions:
            answer = None
            possible_responses = (0,1,2,3)
            print("\nOver the last two weeks, how often have you been bothered by the following:")
            print(q, "\n")
            print("Please enter \t'0'\t for 'not at all'.")
            print("Please enter \t'1'\t for 'several days' (within the last 14 days).")
            print("Please enter \t'2'\t for 'more than half the days' (within the last 14 days).")
            print("Please enter \t'3'\t for 'nearly every day' (within the last 14 days).")
            while answer not in possible_responses:
                try:
                    answer = int(input("Please enter a number between 0 and 3: "))
                except ValueError:
                    print("This was not a valid entry. Please choose a number between 0 and 3.")
            responses.append(answer)
        return responses

    def difficulty_question(self):
    # asks an additional question about symptom burden, and returns the answer
        difficulty_answer = None
        possible_responses = (0, 1, 2, 3)
        print("\nIf you have experienced any of the problems on this qustionnnaire so far, how difficult have these problems made it for you to do your work, take care of things at home, or get along with other people?\n")
        print("Please enter \t'0'\t for 'not difficult at all'.")
        print("Please enter \t'1'\t for 'somewhat difficult'.")
        print("Please enter \t'2'\t for 'very difficult'.")
        print("Please enter \t'3'\t for 'extremely difficult'.")
        while difficulty_answer not in possible_responses:
            try:
                difficulty_answer = int(input("Please enter a number between 0 and 3: "))
            except ValueError:
                print("This was not a valid entry. Please choose a number between 0 and 3.")
        return difficulty_answer

    def calculate_phq9_score(self, responses):
    # sums us individual responses to the nine core questions of the PHQ-9 to generate a sum score
        phq9_score = 0
        for r in responses:
            phq9_score = phq9_score + r
        return phq9_score

    def depression_diagnosis(self, responses, difficulty_answer, phq9_score):
    # uses inputs of client answers to establish the following symptom categories based on medical cutoff criteria;
    # depression symptoms present or not, possible major depression, depession severity, and suicide risk
        depression_diagnosis = "no"
        depression_symptoms = "not found"
        depression_severity = "none"
        suicide_risk = "absent"
        if ((responses[0] > 1 or responses[1] > 1) and difficulty_answer > 0):
            depression_diagnosis = "yes"
            depression_symptoms = "found"
        elif ((responses[0] > 0 or responses[1] > 0) and phq9_score >4):
            depression_symptoms = "found"
        if phq9_score > 20:
            depression_severity = "severe"
        elif phq9_score > 14:
            depression_severity = "moderately severe"
        elif phq9_score > 9:
            depression_severity = "moderate"
        elif phq9_score > 4:
            depression_severity = "mild"
        else:
            depression_severity = "none or minimal"
        if responses[8] > 0:
            suicide_risk = "present"
        return depression_diagnosis, depression_symptoms, depression_severity, suicide_risk

    def generate_feedback(self, phq9_score, depression_diagnosis, depression_symptoms, depression_severity, suicide_risk):
    # uses information generated by the depression diagnosis function to print a personalized output, simulating a clinic setting
        print("\n_________________________________________________________________________________________________")
        print("\nThank you for filling out our PHQ-9 questionnaire. Here is what the results show:\n")
        if depression_diagnosis == "no":
            print("You currently do not meet criteria for a diagnosis of major depression.")
            if depression_symptoms == "found":
                print("However, you may be experiencing some symptoms of depression.")
                print("Even without a formal diagosis, these depression symptoms might still cause you distress.")
                print("If you feel you are struggling now, or if things get worse over time, you might benefit from treatment.")
        else:
            print("You may be suffering from major depression of {} intensity.".format(depression_severity))
            print("Your health care provider will talk to you about treatment options today.")
        if suicide_risk == "present":
            print("Your health care provider will also want to talk to you about thoughts you may have about harming yourself.")
            # if I had more programming skill, I would model an email sent off to the health care provider at this stage
        print("\nPlease let your health care provider know if you have any questions or concerns about this questionnaire.")
        print("_________________________________________________________________________________________________\n")

    def generate_session_entry(self, session_id, responses, difficulty_answer, phq9_score, depression_diagnosis, depression_symptoms, depression_severity, suicide_risk):
    # generates a one-item dictionary with session_id as key and all other collceted or computed parameters as members of a tuple
    # prints the session entry for review
        session_data = (responses, difficulty_answer, phq9_score, depression_diagnosis, depression_symptoms, depression_severity, suicide_risk)
        session_entry = {session_id: session_data}
        print ("This is the entry for the session just completed: {}.".format(session_entry))
        return session_entry

    def write_session_entry(self, session_entry):
    # appends the session entry to a csv file
        with open("PHQ-9_collection.csv", "a", newline = "") as outfile:
            writer = csv.writer(outfile)
            for k, v in session_entry.items():
                writer.writerow([k,v])

def read_session_entries():
# reads a csv file with the collection of session entries as gateway to further actions(not in this script), and prints the entries
    print("Below is a list of entries collected so far:")
    with open("PHQ-9_collection.csv", "r", newline = "") as infile:
        reader = csv.reader(infile)
        for row in reader:
            print(row)

def main():
    timestamp = datetime.now().isoformat(timespec='minutes')
    client = PHQ9(session_time = timestamp)
    session_id = client.gennerate_session_id(session_time = timestamp)
    responses = client.nine_questions()
    difficulty_answer = client.difficulty_question()
    phq9_score = client.calculate_phq9_score(responses)
    depression_diagnosis, depression_symptoms, depression_severity, suicide_risk = client.depression_diagnosis(responses, difficulty_answer, phq9_score)
    client.generate_feedback(phq9_score, depression_diagnosis, depression_symptoms, depression_severity, suicide_risk)
    session_entry = client.generate_session_entry(session_id, responses, difficulty_answer, phq9_score, depression_diagnosis, depression_symptoms, depression_severity, suicide_risk)
    client.write_session_entry(session_entry)
    infile = read_session_entries()

if __name__ == '__main__':
    main()