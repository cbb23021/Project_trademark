import pandas as pd
import re

def check_famous(input_s):
    df = pd.read_csv("./famous_clean.csv")
    col_check = df['famous_tname'].apply(lambda x: str(x)).tolist()
    ans_list = []
    # print(col_check)
    ans_list=[]
    for i in enumerate(col_check):
        if len(str(input_s)) >0:
            if str.upper(input_s) == str.upper(i[1]):
                ans = "[ " + input_s + " ]" + " was registered as famous tmark "+ "[ " +i[1] +" ]"
                # return ans
            elif len(re.findall(str.upper(input_s),str.upper(i[1]),flags=0)) != 0:
                if i[1] not in ans_list:
                    ans_list.append(i[1])
                ans = "[ " +input_s + " ]" + " is similar to famous tmark " + "[ " + str(ans_list) +" ]"
                # return ans

            else:
                output_score = []
                tmp_list = []
                for j in input_s:
                    # print(j)
                    # print(i[1])
                    # tmp_list = []
                    for k in str(i[1]):
                        # print(k)
                        if str.upper(j) == str.upper(k):
                            # print(k)
                            # print(j)
                            tmp_list.append(k)
                            # print(i[1])
                # print(tmp_list)

                output_score.append((len(tmp_list)/len(i[1]),i[0]))
                for l in output_score:
                    if l[0] >= 0.6:
                        if i[1] not in ans_list:
                            ans_list.append(i[1])
        else:
            ans = "--沒有相似的著名商標--"
    if len(ans_list) != 0:
        ans = str(",".join(ans_list))
    else:
        return "--沒有相似的著名商標--"
    return ans



if __name__ == "__main__":
    a= check_famous("CHANEL")

    print(a)



