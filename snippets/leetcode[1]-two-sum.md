Title: leetcode[1]-two-sum
Date: 2015-08-19 16:37
Category: Snippets
Tags: leetcode, python, java
Summary: leetcode刷题记录1-two_sum
Slug: leetcode[1]-two-sum

##原题

leetcode第一题，two sum，难度为适中，通过率为：18.4%

原题链接见：https://oj.leetcode.com/problems/two-sum/

简单翻译下：

已知（输入）：一个整型（integers）数组，一个目标整型数字，要求在数组中找出两个数，相加之和等于该目标整型数字。

要求（输出）：找到符合条件的数组中的两个整型数字的序号，要求序号1小于序号2，并且这些序号是从1开始的（数组默认index为从0开始）。

其他假设条件：假设一组输入数据，只有一个解。

举例：

输入：numbers={2, 7, 11, 15}, target=9

输出：index1=1, index2=2



##分析：

题目不难，但是需要考虑的特殊情况比较多，尝试三次后成功提交，期间掉入的坑主要有这个：

Input: [3,2,4], 6

Output: 1, 1

Expected: 2, 3

——没有判断index2不能等于index1



##解决方案：
1. python版本解决方案1

这是稍微思考后的方案。

````python
def twoSum(self, num, target):
    index1 = 0
    index2 = 0
    numberDict = dict()
    for indexCurrent, number in enumerate(num):
        # 使用dict缓存所有数据和对应的index
        numberDict[number] = indexCurrent
    for indexCurrent, number in enumerate(num):
        diff = target - number
        index2 = numberDict.get(diff, 0)
        if index2 == indexCurrent:
            continue
        if index2:
            index1 = indexCurrent
            break
    return index1 + 1, index2 + 1
````

首先使用dict存储数组的数据（用空间换时间），

然后遍历一遍整个数组，计算当前数字和target数字的差值，在dict中查找该差值，若能找到则说明找到了组合，若找不到则遍历结束后程序返回。

执行时间：204ms（leetcode记录）

时间复杂度：O(n)

空间复杂度：O(n)

2. python版本解决方案2

这是第一直觉的方案，但是仔细想一下就会发现时间复杂度很高。

````python
def twoSum(num, target):
    # 使用双重循环，时间复杂度O(n^2)
    index1 = 0
    index2 = 0
    bingo = False
    for i in range(len(num)):
        for j in range(i + 1, len(num)):
            if target - num[i] == num[j]:
                index1 = i
                index2 = j
                bingo = True
                break
        if bingo:
            break
    return index1 + 1, index2 + 1
````

时间复杂度：O(n^2)

空间复杂度：O(1)

也可以称为冒泡查找，就不详细说了，因为leetcode没过，TLE（Time Limit Exceeded）错误了。

下面列一下java版本代码，实际上就是上述python代码的简单改写。

3. java版本解决方案1

````java
public int[] twoSum(int[] numbers, int target) {
  Integer index1 = 0;
  Integer index2 = 0;
  Map<Integer, Integer> numberMap = new HashMap<Integer, Integer>();
  for (int i = 0; i < numbers.length; i++) {
    numberMap.put(numbers[i], i);
  }
  for (int i = 0; i < numbers.length; i++) {
    Integer diff = target - numbers[i];
    index2 = numberMap.get(diff);
    if (null == index2 || index1 == index2) {
      continue;
    } else {
      if (index2.intValue() > 0) {
        index1 = i;
        break;
      }
    }
  }
  int[] result = {index1.intValue() + 1, index2.intValue() + 1};
  return result;
}
````

执行时间：476ms（leetcode记录）

4. java版本解决方案2

````java
public int[] twoSum(int[] numbers, int target) {
  Integer index1 = 0;
  Integer index2 = 0;
breakpoint:for (int i = 0; i < numbers.length; i++) {
    for (int j = i + 1; j < numbers.length; j++) {
      Integer diff = target - numbers[i];
      if (diff.intValue() == numbers[j]) {
        index1 = i + 1;
        index2 = j + 1;
        break breakpoint;
      }
    }
  }
  int[] result = {index1.intValue() + 1, index2.intValue() + 1};
  return result;
}
````

leetcode没过，TLE（Time Limit Exceeded）错误了。

（5）java版本解决方案3（同1，不过是只有一个循环精简版本）  

````java
public int[] twoSum(int[] numbers, int target) {
  Integer index1 = 0;
  Integer index2 = 0;
  Map<Integer, Integer> numberMap = new HashMap<Integer, Integer>();
  for (int i = 0; i < numbers.length; i++) {
    Integer diff = target - numbers[i];
    if (null != numberMap.get(diff)) {
      index1 = i + 1;
      index2 = numberMap.get(diff) + 1;
      if (index1 != index2) {
        if (index1.intValue() > index2.intValue()) {
          Integer tmp = index1;
          index1 = index2;
          index2 = tmp;
        }
        break;
      }
    } else {
      numberMap.put(numbers[i], i);
    }
  }
  int[] result = {index1.intValue(), index2.intValue()};
  return result;
}
````

执行时间：348ms（leetcode记录）

##存在的问题：

1. 在找不到解时，没有对返回的数据进行合理判断和处理；

2. 使用dict存储所有数据的解决方案，若数字中有重复的，则只会存储最后一个重复数字的index，例如：
[0, 3, 3, 4], 7   
答案可以是 2, 4 或3, 4，用上面的方法只能找出3, 4