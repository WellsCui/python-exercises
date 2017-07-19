def getAnagram(needle):
    length = len(needle);
    if length == 1:
        yield needle
    else:
        for i in range(length):
            for subAnagram in getAnagram(needle[:i] + needle[i + 1:]):
                yield needle[i] + subAnagram


def getAnagramIndices(haystack, needle):
    len1 = len(haystack)
    len2 = len(needle)
    anagrams = list(getAnagram(needle))
    for i in range(len1 - len2):
        if haystack[i:i + len2] in anagrams:
            yield i


def is_included_in(str1, str2):
    _exhausted = object()
    return next((c for c in str1 if c not in str2), _exhausted) == _exhausted


def is_inter_included(str1, str2):
    return is_included_in(str1, str2) and is_included_in(str2, str1)


def getAnagramIndices2(haystack, needle):
    len1 = len(haystack)
    len2 = len(needle)
    return (i for i in range(len1 - len2 + 1) if is_inter_included(haystack[i:i + len2], needle))


print(list(item for item in getAnagram("ab")))
print(list(item for item in getAnagramIndices2("abcbabee", "ab")))
