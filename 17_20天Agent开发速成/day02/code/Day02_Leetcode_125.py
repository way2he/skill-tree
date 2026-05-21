# -*- coding: utf-8 -*-
"""
Day 02 算法热身: Leetcode 125. 验证回文串
20天Agent开发速成 - 第2天

题目链接: https://leetcode.cn/problems/valid-palindrome/
难度: 简单

为什么和Agent相关：
- Prompt工程天天要处理字符串
- 回文判断是字符串处理的基础技能
- 双指针思想在文本匹配中广泛应用
"""

from typing import Tuple


class Solution:
    """
    验证回文串解决方案
    """

    def isPalindrome(self, s: str) -> bool:
        """
        验证字符串是否为回文串

        回文串定义：
        - 只考虑字母和数字字符
        - 忽略大小写
        - 正读反读相同

        算法：双指针法
        时间复杂度: O(n)
        空间复杂度: O(1)

        Args:
            s: 输入字符串

        Returns:
            是否为回文串
        """
        if not s:
            return True

        # 初始化双指针
        left: int = 0
        right: int = len(s) - 1

        while left < right:
            # 左指针：跳过非字母数字字符
            while left < right and not s[left].isalnum():
                left += 1

            # 右指针：跳过非字母数字字符
            while left < right and not s[right].isalnum():
                right -= 1

            # 比较字符（忽略大小写）
            if s[left].lower() != s[right].lower():
                return False

            # 移动指针
            left += 1
            right -= 1

        return True

    def isPalindrome_pythonic(self, s: str) -> bool:
        """
        Pythonic写法：过滤后比较

        时间复杂度: O(n)
        空间复杂度: O(n) - 需要额外空间存储过滤后的字符串

        Args:
            s: 输入字符串

        Returns:
            是否为回文串
        """
        # 过滤：只保留字母数字，并转为小写
        filtered: str = "".join(char.lower() for char in s if char.isalnum())

        # 比较正序和逆序
        return filtered == filtered[::-1]


def test_solution():
    """
    测试用例
    """
    solution = Solution()

    test_cases: list[Tuple[str, bool]] = [
        # (输入, 期望输出)
        ("A man, a plan, a canal: Panama", True),
        ("race a car", False),
        (" ", True),
        ("a", True),
        ("ab_a", True),
        ("0P", False),
        (".,", True),  # 空字符串也是回文
    ]

    print("🧪 Leetcode 125. 验证回文串 - 测试")
    print("=" * 60)

    all_passed = True
    for i, (input_str, expected) in enumerate(test_cases, 1):
        result1 = solution.isPalindrome(input_str)
        result2 = solution.isPalindrome_pythonic(input_str)

        passed = (result1 == expected) and (result2 == expected)
        status = "✅ PASS" if passed else "❌ FAIL"

        print(f"\n测试用例 {i}: {status}")
        print(f"  输入: '{input_str}'")
        print(f"  期望: {expected}")
        print(f"  双指针法: {result1}")
        print(f"  Pythonic法: {result2}")

        if not passed:
            all_passed = False

    print("\n" + "=" * 60)
    print(f"测试结果: {'全部通过!' if all_passed else '存在失败用例'}")

    return all_passed


def demonstrate_agent_application():
    """
    演示在Agent中的应用
    """
    print("\n🤖 Agent应用场景演示")
    print("=" * 60)

    # 场景1: 检查用户输入是否对称
    print("\n场景1: 检查对称性输入")
    inputs = ["level", "hello", "A Toyota's a Toyota", "Was it a car or a cat I saw"]
    solution = Solution()

    for text in inputs:
        is_pal = solution.isPalindrome(text)
        print(f"  '{text}' -> {'回文' if is_pal else '非回文'}")

    # 场景2: Prompt中的文本处理
    print("\n场景2: Prompt模板匹配")
    template = "请总结以下内容：{}"
    user_input = "   这是一个重要的文档!!!   "

    # 清理用户输入（类似回文判断中的过滤）
    cleaned = "".join(c for c in user_input if c.isalnum() or c.isspace())
    final_prompt = template.format(cleaned.strip())
    print(f"  原始输入: '{user_input}'")
    print(f"  清理后: '{cleaned.strip()}'")
    print(f"  最终Prompt: '{final_prompt}'")


def main():
    """
    主函数
    """
    print("🎯 Day 02 算法热身: Leetcode 125. 验证回文串")
    print("=" * 60)

    # 运行测试
    test_solution()

    # 展示Agent应用
    demonstrate_agent_application()

    print("\n" + "=" * 60)
    print("🎉 算法热身完成!")
    print("\n核心知识点:")
    print("  • 双指针技巧: 从两端向中间逼近")
    print("  • 字符过滤: isalnum() 检查字母数字")
    print("  • 大小写处理: lower() 统一比较")
    print("  • 边界条件: 空字符串也是回文")
    print("\nAgent应用:")
    print("  • 文本清理和标准化")
    print("  • 输入验证和匹配")
    print("  • Prompt预处理")


if __name__ == "__main__":
    main()
