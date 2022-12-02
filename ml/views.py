from django.shortcuts import render
import joblib
import pandas as pd
from django.http import JsonResponse

# col_list = {'fare_cat' : [1,2,3,4], 'age_cat': [0,1,2,3,4], 'family': [0,1,2,3,4,5,6,7,8,9,10], 'sex_female': [0,1], 'sex_male': [0,1], 'embarked_C': [0,1], 'embarked_Q': [0,1], 'embarked_S': [0,1]}
col_list = {'AGE':[6, 5, 4, 3, 2, 1], '가구/인테_avg':[0., 1., 2., 3., 4., 5., 6.,7., 8., 9.], '일상_avg':[0., 1., 2., 3., 4., 5., 6.,7., 8., 9.],  '스포츠_avg':[0., 1., 2., 3., 4., 5., 6.,7., 8., 9.], '패션잡화_avg':[0., 1., 2., 3., 4., 5., 6.,7., 8., 9.], '교육/문화_avg':[0., 1., 2., 3., 4., 5., 6.,7., 8., 9.], 'avg_grade':[6., 2., 1., 3., 5., 4.], 'food_grade':[3., 4., 2., 6., 5., 1., 0.], 'fun_grade':[1.,2.,3.,4.,5.,6.], 'fresh_grade':[1.,2.,3.,4.,5.,6.], 'fashion_grade':[1.,2.,3.,4.,5.,6.], 'necce_grade':[1.,2.,3.,4.,5.,6.], 'sport_grade':[1.,2.,3.,4.,5.,6.], 'stuff_grade':[1.,2.,3.,4.,5.,6.], 'digital_grade':[1.,2.,3.,4.,5.,6.], 'edu_grade':[1.,2.,3.,4.,5.,6.], 'high_grade':[1.,2.,3.,4.,5.,6.], 'fre_grade':[1.,2.,3.,4.,5.,6.],  'grade':[6., 3., 4., 2., 5., 1., 0.]}

# Create your views here.
def inputdata(request):
    context = { 'lis' : col_list}

    return render(request, 'ml/inputdata.html', context)


def result(request):
    # cls = joblib.load('ml/tcl_model.pkl')
    cls = joblib.load('ml/model_L-members_rf.pkl')

    col_li = list(col_list)
    df = pd.DataFrame(columns=col_li)

    lis = []
    if request.POST:
        for i in col_li:
            lis.append(request.POST[i])   

        df.loc[0,:] = lis
        ans = cls.predict(df)
        if ans == 0:
            ans = "Down"
        else:
            ans = "Up"

        context = { 'lis' : lis, 'ans': ans }
    else:
        context = {}

    return render(request, "ml/result.html", context)
    #return JsonResponse(context)