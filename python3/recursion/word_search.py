# https://leetcode.com/problems/word-search/


from typing import List


class Solution:
    def exist(self, board: List[List[str]], word: str) -> bool:
        path = set()
        found = False

        rows = len(board)
        cols = len(board[0])
        word_len = len(word)

        def solve(i, x, y):
            nonlocal board, path, word, rows, cols, word_len, found

            if (x, y) in path:
                return
            elif x < 0 or y < 0 or x >= rows or y >= cols:
                return
            else:
                wc = word[i]
                bc = board[x][y]

                if wc == bc:
                    if i == (word_len - 1):
                        found = True
                        return

                    path.add((x, y))
                    solve(i + 1, x + 1, y)
                    solve(i + 1, x - 1, y)
                    solve(i + 1, x, y + 1)
                    solve(i + 1, x, y - 1)
                    path.remove((x, y))
                else:
                    return

        for x in range(0, rows):
            for y in range(0, cols):
                found = False
                path = set()

                solve(0, x, y)

                if found:
                    return found

        return False
