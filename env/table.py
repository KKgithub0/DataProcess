#!usr/bin/python
#coding:utf-8

class MyTable:
    __default_encoding  = "utf8"
    __text              = ""
    def __init__(self):
        pass

    def gen_field(self, field_str, colspan=1, rowspan=1, font_size=14, bg_color="#FFFFFF", text_align="center"):
        if type(field_str) == float:
            field_str = "%.2f" % field_str
        return """
                <td rowspan='{rowspan}';
                    colspan='{colspan}';
                    style='background-color:{bg_color};
                    font-size:{font_size}px;
                    width:{width}px;
                    height={height}px;
                    text-align:{text_align};'>\n
                {td_str}\n
                </td>\n""".format(
                td_str      = field_str,
                width       = colspan*120,
                height      = 50,
                colspan     = colspan,
                rowspan     = rowspan,
                font_size   = font_size,
                bg_color    = bg_color,
                text_align  = text_align).decode(self.__default_encoding,"ignore")
        pass

    def gen_fields(self, field_str_list, colspan=1, rowspan=1, font_size=14, bg_color="#FFFFFF", text_align="center"):
        fields = list()
        for field_str in field_str_list:
            fields.append(self.gen_field(field_str, colspan, rowspan, font_size, bg_color, text_align))
        return fields
        pass

    def add_line(self, fields):
        self.__text += """
                <tr>
                    {td_text}
                </tr>\n""".format(
                td_text=("\t".join(fields)).encode(self.__default_encoding,"ignore"))
        pass

    def text(self):
        return """<table border='1';
                          cellpadding='0'
                          cellspacing='0'
                          style='border-collapse:collapse;font-size:18px;border:solid 1px; table-layout:fixed;text-align:right;'>
                {text}
               </table>""".format(
                text=self.__text)

        return
