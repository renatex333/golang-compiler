class PrePro:
    @staticmethod
    def filter(lines):
        code = ""
        for line in lines:
            code += line.split("//")[0]
        code = code.replace("\n", "")
        return code
