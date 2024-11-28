import random

end = bytes([random.getrandbits(8) for _ in range(8)]).hex()
flag = "flag{r3d1rect1ng_d1_y4pp5_"+end+"}"

print(f"Generated {flag=}")
with open("flag", "w") as file:
    file.write(flag)
    file.close()

