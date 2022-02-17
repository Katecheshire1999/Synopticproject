import json

from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

from ibm_watson import NaturalLanguageUnderstandingV1

from ibm_watson.natural_language_understanding_v1 import Features, EmotionOptions

from flask import Flask, render_template, jsonify

from flask_restful import Resource, Api, request

app = Flask(__name__)

api = Api(app)


#
#
@app.route('/')
def index():
    return render_template('index.html')


@app.route('/train/', methods=['POST'])
def train():
    if request.method == "POST":
        print(request.get_json())
        result = biasdetect(request.get_json())
        print(result)
        return result


myList = ['brown bags', 'cakewalk', 'latino', 'oriental', 'native', 'english speaker', 'local', 'russel group',
          'native', 'illegal', 'immigrant', 'migrant', 'clean-shaven', 'hair', 'illegal', 'illegals', 'eskimo',
          'top university', 'top school', 'walk', 'kneel', 'run', 'bend', 'carry', 'carrying', 'lift', 'athletic',
          'climbing', 'fast', 'able-bodied', 'strong', 'upright', 'stationary', 'recent grad', 'young', 'active',
          'autonomously', 'courageously', 'headstrong', 'lead', 'self-sufficient', 'adventurous', 'boast', 'decide',
          'hierarchy', 'leads', 'self-sufficiently', 'aggressive', 'boasts', 'decisive', 'hierarchical', 'leader',
          'self-reliant', 'aggressively', 'boasting', 'decision', 'hostile', 'leading', 'self-reliance',
          'aggressiveness', 'boastful', 'hostiles', 'logic', 'aggression', 'boastfully', 'decisional', 'hostility',
          'masculine', 'ambition', 'challenge', 'determine', 'hostilely', 'objective', 'ambitious', 'he', 'she', 'him',
          'her', 'challenging', 'determines', 'impulsive', 'opinion', 'ambitiously', 'challenged', 'determined',
          'independent', 'outspoken', 'ambitiousness', 'challenges', 'determining', 'independents', 'persist',
          'analytical', 'challengingly', 'dominant', 'independence', 'principle', 'analytic', 'challengingly',
          'dominate', 'independence', 'principles', 'analyst', 'competition', 'dominates', 'independency', 'principled',
          'athlete', 'competitive', 'dominated', 'independently', 'reckless', 'athletic', 'competitiveness',
          'dominating', 'individual', 'stubborn', 'athletically', 'competitiveness', 'force', 'individuals', 'superior',
          'athletes', 'competitively', 'forces', 'individually', 'superior', 'athletics', 'confident', 'forcible',
          'intellect', 'self-confident', 'autonomy', 'courage', 'force', 'intellectually', 'self-confidence',
          'autonomous', 'courageous', 'greedy', 'intellectual', 'self-confidently']


def biasdetect(jobdesc):
    print('in biasdetect function', jobdesc)

    authenticator = IAMAuthenticator('KCj30y9BiViSobYMh_wzVk5RejqivEMOZZvRgqyBaU_y')
    natural_language_understanding = NaturalLanguageUnderstandingV1(
        version='2021-08-01',
        authenticator=authenticator
    )

    natural_language_understanding.set_service_url(
        'https://api.eu-gb.natural-language-understanding.watson.cloud.ibm.com')


    response = natural_language_understanding.analyze(
        text=jobdesc,
        features=Features(emotion=EmotionOptions())).get_result()

    # print(json.dumps(response, indent=2))
    emotionRatings = response['emotion']['document']['emotion']

    wordList = jobdesc.lower().strip().split(' ')
    matches = list(set(wordList).intersection(myList))

    if matches:
        return jsonify(
            message="We've found a match to some words which may be bias or subconciously gender-coded, and you may want to consider replacing them based on their context:",
            matches=matches,
            jobdesc=len(jobdesc),
            emotionRating=emotionRatings
        )
    else:
        return jsonify(
            message= "Looks good! There is no biased language detected.",
            matches = matches,
            jobdesc = len(jobdesc),
            emotionRating = emotionRatings
        )

# # Define Flask resource to act as API endpoint
# class biasdetect(Resource):
#     def get(self, jobdesc):
#         # Process to retrieve track details, get recommendations, train classifier and get owner predictions.
#         print('in gunc')
#         print(jobdesc)
#         # Return the recommended tracks and the owner predictions.
#         return {'tracks': 'hello'}
#
#
# api.add_resource(biasdetect, '/train/<string:jobdesc>')
