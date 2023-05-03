from linkedin_api import Linkedin

class LinkedInBot:
    def __init__(self, username, password):
        api = Linkedin(username, password)
        print('Successfully logged in to LinkedIn...')
        self.conversations = []
        api_conversations = api.get_conversations()['elements']
        for i in range(5):
            try:
                urn = api_conversations[i]['entityUrn']
                urn = urn.split(':')[-1]
                conversation = api.get_conversation(urn)['elements']
                texts = [(self.get_sender(t), self.get_text_content(t)) for t in conversation]
                self.conversations.append(texts)
                print('Processed convo {}'.format(i))
            except:
                self.conversations.append(None)
                print('Error processing convo {}'.format(i))
                continue
        
    def print_conversation(self, texts):
        for t in texts:
            print(t[0]['first_name'] + ' ' + t[0]['last_name'] + ':\n')
            print(t[1])
            print('*' * 50 + '\n')

    def build_gpt_prompt(self, texts):
        prompt = 'This is a LinkedIn conversation between 2 people. You are a computer science student who is a software engineer.\n'
        for t in texts:
            prompt += t[0]['first_name'] + ' ' + t[0]['last_name'] + ':'
            prompt += t[1] + '\n'
        prompt += 'Now reply to the conversation. Make sure you are polite and concise. Remember not to decline or commit to anything, but rather respond by asking for more information. Your goal is to continue engaging with the other user while extracting useful information.\n'
        return prompt

    def get_sender(self, text):
        urn = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['objectUrn']
        first_name = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['firstName']
        last_name = text['from']['com.linkedin.voyager.messaging.MessagingMember']['miniProfile']['lastName']
        return {'urn': urn, 'first_name': first_name, 'last_name': last_name}
    
    def get_text_content(self, text):
        return text['eventContent']['com.linkedin.voyager.messaging.event.MessageEvent']['attributedBody']['text']

