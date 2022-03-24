cnt, ans = 0, 0
with open("output2.txt") as f:
    for line in f:
        if "open(" in line or "openat(" in line:
            cnt += 1
        elif "close(" in line:
            cnt -= 1
        ans = max(ans, cnt)
print(ans)
