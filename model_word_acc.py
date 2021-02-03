import pandas as pd
import numpy as np
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import OneHotEncoder
import time
from sklearn import decomposition
from sklearn.cluster import AgglomerativeClustering
from sklearn.cluster import KMeans
from sklearn import cluster, datasets, metrics
import pickle

dt_model = pickle.load(open('dt_model.pkl', 'rb'))
input_time = time.time()


def find_same_word(input_s, g_codes, db_path):
    df = pd.read_csv(db_path, sep=",", header=None, dtype="str")
    df_gcode = df.iloc[:, 2]
    df_name = df.iloc[:, 1]
    #     print(df_gcode)

    # 先找出同類別的商標們
    g_list = []
    no1_list = []
    n = 0
    a = len(df_gcode)
    for i in range(a):
        n += 1
        try:
            if str(df_gcode[i]) == str(g_codes):
                if df_name[i] not in g_list:
                    g_list.append(str(df_name[i]))
        except:
            pass
    # #有一樣字的就選出來
    # #把問題也加入 list
    output_list = [input_s]

    for j in str(input_s):
        b = len(g_list)
        for i in range(b):
            c = len(str(g_list[i]))
            for k in range(c):
                if str(j) == str(g_list[i])[k]:
                    if str(g_list[i]) not in output_list:
                        output_list.append(str(g_list[i]))
    new_df = pd.DataFrame(output_list, columns=["output"])
    #     new_df.to_csv("./data/input_temp.csv",index=False)

    # 2.one hot encoding
    #     df_input = pd.read_csv("./data/input_temp.csv")
    #     df = df_input['output']
    df = new_df['output']
    out_put_list = []
    for i in range(len(df)):
        out_put_one_list = []
        for j in df[i]:
            out_put_one_list.append(j)
        out_put_list.append(out_put_one_list)
    out_put_df = pd.DataFrame(out_put_list)
    dummy_df = pd.get_dummies(out_put_df)
    df_train_one_sk = pd.DataFrame(OneHotEncoder().fit_transform(dummy_df).toarray())
    array_train_one_sk = OneHotEncoder().fit_transform(dummy_df).toarray()

    # 3.PCA降維
    X_pca = array_train_one_sk
    pca = decomposition.PCA(n_components=5)
    X_pca_done = pca.fit_transform(X_pca)
    X_pca_df = pd.DataFrame(X_pca_done)

    # 4. 開始各種分群
    model_a1 = AgglomerativeClustering(n_clusters=15, linkage='average')
    c_a1 = model_a1.fit_predict(X_pca_done)
    label_a1 = pd.Series(model_a1.labels_)

    model_a2 = AgglomerativeClustering(n_clusters=15, linkage='complete')
    c_a2 = model_a2.fit_predict(X_pca_done)
    label_a2 = pd.Series(model_a2.labels_)

    model_a3 = AgglomerativeClustering(n_clusters=15, linkage='ward')
    c_a3 = model_a3.fit_predict(X_pca_done)
    label_a3 = pd.Series(model_a3.labels_)

    model_a4 = AgglomerativeClustering(n_clusters=15, linkage='single')
    c_a4 = model_a4.fit_predict(X_pca_done)
    label_a4 = pd.Series(model_a4.labels_)

    model_k1 = KMeans(n_clusters=15, init="random")
    c_k1 = model_k1.fit_predict(X_pca_done)
    label_k1 = pd.Series(model_k1.labels_)

    model_k2 = KMeans(n_clusters=15, init="k-means++")
    c_k2 = model_k2.fit_predict(X_pca_done)
    label_k2 = pd.Series(model_k2.labels_)

    clus_df = pd.DataFrame()
    clus_df["ag_average"] = label_a1
    clus_df["ag_complete"] = label_a2
    clus_df["ag_ward"] = label_a3
    clus_df["ag_single"] = label_a4
    clus_df["kmeans"] = c_k1
    clus_df["kmeans_plus"] = c_k2

    out_put_name_list = []
    for i in out_put_list:
        name = str(i).strip("[]").replace("'", "").replace(", ", "")
        out_put_name_list.append(name)
    df_n = pd.DataFrame(out_put_name_list)
    df_new = pd.concat([df_n, clus_df], axis=1)
    #     df_new.to_csv("./data/trained.csv",encoding="utf-8-sig")

    # 5. 和問題同群的有
    q_a_list = []
    for i in df_new.columns:
        q_a_list.append(df_new[i][0])
    all_list = []

    for j in range(1, len(q_a_list)):
        one_list = []
        one_no_list = []
        for k in range(1, len(df_new)):
            if str(df_new.iloc[:, j][k]) == str(q_a_list[j]):
                one_list.append(df_new.iloc[:, 0][k])
                one_no_list.append(df_new.iloc[:, -1][k])
        all_list.append(one_list)

    all_df = pd.DataFrame(all_list)

    # 6. 分群結果計算分數
    silhouette_a1 = metrics.silhouette_score(X_pca_done, label_a1)
    silhouette_a2 = metrics.silhouette_score(X_pca_done, label_a2)
    silhouette_a3 = metrics.silhouette_score(X_pca_done, label_a3)
    silhouette_a4 = metrics.silhouette_score(X_pca_done, label_a4)
    silhouette_k1 = metrics.silhouette_score(X_pca_done, c_k1)
    silhouette_k2 = metrics.silhouette_score(X_pca_done, c_k2)
    silhouette_score_list = [silhouette_a1, silhouette_a2, silhouette_a3, silhouette_a4, silhouette_k1, silhouette_k2]
    #     print(silhouette_score_list)
    n = len(silhouette_score_list)
    silhouette_percentage = []

    for i in silhouette_score_list:
        silhouette_percentage.append(float("{:.2f}".format((i / n) * 100)))
    #     print(silhouette_percentage )

    q_a_list = []
    for i in df_new.columns:
        q_a_list.append(df_new[i][0])
    unique_list = []
    for j in range(1, len(q_a_list)):
        #     one_list = []
        for k in range(1, len(df_new)):
            if str(df_new.iloc[:, j][k]) == str(q_a_list[j]):
                if df_new.iloc[:, 0][k] not in unique_list:
                    if df_new.iloc[:, 0][k] != None:
                        unique_list.append(df_new.iloc[:, 0][k])

    score_list = [0] * len(unique_list)
    for i in range(len(unique_list)):
        if unique_list[i] in all_list[0]:
            score_list[i] += silhouette_percentage[0]
        if unique_list[i] in all_list[1]:
            score_list[i] += silhouette_percentage[1]
        if unique_list[i] in all_list[2]:
            score_list[i] += silhouette_percentage[2]
        if unique_list[i] in all_list[3]:
            score_list[i] += silhouette_percentage[3]
        if unique_list[i] in all_list[4]:
            score_list[i] += silhouette_percentage[4]
        if unique_list[i] in all_list[5]:
            score_list[i] += silhouette_percentage[5]

    #     return unique_list, score_list

    # 7. 找前幾名相似商標(若小於五個，再找次高分的)
    #

    #     count = 0
    #     for i,j in zip(unique_list, score_list):
    #         if count < 30:
    #             if j == max(score_list):
    #                 count +=1
    #                 res5.append([i,j])
    #     print(unique_list)
    #     print(score_list)

    #     找最高分相似商標名(運算用)

    res = []
    count = 0
    score_list_sorted = sorted(score_list, reverse=True)
    new_score_list = []
    for i in score_list_sorted:
        if i not in new_score_list:
            new_score_list.append(i)
    for h in new_score_list:
        for i, j in zip(unique_list, score_list):
            if j == h:
                res.append([i, j])
                count += 1
        if count >= 5:
            break
    #     找前五名(顯示用)
    res5 = res[0:5]
    print(res)

    keys = []
    values = []
    dict_plaintiff = {}
    dict_defendant = {}

    for i in range(len(res)):
        keys.append(i)
    for i in range(len(keys)):
        values.append(res[i][0])
        dict_plaintiff[keys[i]] = input_s
        dict_defendant[keys[i]] = values[i]

    data = {'plaintiff': dict_plaintiff,
            'defendant': dict_defendant}
    df = pd.DataFrame(data)

    df.insert(2, 'len_difference', 0)
    df.insert(3, 'similar_rate1', 0.0)
    df.insert(4, 'similar_rate2', 0.0)
    df.insert(5, 'similar_rate3', 0.0)

    # 8. 建立前五相似商標之特徵值
    for i in range(len(df)):
        #         計算字元差異度
        df['len_difference'][i] = abs(len(df['plaintiff'][i]) - len(df['defendant'][i]))

        plaintiff_voc = []
        defendant_voc = []

        #         將原告、被告的每個字元加進新的list
        for j in df['plaintiff'][i]:
            plaintiff_voc.append(j)
        for k in df['defendant'][i]:
            defendant_voc.append(k)

        #         計算字元相似度
        a = 0
        for l in range(len(plaintiff_voc)):
            if plaintiff_voc[l] in defendant_voc:
                a += 1
        similar_rate1 = (a / len(plaintiff_voc) + a / len(defendant_voc)) / 2
        df['similar_rate1'][i] = similar_rate1

        #         列出原告、被告共同的字元
        plaintiff_voc_kind = list(set(plaintiff_voc))
        defendant_voc_kind = list(set(defendant_voc))
        both_kind = plaintiff_voc_kind + defendant_voc_kind
        both_kind = list(set(both_kind))
        both = []
        for n in range(len(plaintiff_voc)):
            if plaintiff_voc[n] in defendant_voc:
                both.append(plaintiff_voc[n])
        both_unique = []
        for o in both:
            if o not in both_unique:
                both_unique.append(o)
        both = both_unique

        #         計算字頻相似度
        b = 0
        for m in range(len(plaintiff_voc_kind)):
            if plaintiff_voc_kind[m] in defendant_voc_kind:
                b += 1
        similar_rate2 = b / len(both_kind)
        df['similar_rate2'][i] = similar_rate2

        #     print(plaintiff_voc)
        #     print(defendant_voc)
        #     print(both)

        #         原告、被告裡共同字元的順序分別為何
        plaintiff_index = []
        defendant_index = []
        for p in range(len(plaintiff_voc)):
            if plaintiff_voc[p] in both:
                plaintiff_index.append(both.index(plaintiff_voc[p]))
        for r in range(len(defendant_voc)):
            if defendant_voc[r] in both:
                defendant_index.append(both.index(defendant_voc[r]))
        #     print(plaintiff_index)
        #     print(defendant_index)
        if len(plaintiff_index) > len(defendant_index):
            shorter = defendant_index
            longer = plaintiff_index
        else:
            shorter = plaintiff_index
            longer = defendant_index

        #         計算順序相似度
        similar_rate3 = []
        for i in range(len(shorter) - 1):
            for j in range(len(longer) - 1):
                if shorter[i:i + 2] == longer[j:j + 2]:
                    k = i + 2
                    l = j + 2
                    while k < len(shorter) and l < len(longer):
                        if shorter[k] == longer[l]:
                            k += 1
                            l += 1
                        else:
                            break
                    n = k - i
                    similar_rate3.append(n)
        #     print(similar_rate3)
        try:
            if len(shorter) in similar_rate3:
                similar_rate3 = 1
            elif len(shorter) == 1 or len(longer) == 1:
                similar_rate3 = 0
            else:
                similar_rate3 = sum(similar_rate3) / len(shorter) / len(similar_rate3)
        except:
            similar_rate3 = 0
        df['similar_rate3'][i] = similar_rate3
    #     print(df1['similar_rate3'][i])

    #     對字元差異度進行標準化
    len_difference = (df.len_difference - df.len_difference.min()) / (df.len_difference.max() - df.len_difference.min())
    df['len_difference'] = len_difference
    df = df.round(4)
    # print(df)

    # 9. 判斷風險

    x_test = df[['len_difference', 'similar_rate1', 'similar_rate2', 'similar_rate3']]
    x_test = np.array(x_test, dtype=float)
    y_pred = dt_model.predict(x_test)
    x_test = pd.DataFrame(x_test)
    y_pred = pd.DataFrame(y_pred)
    result = pd.concat([df[['plaintiff', 'defendant']], x_test, y_pred], axis=1)
    print(result)
    y_pred = np.array(y_pred, dtype=float)

    if input_s in res:
        result = ['侵權風險', '極高']
    else:
        if y_pred.mean() >= 0.6:
            result = ['侵權風險', '高']
        elif y_pred.mean() >= 0.4:
            result = ['侵權風險', '中']
        else:
            result = ['侵權風險', '低']
    res5.append(result)
    return res5

if __name__ == "__main__":
    A = "香奈"
    B = "017"
    C = "./g_code_tname_clean.csv"

    res5 = find_same_word(A, B, C)
    # print(res5)