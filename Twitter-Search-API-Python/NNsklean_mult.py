from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor
import path
import json
import time
import numpy as np
from sklearn import datasets, metrics
from random import shuffle
import featuresdecription
# p=np.array([1,2,3,4,5])
# print(p.reshape(-1, 1))
# # shuffle(p)
# print(p)
import multiprocessing
from multiprocessing import Pool

def read_data():
    listofrumorevents=dict()
    listofnewsevents=dict()


    with open(path.Featurepath+'featuresRumors.txt',encoding='utf-8', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofrumorevents[JSON['eventID']]=(JSON['data'])

    with open(path.Featurepath+'featuresNews.txt',encoding='utf-8', mode='r') as writer:
        for line in writer:
            JSON=json.loads(line)
            listofnewsevents[JSON['eventID']]=(JSON['data'])
    return listofrumorevents,listofnewsevents

    # lenthofrumor=len(listofrumor)
    # print(lenthofrumor)
    # lenthofnews=len(listofnews)
    # shuffle(listofrumor)
    # shuffle(listofnews)
    #
    # print(lenthofnews)
    # minsize=min(len(listofrumor),len(listofnews))
    # mintrainsize=int(0.89*minsize)
    # mintestsize=int(0.1*minsize)
    # rumortrainsize=int(0.89*lenthofrumor)
    # newstrainsize=int(0.89*lenthofnews)
    # rumortestsize=int(0.1*lenthofrumor)
    # newstestsize=int(0.1*lenthofnews)

def getFeauture(tweet):
    features=tweet['features']
    featureslist=[]
    for featureIndex in featuresdecription.Allfeaturesingle:
        featureslist.append(features[featureIndex])
    return featureslist

def StandardFit(x_train,x_test):
    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    # Don't cheat - fit only on training data
    scaler.fit(x_train)
    #x_train = scaler.transform(x_train)
    # apply same transformation to test data
    x_test = scaler.transform(x_test)
    return x_train,x_test



def getTestAndTrainSetsSingle(trainEventIDlist,testEventIDlist,listofrumorevents,listofnewsevents):

    x_train=list()
    y_train=list()

    x_test=list()
    y_test=list()

    for trainEventID in trainEventIDlist:
        isRumor=-1
        if trainEventID in listofrumorevents:
            event=listofrumorevents[trainEventID]
            isRumor=1
        else:
            event=listofnewsevents[trainEventID]
        if event == None:
            raise NameError(trainEventID)

        for tweet in event :
                featureslist = getFeauture(tweet)
                x_train.append(featureslist)
                y_train.append(isRumor)

    for testEventID in testEventIDlist:
        isRumor=-1
        if testEventID in listofrumorevents.keys():
            event=listofrumorevents[testEventID]
            isRumor=1
        else:
            event=listofnewsevents[testEventID]
        if event == None:
            raise NameError(testEventID)

        for tweet in event :
                featureslist = getFeauture(tweet)
                x_test.append(featureslist)
                y_test.append(isRumor)


    x_train=np.array(x_train)
    y_train=np.array(y_train)
    x_test=np.array(x_test)
    y_test=np.array(y_test)

    from sklearn.preprocessing import StandardScaler
    scaler = StandardScaler()
    # Don't cheat - fit only on training data
    scaler.fit(x_train)
    x_train = scaler.transform(x_train)
    # apply same transformation to test data
    x_test = scaler.transform(x_test)


    return x_train,y_train,x_test,y_test,scaler



# Multinomial Naive Bayes Classifier
def naive_bayes_classifier(train_x, train_y):
    from sklearn.naive_bayes import MultinomialNB
    model = MultinomialNB(alpha=0.01)
    model.fit(train_x, train_y)
    return model


# KNN Classifier
def knn_classifier(train_x, train_y):
    from sklearn.neighbors import KNeighborsClassifier
    model = KNeighborsClassifier()
    model.fit(train_x, train_y)
    return model


# Logistic Regression Classifier
def logistic_regression_classifier(train_x, train_y):
    from sklearn.linear_model import LogisticRegression
    model = LogisticRegression(penalty='l2')
    model.fit(train_x, train_y)
    return model


# Random Forest Classifier
def random_forest_classifier(train_x, train_y):
    from sklearn.ensemble import RandomForestClassifier
    model = RandomForestClassifier(n_estimators=8)
    model.fit(train_x, train_y)
    return model


# Decision Tree Classifier
def decision_tree_classifier(train_x, train_y):
    from sklearn import tree
    model = tree.DecisionTreeClassifier()
    model.fit(train_x, train_y)
    return model


# GBDT(Gradient Boosting Decision Tree) Classifier
def gradient_boosting_classifier(train_x, train_y):
    from sklearn.ensemble import GradientBoostingClassifier
    model = GradientBoostingClassifier(n_estimators=200)
    model.fit(train_x, train_y)
    return model


# SVM Classifier
def svm_classifier(train_x, train_y):
    from sklearn.svm import SVC
    #model = SVC(kernel='rbf', probability=True)
    model = SVC(kernel='rbf',C=2,random_state=0)
    model.fit(train_x, train_y)
    return model

# SVM Classifier using cross validation
def svm_cross_validation(train_x, train_y):
    from sklearn.grid_search import GridSearchCV
    from sklearn.svm import SVC
    model = SVC(kernel='rbf', probability=True)
    param_grid = {'C': [1e-3, 1e-2, 1e-1, 1, 10, 100, 1000], 'gamma': [0.001, 0.0001]}
    grid_search = GridSearchCV(model, param_grid, n_jobs = 1, verbose=1)
    grid_search.fit(train_x, train_y)
    best_parameters = grid_search.best_estimator_.get_params()
    for para, val in best_parameters.items():
        print (para, val  )
    model = SVC(kernel='rbf', C=best_parameters['C'], gamma=best_parameters['gamma'], probability=True)
    model.fit(train_x, train_y)
    return model

# x_test = [[0., 0.], [1., 1.]]
# y = [[0, 1], [1, 1]]
def MLP(train_x, train_y):

    clf = MLPClassifier(activation='relu', algorithm='adam', alpha=1e-05,
           batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=False,
           epsilon=1e-08, hidden_layer_sizes=([16,16]), learning_rate='constant',
           learning_rate_init=0.01, max_iter=500, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
           tol=0.0001, validation_fraction=0.1, verbose=False,
           warm_start=False)
    clf.fit(train_x, train_y)
    #score = metrics.accuracy_score(clf.predict((train_x)), (train_y))
    #print(score)
    return clf
def MLP_Regressor(train_x, train_y):

    clf = MLPRegressor(  alpha=1e-05,
           batch_size='auto', beta_1=0.9, beta_2=0.999, early_stopping=False,
           epsilon=1e-08, hidden_layer_sizes=([8,8]), learning_rate='constant',
           learning_rate_init=0.01, max_iter=500, momentum=0.9,
           nesterovs_momentum=True, power_t=0.5, random_state=1, shuffle=True,
           tol=0.0001, validation_fraction=0.1, verbose=False,
           warm_start=False)
    clf.fit(train_x, train_y)
    #score = metrics.accuracy_score(clf.predict((train_x)), (train_y))
    #print(score)
    return clf

def multisvm(testevent,eventids,listofrumorevents,listofnewsevents,selectclassifier):

    classifiers = {'NB':naive_bayes_classifier,
                   'MLPRE':MLP_Regressor,
                    'MLP':MLP,
                  'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM':svm_classifier,
                'SVMCV':svm_cross_validation,
                 'GBDT':gradient_boosting_classifier
    }
    x_train,y_train,x_test,y_test,scaler=getTestAndTrainSetsSingle(Sublist(eventids,[testevent]),[testevent],listofrumorevents,listofnewsevents)
    for  clf in selectclassifier:
        #print(str(testevent)+'    '+clf+' accuracy: %.2f%%' % (100 * 22))

        modelclf = classifiers[clf](x_train, y_train)
        # predict = modelclf.predict(x_test)
        #
        # accuracy = metrics.accuracy_score(y_test, predict)
        # print (str(testevent)+'    '+clf+' accuracy: %.2f%%' % (100 * accuracy))
        # writelog(str(testevent)+'    '+clf+' accuracy: %.2f%%' % (100 * accuracy))
        for testevent in eventids:
            if testevent!=303:
                continue
            x_train,y_train,x_test,y_test,scaler=getTestAndTrainSetsSingle(Sublist(eventids,[testevent]),[testevent],listofrumorevents,listofnewsevents)

            isRumor=-1
            if testevent in listofrumorevents:
                testevent=listofrumorevents[testevent]
                isRumor=1
            else:
                testevent=listofnewsevents[testevent]
            maplenthofTweet=[]
            for tweet in testevent:
                retdict={'tweetid':tweet['tweetid'],"features":{}}
                tweettest=np.array(getFeauture(tweet)).reshape(1, -1)
                #print(tweettest.ndim)
                tweettest=scaler.transform(tweettest)
                ret=modelclf.predict(tweettest)
                retdict["features"]['Isrumor']=ret[0]
                maplenthofTweet.append(retdict)
            maplenthofTweet={'eventID':testevent,'data':maplenthofTweet}
            outputFile=path.Featurepath+'tweetscore.txt'
            with open(outputFile, mode='a') as writer:
                    JSON=json.dumps(maplenthofTweet)
                    writer.write(JSON + '\n')


# score = metrics.accuracy_score(clf.predict((x_test)), (y_test))
# print(score)
def writelog(lin):
    with open(path.Featurepath+'output.txt',mode='a') as writer:
        writer.write(lin +'\n')

if __name__ == '__main__':
    data_file = "mnist.pkl.gz"
    thresh = 0.5
    model_save_file = None
    model_save = {}
    test_classifiers = [  'MLP',  'LR', 'RF', 'DT', 'GBDT','SVM']
    # test_classifiers = [ 'MLPRE','MLP']#,  'LR', 'RF', 'DT', 'SVM']
    #test_classifiers = [ 'MLP']#'KNN',

    classifiers = {'NB':naive_bayes_classifier,
                   'MLPRE':MLP_Regressor,
                    'MLP':MLP,
                  'KNN':knn_classifier,
                   'LR':logistic_regression_classifier,
                   'RF':random_forest_classifier,
                   'DT':decision_tree_classifier,
                  'SVM':svm_classifier,
                'SVMCV':svm_cross_validation,
                 'GBDT':gradient_boosting_classifier
    }

    print ('reading training and testing data...'  )
    listofrumorevents,listofnewsevents = read_data()
    eventids=[]
    for key in listofrumorevents.keys():
        eventids.append(key)
    for key in listofnewsevents.keys():
        eventids.append(key)
    def Sublist(a,b):
        ret=[]
        for ele in a:
            if ele not in b:
                ret.append(ele)
        return ret

    pool = Pool(processes=4)
    for testevent in eventids:


        pool.apply_async(multisvm,args=(testevent,eventids,listofrumorevents,listofnewsevents,['SVM'],))
        #result = multisvm(testevent,eventids,listofrumorevents,listofnewsevents,['SVM','LR','MLP'])

##########################
    pool.close()
    pool.join()


    # for testevent in eventids:
    #     if testevent!=303:
    #         continue
    #     x_train,y_train,x_test,y_test,scaler=getTestAndTrainSetsSingle(Sublist(eventids,[testevent]),[testevent],listofrumorevents,listofnewsevents)
        #modelref = classifiers['MLPRE'](x_train, y_train)
        # for classifier in test_classifiers:
        #     modelclf = classifiers[classifier](x_train, y_train)
        #     predict = modelclf.predict(x_test)
        #
        #     accuracy = metrics.accuracy_score(y_test, predict)
        #     print (str(testevent)+'    '+classifier+' accuracy: %.2f%%' % (100 * accuracy))






        # isRumor=-1
        # if testevent in listofrumorevents:
        #     testevent=listofrumorevents[testevent]
        #     isRumor=1
        # else:
        #     testevent=listofnewsevents[testevent]
        # maplenthofTweet=[]
        # for tweet in testevent:
        #     retdict={'tweetid':tweet['tweetid'],"features":{}}
        #     tweettest=np.array(getFeauture(tweet)).reshape(1, -1)
        #     #print(tweettest.ndim)
        #     tweettest=scaler.transform(tweettest)
        #     ret=modelclf.predict(tweettest)
        #     retdict["features"]['credit_score']=ret[0]
        #     maplenthofTweet.append(retdict)
        # maplenthofTweet={'eventID':testevent,'data':maplenthofTweet}
        # outputFile=path.Featurepath+'tweetscore.txt'
        # with open(outputFile, mode='a') as writer:
        #         JSON=json.dumps(maplenthofTweet)
        #         writer.write(JSON + '\n')








# accuracy: 54.51%
# accuracy: 84.91%
# accuracy: 89.84%
# accuracy: 25.58%
# accuracy: 40.71%
# accuracy: 61.47%
# accuracy: 11.37%
# accuracy: 97.97%
# accuracy: 79.79%
# accuracy: 18.00%
# accuracy: 37.82%
# accuracy: 69.49%
# accuracy: 36.36%
# accuracy: 90.70%
# accuracy: 63.37%
# accuracy: 93.90%
# accuracy: 31.62%
# accuracy: 47.62%
# accuracy: 78.57%
# accuracy: 91.89%
# accuracy: 64.57%





        # num_train, num_feat = train_x.shape
        # num_test, num_feat = test_x.shape
        #
        # is_binary_class = (len(np.unique(train_y)) == 2)
        # print ('******************** Data Info *********************' )
        # print ('#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat)  )
        #
        # for classifier in test_classifiers:
        #     print ('******************* %s ********************' % classifier)
        #     start_time = time.time()
        #     model = classifiers[classifier](train_x, train_y)
        #     print ('training took %fs!' % (time.time() - start_time))
        #     predict = model.predict(test_x)
        #     # for i in range(len(predict)):
        #     #     print(str(test_y[i])+'      '+str(predict[i]))
        #     if model_save_file != None:
        #         model_save[classifier] = model
        #     if is_binary_class:
        #         precision = metrics.precision_score(test_y, predict)
        #         recall = metrics.recall_score(test_y, predict)
        #         print( 'precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        #     accuracy = metrics.accuracy_score(test_y, predict)
        #     print ('accuracy: %.2f%%' % (100 * accuracy))






















        # getTestAndTrainSetsSingle()
        # num_train, num_feat = train_x.shape
        # num_test, num_feat = test_x.shape
        #
        # is_binary_class = (len(np.unique(train_y)) == 2)
        # print ('******************** Data Info *********************' )
        # print ('#training data: %d, #testing_data: %d, dimension: %d' % (num_train, num_test, num_feat)  )
        #
        # for classifier in test_classifiers:
        #     print ('******************* %s ********************' % classifier)
        #     start_time = time.time()
        #     model = classifiers[classifier](train_x, train_y)
        #     print ('training took %fs!' % (time.time() - start_time))
        #     predict = model.predict(test_x)
        #     # for i in range(len(predict)):
        #     #     print(str(test_y[i])+'      '+str(predict[i]))
        #     if model_save_file != None:
        #         model_save[classifier] = model
        #     if is_binary_class:
        #         precision = metrics.precision_score(test_y, predict)
        #         recall = metrics.recall_score(test_y, predict)
        #         print( 'precision: %.2f%%, recall: %.2f%%' % (100 * precision, 100 * recall))
        #     accuracy = metrics.accuracy_score(test_y, predict)
        #     print ('accuracy: %.2f%%' % (100 * accuracy))


        