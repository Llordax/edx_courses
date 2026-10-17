# Request the name of the camelcase variable from the user
camel_case = input("camelCase: ")

# Replace every uppercase letter with its snake_case equivalent
# The replacements follow one by one
snake_case = (
    camel_case.replace("A", "_a")
    .replace("B", "_b")
    .replace("C", "_c")
    .replace("D", "_d")
    .replace("E", "_e")
    .replace("F", "_f")
    .replace("G", "_g")
    .replace("H", "_h")
    .replace("I", "_i")
    .replace("J", "_j")
    .replace("K", "_k")
    .replace("L", "_l")
    .replace("M", "_m")
    .replace("N", "_n")
    .replace("O", "_o")
    .replace("P", "_p")
    .replace("Q", "_q")
    .replace("R", "_r")
    .replace("S", "_s")
    .replace("T", "_t")
    .replace("U", "_u")
    .replace("V", "_v")
    .replace("W", "_w")
    .replace("X", "_x")
    .replace("Y", "_y")
    .replace("Z", "_z")
)

# print input in snake_case
print("snake_case:", snake_case)

