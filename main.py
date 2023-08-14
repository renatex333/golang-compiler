import sys
import operator

valid_operations = {'+': operator.add, '-': operator.sub}

def preprocess(arg):
    string = arg
    string = string.replace("\\n","")
    print(string)
    return string

def lexical_analysis(s):
    for i in range(len(s)):
        if not (s[i].isnumeric() or s[i] in valid_operations or s[i] == " "):
            raise Exception(f"Invalid input: {s[i]} in {repr(s)}")

def syntactic_analysis(s):
    pass

def semantic_analysis(s):
    for i in range(len(s)):
        # Checa se um operador está entre dois números
        if s[i] in valid_operations:
            if i == 0 or i == len(s)-1:
                raise Exception(f"Invalid input: {s[i]} in {repr(s)}")
            
            for j in range(i+1, len(s)):
                if s[j] == " ":
                    continue
                if s[j].isnumeric():
                    break
                if s[j] in valid_operations:
                    raise Exception(f"Invalid input: {s[i]} in {repr(s)}")
            else:
                raise Exception(f"Invalid input: {s[i]} in {repr(s)}")
            
            for j in range(i-1, -1, -1):
                if s[j] == " ":
                    continue
                if s[j].isnumeric():
                    break
                if s[j] in valid_operations:
                    raise Exception(f"Invalid input: {s[i]} in {repr(s)}")
            else:
                raise Exception(f"Invalid input: {s[i]} in {repr(s)}")
            
        # Checa se não há espaços entre os números
        elif s[i] == " " and s[i-1].isnumeric():
            for j in range(i+1, len(s)):
                if s[j] == " ":
                    continue
                if s[j] in valid_operations:
                    break
                if s[j].isnumeric():
                    raise Exception(f"Invalid input: {s[i]} in {repr(s)}")

def calculate(s):
    operands = []
    operators = []
    number = ""
    for i in range(len(s)):
        if s[i].isnumeric():
            number += s[i]
        elif s[i] in valid_operations:
            operands.append(int(number))
            operators.append(s[i])
            number = ""
        if i == len(s)-1:
            operands.append(int(number))
    
    result = operands[0]
    for operand, operator in zip(operands[1:], operators):
        result = valid_operations[operator](result, operand)
    return result

def main(argv):
    string = preprocess(argv[1])
    lexical_analysis(string)
    syntactic_analysis(string)
    semantic_analysis(string)
    result = calculate(string)
    print(result)

if __name__ == "__main__":
    main(sys.argv)


