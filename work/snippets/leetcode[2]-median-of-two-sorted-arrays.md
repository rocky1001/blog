Title: leetcode[2]-median-of-two-sorted-arrays
Date: 2015-08-19 16:44
Category: Work
Tags: leetcode, python, java
Summary: leetcode刷题记录2-median_of_two_sorted_arrays
Slug: leetcode[2]-median-of-two-sorted-arrays

##原题
leetcode第二题，median of two sorted arrays，难度为困难，通过率为：17.6%

原题链接见：https://oj.leetcode.com/problems/median-of-two-sorted-arrays/

简单翻译下：

已知（输入）：两个已排序的数组，长度分别是m和n。

要求（输出）：找到两个已排序数组的中位数（median），要求程序总的时间复杂度为O(log(m+n))。

##分析：

题目不难，但是在理解上有一点歧义（可能是我个人的理解问题）：

1. 中位数指的是一个已升序排序数组中，位置处于中间的那个数（如果数组具有偶数个数据的话，就是中间两个数的平均值）

2. 那么，原题要求找出“两个数组的中位数”，但是返回值只有一个，显然不能分别找出两个数组的两个中位数了，我的理解是将两个数组合并，重新排序后，找出这个新的数组的中位数。

##解决方案：

1. python版本解决方案1

````python
def findMedianSortedArrays(A, B):
    C = sorted(A + B)
    # print C
    if len(C) % 2 == 0:
        index = len(C) / 2
        median = (C[index] + C[index - 1]) / 2.0
    else:
        index = (len(C) - 1) / 2
        median = C[index]
    return median
````

找出中位数的算法非常简单，不再赘述。稍微麻烦点的是对两个数组进行合并和排序，值得庆幸的是，在python中，这一切只需要一行代码就可以搞定。

执行时间：620ms（leetcode记录）

时间复杂度：上面代码最主要算法就是是采用了python的sorted函数，

而该函数使用的算法为Timsort（参见wikipedia；关于python内置sorted实现算法的问题，也可以参见stackoverflow上面的一个答案），该算法的时间复杂度为O(n)到O(n log n)之间；

空间复杂度：O(n)——同样是由timsort算法决定的。

##存在的问题：

虽然leetcode accept了该解法，但是显然该解法的时间复杂度不满足原题的要求：O(log(m+n))，

主要原因是，上述解法浪费了“两个已排序的数组”这个条件，重新对连接后的数组进行了排序。