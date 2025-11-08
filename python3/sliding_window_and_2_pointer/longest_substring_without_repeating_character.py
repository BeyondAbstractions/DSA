# https://leetcode.com/problems/longest-substring-without-repeating-characters/description/


class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:

        i = 0
        j = i + 1
        cache = set()
        if s:
            cache.add(s[i])
        else:
            return 0
        max_ret = 0
        len_s = len(s)

        max_ret = max(max_ret, len(cache))

        while 1:

            if j >= len_s:
                break

            max_ret = max(max_ret, len(cache))

            if s[j] in cache:

                while 1:
                    if i >= j:
                        cache.add(s[j])
                        break

                    cache.remove(s[i])

                    if s[i] == s[j]:
                        cache.add(s[j])
                        i += 1
                        break

                    i += 1

            else:
                cache.add(s[j])

            max_ret = max(max_ret, len(cache))

            j += 1

        return max_ret
