# import surprise
# print(surprise.__version__)
# import pandas as pd
# from surprise import Reader, Dataset
# from surprise import SVD
# from surprise import accuracy
# from surprise.model_selection import train_test_split
# import surprise as surprise

def get_not_buy_surprise(ratings, pro_df, userId):
    buying_pro = ratings[ratings['CUSTNO']==userId]['SGROUP'].tolist()
    
    # 모든 상품의 SGROUP를 리스트로 생성.
    total_pro = pro_df['SGROUP'].tolist()
    
    # 모든 상품의 SGROUP 중 이미 구매한 상품의 SGROUP를 제외한 후 리스트로 생성
    not_buy_pro = [ pro for pro in total_pro if pro not in buying_pro]
    # print('구매했던 제품 수:', len(buying_pro), '추천 대상 제품 수:', len(not_buy_pro), '전체 제품 수:', len(total_pro))
    
    return not_buy_pro

def recomm_pro_by_surprise(algo, userId, not_buy_pro, items, top_n=10):
    # 알고리즘 객체의 predict() 메서드를 평점이 없는 영화에 반복 수행한 후 결과를 list 객체로 저장
    predictions = [ algo.predict(str(userId), str(proid)) for proid in not_buy_pro ]
    
    # prediction list 객체는 surprise의 Predictions 객체를 원소로 가지고 있음.
    # [Prediction(uid='9', iid='1', est=3.69), Prediction(uid='9', iid='2', est=2.98),,,,]
    
    # 이를 est 값으로 정렬하기 위햇 아래의 sortkey_est 함수를 정의함.
    # sortkey_est 함수는 list 객체의 sort() 함수의 키 값으로 사용되어 정렬 수행.
    def sortkey_est(pred):
        return pred.est
    
    # sortkey_est() 반환값의 내림 차순으로 정렬 수행하고 top_n개의 최상위 값 추출.
    predictions.sort(key=sortkey_est, reverse=True)
    top_predictions = predictions[:top_n]
    
    # top_n으로 추출된 상품의 정보 추출. 상품 코드, 추천 예상 지수, 분류별 삼품명
    # est - 예상 평점
    top_pro_ids = [ pred.iid for pred in top_predictions ]
    top_pro_rating = [ pred.est for pred in top_predictions ]
    top_pro_bgroup = items[items.SGROUP.isin(top_pro_ids)]['대분류명']
    top_pro_mgroup = items[items.SGROUP.isin(top_pro_ids)]['중분류명']
    top_pro_sgroup = items[items.SGROUP.isin(top_pro_ids)]['소분류명']    
    top_pro_scode = items[items.SGROUP.isin(top_pro_ids)]['상품등급']        
    
    top_pro_preds = [ (id, rating, bgroup, mgroup, sgroup, scode) \
                     for id, rating, bgroup, mgroup, sgroup, scode in zip(top_pro_ids, 
                                                                     top_pro_rating,
                                                                     top_pro_bgroup,
                                                                     top_pro_mgroup,
                                                                     top_pro_sgroup,
                                                                     top_pro_scode
                                                                    ) ]

    return top_pro_preds

def get_not_buy_member_item(userId, top_n=10):
    # import pickle    
    # #import pickle5 as pickle
    # #print('__file__',__file__)
    # #print('pickle.format_version',pickle.format_version)

    # # 데이터 로드
    # with open('/mnt/c/Users/admin/workspace/web_project/lmembers/algo.pkl', 'rb') as f:
    #     algo = pickle.load(f)

    # with open('/mnt/c/Users/admin/workspace/web_project/lmembers/ratings.pkl', 'rb') as f:
    #     ratings = pickle.load(f)    

    # with open('/mnt/c/Users/admin/workspace/web_project/lmembers/items.pkl', 'rb') as f:
    #     items = pickle.load(f)       
    
    not_buy_pro = get_not_buy_surprise(ratings, items, userId)
    top_pro_preds = recomm_pro_by_surprise(algo, userId, not_buy_pro, items, top_n=top_n)

    #print('#### Top-10 추천 제품 리스트 ####')
    #for top_pro in top_pro_preds:
    #    print(top_pro[0], ':', top_pro[1], top_pro[2], top_pro[3], top_pro[4], top_pro[5])
       
    return top_pro_preds

# import time
# start = time.time()  # 시작 시간 저장

# print('#### Top-10 추천 제품 리스트 ####')
# top_pro_preds = get_not_buy_member_item(1000)
# for top_pro in top_pro_preds:
#     print(top_pro[0], ':', top_pro[1], top_pro[2], top_pro[3], top_pro[4], top_pro[5])

# print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간

# import pickle    
#import pickle5 as pickle
#print('__file__',__file__)
#print('pickle.format_version',pickle.format_version)

# import time
# start = time.time()  # 시작 시간 저장
# print("상품추천 로딩 시작 : ...")  # 현재시각 - 시작시간 = 실행 시간    
# # 데이터 로드
# with open('/mnt/c/Users/admin/workspace/web_project/lmembers/algo.pkl', 'rb') as f:
#     algo = pickle.load(f)

# with open('/mnt/c/Users/admin/workspace/web_project/lmembers/ratings.pkl', 'rb') as f:
#     ratings = pickle.load(f)    

# with open('/mnt/c/Users/admin/workspace/web_project/lmembers/items.pkl', 'rb') as f:
#     items = pickle.load(f)  

# print("상품추천 로딩 끝 :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간    