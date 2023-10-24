class PrePro:
    @staticmethod
    def filter(lines):
        code = ""
        for line in lines:
            code_segment = line.split("//")[0]
            if len(code_segment) == 0:
                code += "\n"
                continue
            if code_segment[-1] != "\n":
                code_segment += "\n"
            code_segment = code_segment.replace("\t", "")
            code += code_segment
        return code
