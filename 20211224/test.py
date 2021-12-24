import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib import style


from sklearn.preprocessing import StandardScaler,RobustScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report,confusion_matrix
from sklearn.metrics import roc_curve,roc_auc_score


def get_result_report(xtrain,ytrain,xtest,ytest,out_file):
    # model
    logreg = LogisticRegression()
    logreg.fit(xtrain, ytrain)
    ytest_pred = logreg.predict(xtest)

    # eval
    print("train set report:\n")
    print(classification_report(ytrain, logreg.predict(xtrain)))
    print("test set report:\n")
    print(classification_report(ytest, ytest_pred))
    # draw
    fpr, tpr, th = roc_curve(ytest, logreg.predict_proba(xtest)[:, 1])
    plt.figure(figsize=(20, 7))
    plt.plot(fpr, tpr, color='crimson')
    plt.xlabel("False Positive Rate", size=25)
    plt.ylabel("True Positive Rate", size=25)
    plt.title(f"AUC:{roc_auc_score(ytest, logreg.predict_proba(xtest)[:, 1])}")
    plt.savefig(out_file)
    plt.show()


def show_data(xtrain,ytrain,out_file):
    style.use('seaborn-darkgrid')
    data3 = pd.concat([xtrain,ytrain],axis=1)
    sns.pairplot(data3,hue='Exited')
    plt.savefig(out_file)
    plt.show()


if __name__ == "__main__":
    data = pd.read_csv("./Churn_Modelling.csv")
    data.info()
    col_n = ['Age','Balance','Exited']
    data1 = pd.DataFrame(data,columns=col_n)
    sns.pairplot(data1, hue='Exited')
    plt.savefig("org.jpg")
    plt.show()

    fig,ax = plt.subplots(figsize=(6,6),dpi=80)
    ax.set_title("Customer Exited or not")
    sns.countplot(data=data1,x='Exited')
    for p in ax.patches:
        ax.annotate(f'\n{p.get_height()}', (p.get_x(), p.get_height()+50), color='black', size=10)
    plt.savefig("count.jpg")
    plt.show()

    from sklearn.model_selection import StratifiedShuffleSplit
    data2 = pd.get_dummies(data1,drop_first=True)
    x = data2.drop("Exited",axis=1)
    y = data2["Exited"]
    sss = StratifiedShuffleSplit(test_size=0.1,n_splits=2)
    for train_ind,test_ind in sss.split(x,y):
        xtrain,xtest = x.iloc[train_ind,:],x.iloc[test_ind,:]
        ytrain,ytest = y[train_ind],y[test_ind]
    #
    # normalization
    scaler = RobustScaler()
    xtrain = pd.DataFrame(scaler.fit_transform(xtrain), columns=x.columns)
    xtest = pd.DataFrame(scaler.fit_transform(xtest), columns=x.columns)


    # original_result
    print("origin result as below:")
    get_result_report(xtrain, ytrain, xtest, ytest,out_file="0_report.jpg")
    show_data(xtrain,ytrain,out_file="0_org.jpg")


    #
    # # Random sample
    from imblearn.over_sampling import RandomOverSampler
    ros = RandomOverSampler(random_state=0)
    x_resample,y_resample = ros.fit_resample(xtrain,ytrain)
    show_data(x_resample, y_resample,out_file="1_random.jpg")
    print("Random sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="1_report.jpg")
    #
    # SMOTE
    from imblearn.over_sampling import SMOTE
    smo = SMOTE()
    x_resample,y_resample = smo.fit_resample(xtrain,ytrain)
    show_data(x_resample, y_resample, out_file="2_smote.jpg")
    print("SMOTE sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="2_report.jpg")

    # BorderLine SMOTE
    from imblearn.over_sampling import BorderlineSMOTE
    smo2 = BorderlineSMOTE()
    x_resample, y_resample = smo2.fit_resample(xtrain, ytrain)
    show_data(x_resample, y_resample, out_file="3_board_smote.jpg")
    print("BorderLine SMOTE sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="3_report.jpg")

    # KMeans SMOTE
    from imblearn.over_sampling import KMeansSMOTE
    smo3 = KMeansSMOTE(k_neighbors=2)
    x_resample, y_resample = smo3.fit_resample(xtrain, ytrain)
    show_data(x_resample, y_resample, out_file="4_kmeans_smote.jpg")
    print("Kmeans SMOTE sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="4_report.jpg")

    # SVM SMOTE
    from imblearn.over_sampling import SVMSMOTE
    smo4 = SVMSMOTE()
    x_resample, y_resample = smo4.fit_resample(xtrain, ytrain)
    show_data(x_resample, y_resample, out_file="5_svm_smote.jpg")
    print("SVM SMOTE sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="5_report.jpg")

    # ADASYN
    from imblearn.over_sampling import ADASYN
    ada = ADASYN()
    x_resample, y_resample = ada.fit_resample(xtrain, ytrain)
    show_data(x_resample, y_resample, out_file="6_SDASYN.jpg")
    print("ADASYN sample result as below:")
    get_result_report(x_resample, y_resample, xtest, ytest,out_file="6_report.jpg")

    #
    # # # SMOTE-NC
    # # from imblearn.over_sampling import SMOTENC
    # # smo5 = SMOTENC(categorical_features=[0],random_state=0)
    # # x_resample, y_resample = smo5.fit_resample(xtrain, ytrain)
    # # print("SMOTENC sample result as below:")
    # # get_result_report(x_resample, y_resample, xtest, ytest,x)
    #
    #
    #
