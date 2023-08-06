### Description-概述：预测泰坦尼克上哪些人存活

#### Start here if...

You're new to data science and machine learning, or looking for a simple intro to the Kaggle prediction competitions.

#### Competition Description

The sinking of the RMS Titanic is one of the most infamous shipwrecks in history.  On April 15, 1912, during her maiden voyage, the Titanic sank after colliding with an iceberg, killing 1502 out of 2224 passengers and crew. This sensational tragedy shocked the international community and led to better safety regulations for ships.

One of the reasons that the shipwreck led to such loss of life was that there were not enough lifeboats for the passengers and crew. Although there was some element of luck involved in surviving the sinking, some groups of people were more likely to survive than others, such as women, children, and the upper-class.

In this challenge, we ask you to complete the analysis of what sorts of people were likely to survive. In particular, ***we ask you to apply the tools of machine learning to predict which passengers survived the tragedy***.



### Evaluation-评价方法：准确率

#### Goal

It is your job to predict if a passenger survived the sinking of the Titanic or not. 
For each PassengerId in the test set, you must predict a 0 or 1 value for the Survived variable.

#### Metric

Your score is the percentage of passengers you correctly predict. This is known simply as ["accuracy”](https://en.wikipedia.org/wiki/Accuracy_and_precision#In_binary_classification).

#### Submission File Format

You should submit a csv file with exactly 418 entries **plus** a header row. Your submission will show an error if you have extra columns (beyond PassengerId and Survived) or rows.

The file should have exactly 2 columns:

- PassengerId (sorted in any order)
- Survived (contains your binary predictions: 1 for survived, 0 for deceased)

```
PassengerId,Survived
 892,0
 893,1
 894,0
 Etc.
```

You can download an example submission file (gender_submission.csv) on the [Data page](https://www.kaggle.com/c/titanic/data).





### Data Dictionary：数据字典

| **Variable** | **Definition**                                               | **Key**                                        |
| ------------ | ------------------------------------------------------------ | ---------------------------------------------- |
| survival     | Survival                                                     | 0 = No, 1 = Yes                                |
| pclass       | Ticket class 票等级                                          | 1 = 1st, 2 = 2nd, 3 = 3rd                      |
| sex          | Sex                                                          |                                                |
| Age          | Age in years                                                 |                                                |
| sibsp        | of siblings / spouses aboard the Titanic 兄妹或配偶在船上的数量 |                                                |
| parch        | of parents / children aboard the Titanic 父母或孩子在船上的数量 |                                                |
| ticket       | Ticket number 票号                                           |                                                |
| fare         | Passenger fare 票价                                          |                                                |
| cabin        | Cabin number 船舱号                                          |                                                |
| embarked     | Port of Embarkation 登船口                                   | C = Cherbourg, Q = Queenstown, S = Southampton |





### 思路

1. 将数值型特征分组变成分类（也称为标称，离散）特征，以及填充一些缺失值
2. 因为原特征还是比较少的，故构建联合特征，如有A/B/C特征的话，可以构建成 A/B/C/AB/AC/BC/ABC
3. 初步筛选特征，去掉某个特征值比列高于80%的特征，以及联合特征与因变量相关性远低于未组合前的相关系，并记录下这种特征构建方法
4. 将特征统一处理成 “one-of-K” 或 “one-hot” 编码
5. 输入到logistic模型训练

