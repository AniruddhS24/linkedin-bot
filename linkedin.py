from linkedin_api import Linkedin

class LinkedInBot:
    def __init__(self):
        self.api = None
        self.authenticated = False
        self.urn = None
        self.conversations = []

    def authenticate(self, username, password):
        try:
            self.api = Linkedin(username, password)
        except:
            return False
        self.authenticated = True
        self.urn = self.api.get_user_profile()['miniProfile']['objectUrn']
        return True
    
    def fetch_conversations(self):
        if not self.authenticated:
            raise Exception('LinkedIn API not initialized')
        api_conversations = self.api.get_conversations()['elements']
        for i in range(5):
            try:
                urn = api_conversations[i]['entityUrn']
                urn = urn.split(':')[-1]
                conversation = self.api.get_conversation(urn)['elements']
                texts = [self.process_texts(t) for t in conversation]
                self.conversations.append(texts)
                print('Processed convo {}'.format(i))
            except:
                self.conversations.append(None)
                print('Error processing convo {}'.format(i))
                continue

    def print_conversation(self, texts):
        for t in texts:
            print(t['first_name'] + ' ' + t['last_name'] + ':\n')
            print(t['message'])
            print('*' * 50 + '\n')

    def build_gpt_prompt(self, texts):
        prompt = 'This is a LinkedIn conversation between 2 people. You are a computer science student who is a software engineer.\n'
        for t in texts:
            prompt += t['first_name'] + ' ' + t['last_name'] + ':'
            prompt += t['message'] + '\n'
        prompt += 'Now reply to the conversation. Make sure you are polite and concise. Remember not to decline or commit to anything, but rather respond by asking for more information. Your goal is to continue engaging with the other user while extracting useful information.\n'
        return prompt

    def process_texts(self, text):
        urn = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['objectUrn']
        first_name = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['firstName']
        last_name = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['lastName']
        message = text['eventContent']['com.linkedin.voyager.messaging.event.MessageEvent']['attributedBody']['text']
        isme = urn == self.urn
        return {'urn': urn, 'first_name': first_name, 'last_name': last_name, 'isme': isme, 'message': message}
    