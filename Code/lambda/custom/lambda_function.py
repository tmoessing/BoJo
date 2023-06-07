from __future__ import print_function
import random
import boto3
dynamodb = boto3.resource('dynamodb')
table    = dynamodb.Table('BoJo')

# --------------- Helper Functions   ------------------

def get_caught_creature_list(session):
    
    try:
        response = table.get_item(
            Key={
                'userId': session["user"]["userId"]
            }
        )
        caught_creature_list = response['Item']['creature']
    except:
        caught_creature_list = []

    return caught_creature_list

def get_unique_creature_list(session):

    caught_creature_list = get_caught_creature_list(session)
    unique_creature_set  = set(caught_creature_list)
    unique_creature_list = list(unique_creature_set)

    return unique_creature_list

def get_available_creature_list(session):

    available_creature_list = [   'Gobolo',
						'Weltim',
						'Eggshem',
						'Hooteray',
						'Lipersnap',
						'Mitlew',
						'Mehsgge',
						'Yaretooth',
						'Pansrepil',
						'Olobog',
						'Netsil',
						'Rofopo',
						'Potxet',
						'Eteci',
						'Cieciov',
						'Ovaxela',
						'Srepeej'
						];

    return available_creature_list

def get_creature_ratio(session):
    unique_creature_list    = get_unique_creature_list(session)
    number_of_unique_creatures = len(unique_creature_list)

    available_creature_list = get_available_creature_list(session)
    number_of_available_creatures = len(available_creature_list)
    
    if number_of_unique_creatures > 1:
        creature_ratio = 'There are currently {} different types of creatures BoJo can catch.  We have caught {} different types of creatures. '.format(number_of_available_creatures, number_of_unique_creatures)
    elif number_of_unique_creatures == 1:
        creature_ratio = 'There are currently {} different types of creatures BoJo can catch. We have only caught {} type of creature.'.format(number_of_available_creatures, number_of_unique_creatures)
    elif number_of_unique_creatures == 0:
        creature_ratio = "There are currently {} different types of creatures BoJo can catch. We don't have any creatures. ".format(number_of_available_creatures )

    return creature_ratio

def get_common_speech_output(session):
    common_speech_output = '<break time="500ms"/>'                \
                         + 'Do you want to '                      \
                         + 'catch a creature, '                   \
                         + 'list your caught creatures, '         \
                         + 'or release duplicate creatures, '

    return common_speech_output

def get_common_reprompt_text(session):
    common_reprompt_text   = 'Say '                                 \
                           + 'catch a creature, '                   \
                           + 'list your caught creatures, '         \
                           + 'or release duplicate creatures, '     \

    return common_reprompt_text

def get_expanded_creater_list(creature_list):
    if len(creature_list) > 1:
        return 'We have a  {} and a {}'.format(', '.join(creature_list[:-1]), creature_list[-1])
    try:
        return 'We have a  {}'.format(creature_list[0])
    except IndexError:
        return 'We have not caught any creatures'

# --------------- Helpers that build all of the responses ----------------------

def build_speechlet_response(title, content, speech_output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': "<speak>" + speech_output + "</speak>"
        },
        'card': {
            'type': 'Simple',
            'title': title,
            'content': content
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_speechlet_response_with_image(title, content, creature_caught, speech_output, reprompt_text, should_end_session):

    smallImageUrl = 'https://s3.amazonaws.com/bojo-creatures/' + creature_caught + 'Small.png'
    largeImageUrl = 'https://s3.amazonaws.com/bojo-creatures/' + creature_caught + 'Large.png'
    
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': '<speak>' + speech_output + '</speak>'
        },
        'card': {
            'type': 'Standard',
            'title': title,
            'text': content,
            'image': {
                'smallImageUrl': smallImageUrl,
                'largeImageUrl': largeImageUrl
            }
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

def build_response(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


# --------------- Functions that control the skill's behavior ------------------

def handle_launch_request(session):
    """ If we wanted to initialize the session to have some attributes we could
    add those here
    """
    superlativesCreatureArray = ['aha',
					     'ahoy',
					     'all righty',
					     'bam',
					     'bingo',
					     'boing',
					     'boom',
					     'booya',
					     'cha ching',
					     'cheers',
					     'cowabunga',
					     'dynomite',
					     'eureka',
					     'fancy that',
					     'geronimo',
					     'giddy up',
					     'gotcha',
					     'great scott',
					     'hear hear',
					     'hip hip hooray',
					     'howdy',
					     'hurrah',
					     'huzzah',
					     'jeepers creeers',
					     'jiminy cricket',
					     'kaboom',
					     'kaching',
					     'kapow',
					     'katchow',
					     'kazaam',
					     'kerbam',
					     'kerboom',
					     'kerching',
					     'kerchoo',
					     'kerpow',
					     'mamma mia',
					     'oh my',
					     'oh snap',
					     'ooh la la',
					     'righto',
					     'squee',
					     'wahoo',
					     'whammo',
					     'woo hoo',
					     'wow',
					     'wowza',
					     'wowzer',
					     'yay',
					     'yippee',
					     'yowza',
					     'yowzer',
		                 'zoinks'
						];

    superlative = random.choice (superlativesCreatureArray)

    session_attributes = {}
    card_title      = 'Welcome '
    card_content    =  get_creature_ratio(session)           \
                    + 'Tell BoJo to '                        \
                    + 'catch a creature, '                   \
                    + 'list your caught creatures, '         \
                    + 'or release duplicate creatures, '     \


    speech_output   = '<say-as interpret-as="interjection">' + str(superlative) + ' </say-as>, '    \
                    + "I'm glad to see you, my name is BoJo! "                                       \
                    + get_creature_ratio(session)                                                   \
                    + get_common_speech_output(session)


    reprompt_text   =  get_common_reprompt_text(session)

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))


