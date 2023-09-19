class PrePro:
    @staticmethod
    def filter(lines):
        code = ""
        for line in lines:
            new_line = line.split("//")[0]
            if new_line[-1] != "\n":
                new_line += "\n"
            code += new_line
        return code
