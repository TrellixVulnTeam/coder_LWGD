import path
import json
Userfeaturefull=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserJoin_date','UserDescription','Usertweets_count',
                   'Userverified','UserNumphoto','UserIsInLargeCity']



Userfeaturesingle=['Userfollowers_count','Userfriends_count','UserrepitationScore',
                   'UserJoin_date','UserDescription','Usertweets_count',
                   'Userverified']


Textfeaturesingle=['lenthofTweet','NumChar','Capital',
                   'Smile','Sad','NumPositiveWords','NumNegativeWords','PositiveScoer',
                   'I','You','HeShe',
                   'Via','Stock','Question','Exclamation','QuestionExclamation']


Textfeaturesingle_old=['lenthofTweet','NumPositiveWords','PositiveScoer',
                   'I',
                   'Question','Exclamation','QuestionExclamation']

Tweetfeaturesingle=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites','ContainNEWS',
                    'Contain_videos','WotScore','UrlRankIn5000','UrlRank']


Tweetfeaturesingle_Old=['Hashtag','Menstion','numUrls','Retweets','Isretweet',
                    'NumPhotos','Favorites']

fullfeatureonly=['Ps','Qp','Qs']
creditScor=['creditScore']

AllfeaturesingleOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old
Allfeaturesingle=Userfeaturesingle+Textfeaturesingle+Tweetfeaturesingle


Allfeaturefull=Textfeaturesingle+Userfeaturefull+fullfeatureonly+Tweetfeaturesingle+['creditScore']
AllfeaturefullOld=Userfeaturesingle+Textfeaturesingle_old+Tweetfeaturesingle_Old#+['creditScore']
Allfeaturefullwithoutcredit=Textfeaturesingle+Userfeaturefull+fullfeatureonly+Tweetfeaturesingle
pickfeature= ['creditScore',
              'QuestionExclamation',
              'Exclamation',
              'UrlRankIn5000',
              'UserrepitationScore',
              'Usertweets_count',
              'Userfollowers_count',
              'UserIsInLargeCity',
              'Userverified',
              'ContainNEWS',
              'Hashtag',
              'Userfriends_count',
              'Question',
              'Menstion',
              'Contain_videos',
              'Isretweet',
              'I',
              'UserNumphoto',
              'numUrls',
              'NumChar',
              'NumNegativeWords']  #['WotScore']#+Userfeaturesingle+Textfeaturesingle_old+['Hashtag','Menstion','numUrls','Retweets','Isretweet','NumPhotos','Favorites']

def getNewsEventID():
    id=[]
    with open (path.Featurepath+'descriptionNews.txt',encoding='utf-8',mode='r') as text:
        for line in text:
            id.append(json.loads(line)['eventID'])
    return id

def getRumorEventID():
    id=[]
    with open (path.Featurepath+'featuresRumors.txt',encoding='utf-8',mode='r') as text:
        for line in text:
            id.append(json.loads(line)['eventID'])
    return id

def getAllEventID():

    return getRumorEventID()+getNewsEventID()