def handle_create_intent(intent, session):
    """ 
    Catch a creature
    """
    available_creature_list = get_available_creature_list(session)


    creature_caught = random.choice (available_creature_list)

    caught_creature_list = get_caught_creature_list(session)
    new_caught_creature_list = [creature_caught] + caught_creature_list

    table.put_item(
    Item={
            'userId': session["user"]["userId"],
            'creature':  new_caught_creature_list
        }
    )

    session_attributes = {}
    card_title      = "Congratulations"
    card_content    = "We caught a " + creature_caught

    speech_output   = 'There are many creatures out today! '                                          \
                    + " let's be very quiet, "                                                        \
                    + '<amazon:effect name="whispered"> and see if we can catch one.</amazon:effect>' \
                    + '<break time="1s"/>'                                                            \
                    + '<say-as interpret-as="interjection"> bada bing bada boom </say-as>'            \
                    + ', we caught a ' + creature_caught     \
                    + get_common_speech_output(session)

    reprompt_text   =  get_common_reprompt_text(session)

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response_with_image(
        card_title, card_content, creature_caught, speech_output, reprompt_text, should_end_session))

def handle_read_intent(intent, session):
    """ 
   Reads Creatures
    """   
    caught_creature_list = get_caught_creature_list(session)

    session_attributes = {}
    card_title      = "Creatures we have"
    card_content    = get_expanded_creater_list(caught_creature_list)   \
                    + get_creature_ratio(session)

    speech_output   = get_expanded_creater_list(caught_creature_list)   \
                    + '<break time="500ms"/>'                           \
                    + get_creature_ratio(session)                       \
                    + get_common_speech_output(session)

    reprompt_text   = get_common_reprompt_text(session)

    should_end_session = False
    
    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_delete_intent(intent, session):
    """ 
   deletes dupliciates Creatures
    """   
    unique_creature_list = get_unique_creature_list(session)

    table.put_item(
    Item={
            'userId': session["user"]["userId"],
            'creature': unique_creature_list
        }
    )   

    session_attributes = {}
    card_title      = "Creatures we have"
    card_content    = 'Done! Now ' + get_expanded_creater_list(unique_creature_list)

    speech_output   = 'Done! Now ' + get_expanded_creater_list(unique_creature_list)  \
                    + get_common_speech_output(session)

    reprompt_text   = get_common_reprompt_text(session)

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_help_intent(session):

    session_attributes = {}
    card_title      = "Try to catch all the creatures. "
    card_content    =  get_creature_ratio(session)           \
                    + 'Tell BoJo to '                        \
                    + 'catch a creature, '                   \
                    + 'list your caught creatures, '         \
                    + 'or release duplicate creatures, '

    speech_output   = 'Try to catch all the creatures. '       \
                    +  get_creature_ratio(session)           \
                    +  'Tell BoJo to '                       \
                    + 'catch a creature, '                   \
                    + 'list your caught creatures, '         \
                    + 'or release duplicate creatures, '

    reprompt_text   =  get_common_reprompt_text(session)

    should_end_session = False

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, reprompt_text, should_end_session))

def handle_end_intent():

    session_attributes = {}
    card_title      = "Good bye"
    card_content    = "Thanks for playing with BoJo, come back soon!"

    speech_output   = '<say-as interpret-as="interjection">okey dokey</say-as>. Thanks for playing with BoJo, come back soon!'

    should_end_session = True

    return build_response(session_attributes, build_speechlet_response(
        card_title, card_content, speech_output, None, should_end_session))

# --------------- Events ------------------

def on_session_started(session_started_request, session):
    """ Called when the session starts """

    print("on_session_started requestId=" + session_started_request['requestId']
          + ", sessionId=" + session['sessionId'])

def on_launch(launch_request, session):
    """ Called when the user launches the skill without specifying what they
    want
    """

    print("on_launch requestId=" + launch_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # Dispatch to your skill's launch
    return handle_launch_request(session)


def on_intent(intent_request, session):
    """ Called when the user specifies an intent for this skill """

    print("on_intent requestId=" + intent_request['requestId'] +
          ", sessionId=" + session['sessionId'])

    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    # Dispatch to your skill's intent handlers
    if intent_name == "CreateIntent" or intent_name == "CatchACreatureIntent":
        return handle_create_intent(intent, session)
    elif intent_name == "ReadIntent":
        return handle_read_intent(intent, session)
    elif intent_name == "DeleteIntent":
        return handle_delete_intent(intent, session)
    elif intent_name == "AMAZON.HelpIntent":
        return handle_help_intent(session)
    elif intent_name == "AMAZON.CancelIntent" or intent_name == "AMAZON.StopIntent":
        return handle_end_intent()
    else:
        print("what the what is " + intent_name)
        raise ValueError("Invalid intent")


def on_session_ended(session_ended_request, session):
    """ Called when the user ends the session.

    Is not called when the skill returns should_end_session=true
    """
    print("on_session_ended requestId=" + session_ended_request['requestId'] +
          ", sessionId=" + session['sessionId'])
    # add cleanup logic here


# --------------- Main handler ------------------

def lambda_handler(event, context):
    """ Route the incoming request based on type (LaunchRequest, IntentRequest,
    etc.) The JSON body of the request is provided in the event parameter.
    """
    print("event.session.application.applicationId=" +
          event['session']['application']['applicationId'])

    """
    Uncomment this if statement and populate with your skill's application ID to
    prevent someone else from configuring a skill that sends requests to this
    function.
    """
    if (event['session']['application']['applicationId'] !=
             "amzn1.ask.skill.2cd8cba1-cfab-418a-99a1-994975470325"):
         raise ValueError("Invalid Application ID")
    

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']},event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])
