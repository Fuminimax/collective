# coding: utf-8

'''
Created on 2009/10/21

@author: tryout
'''
from math import sqrt

critics = {'Lisa Rose': {'Lady in the Water': 2.5, 
                         'Snakes on a Plane': 3.5,
                         'Just My Luck': 3.0, 
                         'Superman Returns': 3.5, 
                         'You, Me and Dupree': 2.5, 
                         'The Night Listener': 3.0},
           'Gene Seymour': {'Lady in the Water':3.0,
                             'Snakes on a Plane': 3.5,
                            'Just My Luck': 1.5, 
                            'Superman Returns': 5.0, 
                            'The Night Listener': 3.0,
                            'You, Me and Dupree': 3.5},
           'Michael Phillips': {'Lady in the Water':2.5,
                                'Snakes on a Plane': 3.0,
                                'Superman Returns': 3.5, 
                                'The Night Listener': 4.0},
           'Claudia Puig': {'Snakes on a Plane': 3.5,
                             'Just My Luck': 3.0, 
                             'The Night Listener': 4.5,
                             'Superman Returns': 4.0,
                             'You, Me and Dupree': 2.5},
           'Mick LaSalle': {'Lady in the Water':3.0,
                            'Snakes on a Plane': 4.0,
                            'Just My Luck': 2.0,
                            'Superman Returns': 3.0, 
                            'The Night Listener': 3.0,
                            'You, Me and Dupree':2.0},
           'Jack Matthews': {'Lady in the Water':3.0,
                            'Snakes on a Plane': 4.0,
                            'The Night Listener': 3.0,
                            'Superman Returns': 5.0, 
                            'You, Me and Dupree': 3.5},
           'Toby': {'Snakes on a Plane': 4.5,
                    'You, Me and Dupree': 1.0,
                    'Superman Returns': 4.0}
           }

def sim_distance(prefs, person1, person2):
    si = {}
    for item in prefs[person1]:
        if item in prefs[person2]:
            si[item] = 1
            
    if len(si) == 0:
        return 0
    
    sum_of_squares = sum([pow(prefs[person1][item] - prefs[person2][item], 2)
                          for item in si])
    
    return 1/(1+sqrt(sum_of_squares))

def sim_pearson(prefs, p1, p2):
    si = {}
    for item in prefs[p1]:
        if item in prefs[p2]:
            si[item] = 1
            
    n = len(si)
    
    if n == 0:
        return 0;
    
    sum1 = sum([prefs[p1][it] for it in si])
    sum2 = sum([prefs[p2][it] for it in si])
    
    sum1Sq = sum([pow(prefs[p1][it], 2) for it in si])
    sum2Sq = sum([pow(prefs[p2][it], 2) for it in si])
    
    pSum = sum([prefs[p1][it] * prefs[p2][it] for it in si])
    
    num = pSum - (sum1 * sum2 / n)
    Sxx = sum1Sq - (pow(sum1, 2)/n)
    Syy = sum2Sq - (pow(sum2, 2)/n)
    den = sqrt(Sxx * Syy)
    
    if den == 0:
        return 0
    
    r = num / den
    
    return r

def topMatches(prefs, person, n=5, similarity=sim_pearson):
    scores = [(similarity(prefs, person, other), other)
              for other in prefs if other != person]
    
    scores.sort()
    scores.reverse()
    
    return scores[0:n]

def getRecommendations(prefs, person, similarity=sim_pearson):
    totals={}
    simSums={}
    
    # 評者を取り出す
    for other in prefs:
        # 自分だった場合は何もしない
        if other == person:
            continue
        
        # 評者の類似度を取得する
        sim = similarity(prefs, person, other)
        
        # 0以下のスコアは推薦相手として好ましくないので無視する
        if sim <= 0:
            continue
        
        # 評者のアイテムを取り出す
        for item in prefs[other]:
            # 自分の見ている映画以外を得点のみを算出
            if item not in prefs[person] or prefs[person][item] == 0:
                totals.setdefault(item, 0)
                # 自分の見ていない映画の評者の評点に類似度を掛け、合計する
                totals[item] += prefs[other][item] * sim
                
                simSums.setdefault(item, 0)
                # 評者の類似度を合計する
                simSums[item] += sim

    # totals からitemとtotalを取り出し計算
    rankings = [(total/simSums[item], item) for item, total in totals.items()]
    
    rankings.sort()
    rankings.reverse()
        
    return rankings

def transformPrefs(prefs):
    result = {}
    for person in prefs:
        for item in prefs[person]:
            result.setdefault(item, {})
            result[item][person] = prefs[person][item]
    
    return result