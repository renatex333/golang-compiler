class PrePro:
    @staticmethod
    def filter(lines):
        code = ""
        for line in lines:
            new_line = line.split("//")[0]
            if len(new_line) == 0:
                code += "\n"
                continue
            if new_line[-1] != "\n":
                new_line += "\n"
            new_line = new_line.replace("\t", "")
            code += new_line
        return code
