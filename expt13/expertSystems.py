knowledge_base = {
    'Hardware Overheating': ['loud fan noise', 'sudden shutdowns', 'laptop feels very hot', 'system freezing'],
    'Malware Infection': ['frequent pop-ups', 'unfamiliar programs installed', 'system freezing', 'browser redirects'],
    'Network Connection Issue': ['cannot access websites', 'wifi drops frequently', 'yellow triangle on network icon', 'slow download speeds'],
    'Failing Hard Drive': ['clicking or grinding noise', 'frequent blue screens', 'corrupted files', 'system freezing']
}

def inference(observed_signs):
    probability = {}
    for problem in knowledge_base.keys():
        count = 0
        for sign in knowledge_base[problem]:
            if sign in observed_signs:
                count += 1
        probability[problem] = count / len(knowledge_base[problem])
        
    max_probability = max(probability.values())
    likely_problems = [problem for problem, prob in probability.items() if prob == max_probability]
    
    print("\n")
    if max_probability == 1:
        print('Diagnosis: Your computer is definitely experiencing a ' + ', '.join(likely_problems) + '.')
    elif max_probability > 0:
        print('Diagnosis: Your computer might be experiencing a ' + ', '.join(likely_problems) + '.')
    else:
        print('Diagnosis: Could not identify the exact computer issue based on inputs.')

def ques_set():
    observed_signs = []
    questions = []
    
    for problem in knowledge_base.keys():
        questions += knowledge_base[problem]
        
    questions = list(set(questions))
    
    print('Answer the following questions about your computer: ')
    for question in questions:
        answer = input(f'Are you experiencing this: {question}? [Y/N]: ')
        if answer.lower() == 'y':
            observed_signs.append(question)
            
    return observed_signs

def make_decision():
    max_questions = 1 
    ques_count = 0
    observed_signs = []
    
    while ques_count < max_questions:
        observed_signs += ques_set()
        ques_count += 1
        
        if observed_signs:
            inference(observed_signs)
            return 
            
    if ques_count >= max_questions:
        print('\nMaximum number of questions reached. Unable to make a decision based on the given information.')

if __name__ == "__main__":
    make_decision()