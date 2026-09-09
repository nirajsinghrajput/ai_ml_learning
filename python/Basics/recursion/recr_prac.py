#question 1

# def cal_sum(n):
#     sum=0
#     if(n==0):
#         return 0
#     else:
#         sum = cal_sum(n-1) + n
#     return sum
# print(cal_sum(5))


#question 2

def pr_list(list,idx=0):
    if(idx==len(list)):
        return
    print(list[idx])
    pr_list(list,idx+1)

heroes = ["SpiderMan","Thor","SuperMan","Krish","Shaktiman","Caps","ironman"]
pr_list(heroes)